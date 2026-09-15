#!/usr/bin/env python3
"""Valida primitivas do GitHub Copilot e políticas de governança do repositório.

Esta é a camada de avaliação/governança do harness de agentes do
datacorp-mm-team-kit. Ela transforma regras antes aplicadas apenas pela memória
das pessoas em uma verificação automatizada, para que primitivas quebradas falhem de
forma visível, em vez de silenciosa.

O que é verificado
------------------
1. Esquema do frontmatter de agentes, prompts, instruções e habilidades.
2. Integridade referencial: prompt -> agente, handoffs de agentes e links
   relativos de Markdown em .github/.
3. Definições de ganchos (`hooks`): validade do JSON, versão, nomes de eventos,
   tipos de manipuladores e existência e permissão de execução de todo script referenciado.
4. Política do repositório: ausência de pragmas do markdownlint, de nomes
   incorretos para o evento, de recomendações de assistentes/IDEs concorrentes e
   de nomes obsoletos de diretórios.
5. Estrutura: todo arquivo Markdown em .github/ termina com exatamente uma
   quebra de linha e contém exatamente um H1.
6. Seções do corpo: todo agente, prompt, habilidade e instrução contém as seções
   `## ` obrigatórias para seu tipo de primitiva (prompts também na ordem
   canônica), de acordo com as primitivas de referência.

Restrições de projeto
---------------------
- Python 3.11+, somente biblioteca padrão. A CI não deve precisar de
  `pip install`, portanto o frontmatter YAML é lido por um pequeno parser
  tolerante, em vez de PyYAML.
- Os arquivos são enumerados com `git ls-files` para que o validador veja
  exatamente o conteúdo obtido pela CI (arquivos versionados), ignorando
  arquivos temporários não versionados.

Código de saída
---------------
Encerra com código diferente de zero quando encontra qualquer violação de nível
de erro. Avisos não reprovam a verificação. Uma anotação `::error`/`::warning` do
GitHub Actions é impressa para cada ocorrência, seguida por um resumo agrupado.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]

# Caminhos POSIX relativos ao repositório para este script e sua documentação
# complementar. Eles são isentos das verificações de política de conteúdo abaixo
# porque contêm legitimamente os literais proibidos (como regexes e documentação).
SCRIPT_RELPATH = os.path.relpath(SCRIPT_PATH, REPO_ROOT).replace(os.sep, "/")
DOC_RELPATH = "docs/copilot-primitive-validation.md"
POLICY_EXEMPT_FILES = {SCRIPT_RELPATH, DOC_RELPATH}

# --- Esquemas oficiais de frontmatter --------------------------------------

AGENT_ALLOWED_KEYS = {
    "name", "description", "tools", "model", "handoffs", "mcp-servers",
    "argument-hint", "target", "user-invocable", "disable-model-invocation",
    "metadata", "agents",
}
AGENT_REQUIRED_KEYS = {"description"}
AGENT_RETIRED_KEYS = {
    "infer": "chave de frontmatter obsoleta 'infer' (removida do esquema de agentes)",
}

PROMPT_ALLOWED_KEYS = {"name", "description",
                       "agent", "model", "tools", "argument-hint"}
PROMPT_REQUIRED_KEYS: set[str] = set()
PROMPT_RETIRED_KEYS = {
    "mode": "chave obsoleta 'mode' (sintaxe de modo de conversa substituída por 'agent')",
    "tested_with": "chave inválida 'tested_with' (não faz parte do esquema de prompts)",
}

INSTRUCTION_ALLOWED_KEYS = {"applyTo", "name", "description", "excludeAgent"}
INSTRUCTION_REQUIRED_KEYS: set[str] = set()
INSTRUCTION_RETIRED_KEYS: dict[str, str] = {}

SKILL_NONSTANDARD_KEYS = {"license",
                          "allowed-tools", "compatibility", "metadata"}

# --- Esquema de hooks -------------------------------------------------------

HOOK_EVENTS = {
    "sessionStart", "sessionEnd", "userPromptSubmitted", "userPromptTransformed",
    "preToolUse", "postToolUse", "postToolUseFailure", "agentStop",
    "subagentStart", "subagentStop", "errorOccurred", "notification",
    "permissionRequest", "preCompact",
}
HOOK_TYPES = {"command", "http", "prompt"}

# --- Política do repositório -----------------------------------------------

STALE_PATHS = ["01-arqueologia", "02-spec-moderna",
               "06-agentes-de-estagio", "legado-sifap"]

# Arquivos que podem manter legitimamente um pragma inline do markdownlint. Nos
# demais casos, .markdownlint-cli2.jsonc na raiz é a fonte única da verdade.
PRAGMA_ALLOWED_FILES = {"docs/adr/0000-template.md", "docs/DOC-STYLE-GUIDE.md"}
# Arquivos que documentam a proibição de nomes do evento e, por isso, citam as palavras proibidas.
TERMINOLOGY_EXEMPT_FILES = {"docs/DOC-STYLE-GUIDE.md"} | POLICY_EXEMPT_FILES

COMPETING_TOOLS = [
    "Cursor", "Windsurf", "Codex", "Cline", "Continue", "Aider", "Codeium",
    "Tabnine", "IntelliJ", "Eclipse", "Neovim",
]
TOOL_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(COMPETING_TOOLS) + r")(?![A-Za-z0-9])")
RECOMMEND_VERB_RE = re.compile(
    r"\b(use|uses|using|used|try|tries|trying|install|installs|installing|"
    r"adopt|adopts|adopting|switch|switching|migrate|migrating|recommend|"
    r"recommends|recommended|recommending|prefer|prefers|choose|choosing|"
    r"pick|picking|run|running|open|opens|opening|usar?|use|utiliz(?:a|e|ar|ando)|"
    r"tentar?|tente|instal(?:a|e|ar|ando)|adot(?:a|e|ar|ando)|trocar?|troque|"
    r"migr(?:a|e|ar|ando)|recomend(?:a|e|ar|ando)|prefer(?:e|ir|indo)|"
    r"escolh(?:a|e|er|endo)|selecion(?:a|e|ar|ando)|execut(?:a|e|ar|ando)|"
    r"abr(?:a|e|ir|indo))\b",
    re.IGNORECASE,
)
NEGATION_RE = re.compile(
    r"(?i)(\bdo not\b|\bdon'?t\b|\bnever\b|\bavoid(?:ing)?\b|\binstead of\b|"
    r"\brather than\b|\bnot\b|"
    r"\bno\s+one(?=\s|[,;:.!?]|$)|\bnobody\b|"
    r"\bno\s+(?:[A-Za-z][A-Za-z'-]*\s+){1,6}"
    r"(?:(?:should|must|may|can|could|would|will)\s+)?"
    r"(?:us(?:e|es|ed|ing)|tr(?:y|ies|ied|ying)|install(?:s|ed|ing)?|"
    r"adopt(?:s|ed|ing)?|switch(?:es|ed|ing)?|migrat(?:e|es|ed|ing)|"
    r"recommend(?:s|ed|ing)?|prefer(?:s|red|ring)?|choos(?:e|es|ing)|chose|"
    r"pick(?:s|ed|ing)?|run(?:s|ning)?|ran|open(?:s|ed|ing)?)\b|"
    r"\b(?:there\s+(?:is|are)|(?:i|we|the team)\s+(?:have|has))\s+no\s+"
    r"(?:plans?|intentions?|reasons?|needs?|requirements?|obligations?|necessit(?:y|ies)|"
    r"permissions?)\s+to\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+(?:need|reason|way|justification|requirement|obligation|necessity|"
    r"intention|plan|permission)\s+to\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+(?:reason|need|requirement|obligation|necessity|permission)\s+for\s+"
    r"(?:\w+\s+){1,3}to\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+(?:reason|need)\s+(?:i|we|you|they|users?|developers?|teams?|people|persons?|"
    r"members?|organizations?|projects?)\s+(?:should|must|may|can|could|would|will)\s+"
    r"(?:use|try|install|adopt|switch|migrate|recommend|prefer|choose|pick|run|open)\b|"
    r"\bno\s+use\s+of\b|"
    r"\bno longer\b|"
    r"\bban(?:ned|s|ning)?\b|\bprohibit\w*\b|"
    r"\bforbid\w*\b|\bdisallow\w*\b|\bunlike\b|\bcannot\b|\bcan'?t\b|"
    r"\bwon'?t\b|\bshould ?n'?t\b|\bshould not\b|\bmust ?n'?t\b|\bmust not\b|"
    r"\brefrain\b|\breject\w*\b|\bdeprecat\w*\b|\bnão\b|\bnunca\b|\bjamais\b|"
    r"^\s*(?:[-*+>]\s+|\d+[.)]\s+)*(?:nem|tampouco|nor|neither)\b|"
    r"\bevit(?:e|ar|ando)\b|\bsem\s+(?:usar?|utiliz(?:ar|e)|instal(?:ar|e)|"
    r"adot(?:ar|e)|trocar?|migrar?|recomendar?|preferir|escolher|selecionar|"
    r"executar?|abrir)\b|"
    r"\b(?:ninguém|nenhum(?:a)?\s+"
    r"(?:usuários?|desenvolvedor(?:es)?|equipes?|pessoas?|membros?|organizações?|projetos?))\b|"
    r"\bem vez de\b|\bao invés de\b|\bproib\w*\b|\bvedad\w*\b|\bnão pode\b|"
    r"\bnão deve\b|\bnão usar\b|\brejeit\w*\b|\bdescontinu\w*\b|❌)"
)
INTERROGATIVE_RE = re.compile(
    r"(?i)(\b(?:can|could|should|may|shall|do|would|will)\s+(?:i|we|you)\b|"
    r"^\s*(?:[-*+>#]\s*)*(?:eu\s+)?posso\b|"
    r"\b(?:verifique|verificar|avalie|avaliar|confirme|confirmar|determine|"
    r"determinar|descubra|descobrir|pergunte|perguntar|saber)\s+se\s+"
    r"(?:eu\s+)?(?:posso|podemos|pode|devo|devemos|deveria|poderia)\b|"
    r"\bwhat about\b|\bis it ok\b|\be quanto a\b|\bestá tudo bem\b|\?)"
)
RECOMMEND_WINDOW = 40  # caracteres antes do nome da ferramenta que podem conter o verbo
HARD_CLAUSE_BOUNDARIES = ";!?"
CONTRAST_BOUNDARY_RE = re.compile(
    r",\s+(?:mas|porém|contudo|todavia|portanto|logo|então|but|however|yet|so|"
    r"therefore|thus)(?:,\s*|\s+)",
    re.IGNORECASE,
)
PERIOD_ABBREVIATIONS = {
    "dr", "dra", "e.g", "etc", "ex", "i.e", "jr", "mr", "mrs", "ms",
    "p.ex", "prof", "sr", "sra", "v", "ver", "vs",
}


class Reporter:
    """Coleta ocorrências, emite anotações do GitHub e imprime um resumo."""

    def __init__(self) -> None:
        self.findings: list[dict] = []

    def _add(self, level: str, check: str, file: str, line: int | None, message: str) -> None:
        self.findings.append(
            {"level": level, "check": check, "file": file,
                "line": line, "message": message}
        )
        location = file if file else "repositório"
        annotation = f"::{level} file={file}" if file else f"::{level} "
        if file and line:
            annotation += f",line={line}"
        annotation += f"::[{check}] {location}"
        if line:
            annotation += f":{line}"
        annotation += f" - {message}"
        print(annotation)

    def error(self, check: str, file: str, line: int | None, message: str) -> None:
        self._add("error", check, file, line, message)

    def warning(self, check: str, file: str, line: int | None, message: str) -> None:
        self._add("warning", check, file, line, message)

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f["level"] == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f["level"] == "warning")

    def summarize(self) -> None:
        print("\n" + "=" * 72)
        print("Resumo da validação das primitivas do Copilot")
        print("=" * 72)
        if not self.findings:
            print("Nenhum problema encontrado. Todas as primitivas e políticas do Copilot foram aprovadas.")
            return
        by_check: dict[str, dict[str, int]] = {}
        for finding in self.findings:
            bucket = by_check.setdefault(
                finding["check"], {"error": 0, "warning": 0})
            bucket[finding["level"]] += 1
        for check in sorted(by_check):
            counts = by_check[check]
            print(
                f"  {check:<24} {counts['error']:>3} erro(s)"
                f"  {counts['warning']:>3} aviso(s)"
            )
        print("-" * 72)
        print(
            f"  {'TOTAL':<24} {self.error_count:>3} erro(s)  {self.warning_count:>3} aviso(s)")
        print("=" * 72)


# --- Utilitários de arquivos ------------------------------------------------

def tracked_files() -> list[str]:
    """Retorna caminhos POSIX relativos ao repositório de arquivos versionados, como na CI.

    Usa uma varredura do sistema de arquivos como alternativa quando o git não está disponível.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
            capture_output=True,
            check=True,
        )
        return [p for p in result.stdout.decode("utf-8", "replace").split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        skip_dirs = {".git", "node_modules"}
        skip_prefixes = ("backend/target/", "frontend/.next/")
        paths: list[str] = []
        for root, dirs, files in os.walk(REPO_ROOT):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for name in files:
                rel = os.path.relpath(os.path.join(
                    root, name), REPO_ROOT).replace(os.sep, "/")
                if not rel.startswith(skip_prefixes):
                    paths.append(rel)
        return paths


def read_text(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8", errors="replace")


def read_bytes(rel: str) -> bytes:
    return (REPO_ROOT / rel).read_bytes()


def looks_binary(data: bytes) -> bool:
    return b"\x00" in data[:8192]


# --- Leitura do frontmatter -------------------------------------------------

FM_DELIM_RE = re.compile(r"^---\s*$")
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")


def split_frontmatter(text: str) -> list[str] | None:
    """Retorna as linhas do frontmatter ou None se estiver ausente/incompleto."""
    lines = text.split("\n")
    if lines and lines[0].startswith("\ufeff"):
        lines[0] = lines[0].lstrip("\ufeff")
    if not lines or not FM_DELIM_RE.match(lines[0]):
        return None
    for i in range(1, len(lines)):
        if FM_DELIM_RE.match(lines[i]):
            return lines[1:i]
    return None


def top_level_entries(fm_lines: list[str]) -> list[tuple[str, str, int]]:
    """Retorna (chave, valor_inline, índice_no_frontmatter) para chaves de nível superior."""
    entries = []
    for idx, line in enumerate(fm_lines):
        if not line or line[0] in " \t#":
            continue
        match = TOP_KEY_RE.match(line)
        if match:
            entries.append((match.group(1), match.group(2), idx))
    return entries


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def get_top_value(fm_lines: list[str], key: str) -> str | None:
    """Retorna o valor escalar de uma chave de nível superior, unindo escalares em bloco."""
    for idx, line in enumerate(fm_lines):
        match = TOP_KEY_RE.match(line)
        if not match or match.group(1) != key or (line[:1].isspace()):
            continue
        inline = match.group(2).strip()
        if inline and inline not in ("|", ">", "|-", ">-", "|+", ">+"):
            return unquote(inline)
        collected = []
        for follow in fm_lines[idx + 1:]:
            if follow.strip() == "":
                continue
            if follow[0] in " \t":
                collected.append(follow.strip())
            else:
                break
        return unquote(" ".join(collected)) if collected else ""
    return None


def handoff_agents(fm_lines: list[str]) -> list[tuple[str, int]]:
    """Retorna (valor_do_agente, índice) para cada agente nomeado no bloco handoffs."""
    results = []
    in_block = False
    for idx, line in enumerate(fm_lines):
        entry = TOP_KEY_RE.match(line)
        if entry and not line[:1].isspace():
            in_block = entry.group(1) == "handoffs"
            continue
        if in_block:
            nested = re.match(r"^\s+-?\s*agent:\s*(.+?)\s*$", line)
            if nested:
                results.append((unquote(nested.group(1)), idx))
    return results


def fm_line_number(idx: int) -> int:
    """Converte um índice do conteúdo do frontmatter em número de linha baseado em 1."""
    return idx + 2  # a linha 1 é o '---' de abertura


# --- Verificações de esquema ------------------------------------------------

def check_closed_schema(
    rel: str,
    fm_lines: list[str],
    allowed: set[str],
    required: set[str],
    retired: dict[str, str],
    reporter: Reporter,
    check: str,
) -> None:
    seen: dict[str, int] = {}
    for key, _inline, idx in top_level_entries(fm_lines):
        seen.setdefault(key, idx)
    for key, idx in seen.items():
        if key in retired:
            reporter.error(check, rel, fm_line_number(idx), retired[key])
        elif key not in allowed:
            reporter.error(
                check, rel, fm_line_number(idx),
                f"chave de frontmatter desconhecida '{key}' (permitidas: {', '.join(sorted(allowed))})",
            )
    for key in sorted(required):
        if key not in seen:
            reporter.error(
                check, rel, 1, f"chave obrigatória ausente no frontmatter: '{key}'")


def check_agents(agent_files: list[str], reporter: Reporter) -> None:
    for rel in agent_files:
        check_agent_structure(rel, reporter)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("agents", rel, 1,
                           "frontmatter YAML ausente ou incompleto")
            continue
        check_closed_schema(
            rel, fm_lines, AGENT_ALLOWED_KEYS, AGENT_REQUIRED_KEYS,
            AGENT_RETIRED_KEYS, reporter, "agents",
        )


def check_prompts(prompt_files: list[str], valid_agent_ids: set[str], reporter: Reporter) -> None:
    for rel in prompt_files:
        check_prompt_structure(rel, reporter)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("prompts", rel, 1,
                           "frontmatter YAML ausente ou incompleto")
            continue
        check_closed_schema(
            rel, fm_lines, PROMPT_ALLOWED_KEYS, PROMPT_REQUIRED_KEYS,
            PROMPT_RETIRED_KEYS, reporter, "prompts",
        )
        agent_value = get_top_value(fm_lines, "agent")
        if agent_value and agent_value not in valid_agent_ids:
            reporter.error(
                "referential-integrity", rel, 1,
                f'agent: "{agent_value}" não corresponde a nenhum agente em .github/agents/',
            )


def check_instructions(instruction_files: list[str], reporter: Reporter) -> None:
    for rel in instruction_files:
        check_instruction_structure(rel, reporter)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("instructions", rel, 1,
                           "frontmatter YAML ausente ou incompleto")
            continue
        check_closed_schema(
            rel, fm_lines, INSTRUCTION_ALLOWED_KEYS, INSTRUCTION_REQUIRED_KEYS,
            INSTRUCTION_RETIRED_KEYS, reporter, "instructions",
        )
        apply_to = get_top_value(fm_lines, "applyTo")
        if apply_to is not None and apply_to.strip() == "**":
            reporter.error(
                "instructions", rel, 1,
                "applyTo: \"**\" injeta este arquivo em todas as solicitações e consome a "
                "janela de contexto; restrinja-o a globs concretos",
            )


def check_skills(skill_files: list[str], reporter: Reporter) -> None:
    for rel in skill_files:
        check_skill_structure(rel, reporter)
        dirname = rel.split("/")[-2]
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            reporter.error("skills", rel, 1,
                           "frontmatter YAML ausente ou incompleto")
            continue
        seen = {key: idx for key, _inline, idx in top_level_entries(fm_lines)}
        for key in ("name", "description"):
            if key not in seen:
                reporter.error("skills", rel, 1,
                               f"chave obrigatória ausente no frontmatter: '{key}'")
        for key in sorted(SKILL_NONSTANDARD_KEYS):
            if key in seen:
                reporter.error(
                    "skills", rel, fm_line_number(seen[key]),
                    f"chave não padronizada no frontmatter da habilidade: '{key}'",
                )
        name = get_top_value(fm_lines, "name")
        if name is not None:
            if name != dirname:
                reporter.error(
                    "skills", rel, fm_line_number(seen.get("name", 0)),
                    f"o nome da habilidade '{name}' deve ser igual ao nome do diretório '{dirname}' "
                    "(uma divergência faz a habilidade falhar silenciosamente ao carregar)",
                )
            if not re.fullmatch(r"[a-z0-9-]+", name):
                reporter.error(
                    "skills", rel, fm_line_number(seen.get("name", 0)),
                    f"o nome da habilidade '{name}' deve conter somente letras minúsculas, dígitos e hifens",
                )
            if len(name) > 64:
                reporter.error(
                    "skills", rel, fm_line_number(seen.get("name", 0)),
                    f"o nome da habilidade tem {len(name)} caracteres; o limite é 64",
                )
        description = get_top_value(fm_lines, "description")
        if description is not None and len(description) > 1024:
            reporter.error(
                "skills", rel, fm_line_number(seen.get("description", 0)),
                f"a descrição da habilidade tem {len(description)} caracteres; o limite é 1024",
            )


def build_agent_registry(agent_files: list[str], reporter: Reporter) -> set[str]:
    """Identificadores válidos de agentes, obtidos dos arquivos presentes em .github/agents/.

    O id canônico é o `name:` do frontmatter, com fallback para o nome-base do
    arquivo quando `name:` está ausente. Quando ambos estão presentes, devem ser
    iguais; uma divergência é relatada porque um prompt vinculado por uma grafia
    não encontraria silenciosamente a outra.
    """
    ids: set[str] = set()
    for rel in agent_files:
        stem = Path(rel).name[: -len(".agent.md")]
        ids.add(stem)
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is not None:
            name = get_top_value(fm_lines, "name")
            if name:
                ids.add(name)
                if name != stem:
                    reporter.error(
                        "referential-integrity", rel, 1,
                        f"o nome do agente '{name}' não corresponde ao nome-base do arquivo '{stem}'; "
                        "renomeie para que o nome declarado e o arquivo sejam iguais",
                    )
    return ids


def check_handoffs(agent_files: list[str], valid_agent_ids: set[str], reporter: Reporter) -> None:
    for rel in agent_files:
        fm_lines = split_frontmatter(read_text(rel))
        if fm_lines is None:
            continue
        for agent_value, idx in handoff_agents(fm_lines):
            if agent_value not in valid_agent_ids:
                reporter.error(
                    "referential-integrity", rel, fm_line_number(idx),
                    f"o handoff aponta para o agente '{agent_value}', que não existe em .github/agents/",
                )


# --- Verificações de ganchos ------------------------------------------------

def check_hooks(hook_files: list[str], subdir_hook_files: list[str], reporter: Reporter) -> None:
    for rel in subdir_hook_files:
        reporter.warning(
            "hooks", rel, 1,
            "hooks.json em um subdiretório não é descoberto; somente arquivos "
            ".github/hooks/NAME.json no nível raiz são carregados",
        )
    for rel in hook_files:
        try:
            data = json.loads(read_text(rel))
        except json.JSONDecodeError as exc:
            reporter.error("hooks", rel, exc.lineno,
                           f"JSON inválido: {exc.msg}")
            continue
        if data.get("version") != 1:
            reporter.error(
                "hooks", rel, 1, f"a 'version' do gancho deve ser 1 (encontrado {data.get('version')!r})")
        hooks = data.get("hooks")
        if not isinstance(hooks, dict):
            reporter.error("hooks", rel, 1,
                           "o arquivo de gancho deve conter um objeto 'hooks'")
            continue
        for event, handlers in hooks.items():
            if event not in HOOK_EVENTS:
                reporter.error("hooks", rel, 1,
                               f"evento de gancho desconhecido: '{event}'")
            if not isinstance(handlers, list):
                reporter.error(
                    "hooks", rel, 1, f"o evento '{event}' deve mapear para uma lista de manipuladores")
                continue
            for handler in handlers:
                if not isinstance(handler, dict):
                    reporter.error("hooks", rel, 1,
                                   f"o evento '{event}' tem um manipulador que não é objeto")
                    continue
                handler_type = handler.get("type")
                if handler_type not in HOOK_TYPES:
                    reporter.error(
                        "hooks", rel, 1,
                        f"o manipulador do evento '{event}' tem o tipo {handler_type!r}; "
                        f"deve ser um de {', '.join(sorted(HOOK_TYPES))}",
                    )
                for shell_key in ("bash", "powershell"):
                    value = handler.get(shell_key)
                    if not value:
                        continue
                    script = value.split()[0]
                    script_path = REPO_ROOT / script
                    if not script_path.is_file():
                        reporter.error(
                            "hooks", rel, 1,
                            f"o script {shell_key} '{script}' do evento '{event}' não existe",
                        )
                    elif not os.access(script_path, os.X_OK):
                        reporter.error(
                            "hooks", rel, 1,
                            f"o script {shell_key} '{script}' do evento '{event}' não é executável",
                        )


# --- Estrutura e links de Markdown -----------------------------------------

H1_RE = re.compile(r"^ {0,3}#(?:[ \t].*)?$")
FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*([^)]*?)\s*\)")
REF_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")
URI_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")


def fence_mask(lines: list[str]) -> list[bool]:
    """Marca linhas de blocos de código cercados, de acordo com CommonMark.

    Um delimitador de fechamento deve repetir o caractere de abertura, ter pelo
    menos o mesmo comprimento e não conter uma string de informações. Isso evita
    que um delimitador interno ```lang (que tem uma string de informações) seja
    confundido com o fechamento de um bloco externo ```.
    """
    mask = [False] * len(lines)
    in_fence = False
    fence_char = ""
    fence_len = 0
    for i, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if not in_fence:
            if match:
                in_fence = True
                fence_char = match.group(2)[0]
                fence_len = len(match.group(2))
                mask[i] = True
        else:
            mask[i] = True
            if (
                match
                and match.group(2)[0] == fence_char
                and len(match.group(2)) >= fence_len
                and match.group(3).strip() == ""
            ):
                in_fence = False
                fence_char = ""
                fence_len = 0
    return mask


def frontmatter_end(lines: list[str]) -> int:
    """Índice da primeira linha após o frontmatter YAML, ou 0 se não houver."""
    if not lines or lines[0].strip() != "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1
    return 0


def iter_prose(rel: str):
    """Produz (número_da_linha, texto) somente para linhas de prosa.

    Linhas de blocos de código cercados são ignoradas e trechos de código inline
    são removidos, para que as verificações de política de conteúdo sinalizem
    ocorrências ativas/em prosa de um padrão proibido, em vez de exemplos citados
    dentro de código (documentação da própria regra).
    """
    lines = read_text(rel).split("\n")
    mask = fence_mask(lines)
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        yield i + 1, INLINE_CODE_RE.sub("", line)


def check_markdown_structure(rel: str, reporter: Reporter) -> None:
    data = read_bytes(rel)
    if not data.endswith(b"\n"):
        reporter.error("markdown-structure", rel, None,
                       "o arquivo deve terminar com exatamente uma quebra de linha")
    elif data.endswith(b"\n\n"):
        reporter.error("markdown-structure", rel, None,
                       "o arquivo tem mais de uma quebra de linha no final")

    lines = data.decode("utf-8", "replace").split("\n")
    mask = fence_mask(lines)
    start = frontmatter_end(lines)
    h1_lines = [
        offset + 1
        for offset in range(start, len(lines))
        if not mask[offset] and H1_RE.match(lines[offset])
    ]
    if len(h1_lines) == 0:
        reporter.error("markdown-structure", rel, None,
                       "o arquivo não tem título H1 (esperado: exatamente um)")
    elif len(h1_lines) > 1:
        reporter.error(
            "markdown-structure", rel, h1_lines[1],
            f"o arquivo tem {len(h1_lines)} títulos H1 (esperado: exatamente um); "
            f"H1 excedente na linha {h1_lines[1]}",
        )


def check_markdown_links(rel: str, reporter: Reporter) -> None:
    lines = read_text(rel).split("\n")
    mask = fence_mask(lines)
    base_dir = (REPO_ROOT / rel).parent
    for lineno, raw in enumerate(lines, start=1):
        if mask[lineno - 1]:
            continue
        line = INLINE_CODE_RE.sub("", raw)
        targets = list(LINK_RE.findall(line))
        ref_def = REF_DEF_RE.match(raw)
        if ref_def:
            targets.append(ref_def.group(1))
        for target in targets:
            _check_link_target(rel, lineno, target, base_dir, reporter)


def _check_link_target(rel: str, lineno: int, target: str, base_dir: Path, reporter: Reporter) -> None:
    target = target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:].split(">", 1)[0]
    elif target:
        target = target.split()[0]
    target = target.split("#", 1)[0]
    if not target:
        return
    if URI_SCHEME_RE.match(target) or target.startswith("//"):
        return
    if any(ch in target for ch in "{}<>$*"):
        return
    if target.startswith("/"):
        candidate = REPO_ROOT / target.lstrip("/")
    else:
        candidate = base_dir / target
    if not os.path.exists(os.path.normpath(candidate)):
        reporter.error(
            "referential-integrity", rel, lineno,
            f"link relativo quebrado '{target}' (é resolvido para um caminho inexistente)",
        )


# --- Verificações da estrutura do corpo das primitivas ----------------------
#
# O frontmatter informa ao carregador como conectar uma primitiva; as seções
# `## ` do corpo são o contrato lido por pessoas. As primitivas de referência
# (o agente archaeologist, os prompts de estágio/persona e as habilidades e instruções
# nativas) compartilham um esqueleto fixo de seções. Estas verificações transformam
# essa convenção em uma verificação, para que uma primitiva que omita silenciosamente
# "O que NÃO farei" ou "Critérios de qualidade" falhe de forma visível, em vez de
# divergir. As ocorrências ficam na categoria `primitive-structure`. Blocos de
# código cercados e frontmatter YAML são ignorados (pela mesma máscara de blocos
# e pelo mesmo detector de frontmatter usados em outros pontos), para que linhas
# `## ` em modelos de exemplo nunca sejam confundidas com seções reais do documento.

STRUCTURE_CHECK = "primitive-structure"

H2_RE = re.compile(r"^ {0,3}##(?!#)[ \t]+(.+?)[ \t]*$")
ATX_CLOSING_RE = re.compile(r"[ \t]+#+[ \t]*$")

# Agentes: somente presença. O archaeologist de referência coloca a seção de
# definição de pronto antes de "Prompts disponíveis", enquanto os agentes de
# persona a colocam depois; por isso, a ordem das seções não é imposta.
AGENT_REQUIRED_SECTIONS = [
    ("Missão", {"Missão"}),
    ("Personas líderes", {"Personas líderes"}),
    ("Princípios operacionais", {"Princípios operacionais"}),
    ("O que este agente sabe", {"O que este agente sabe"}),
    ("O que este agente NÃO sabe", {"O que este agente NÃO sabe"}),
    ("Prompts disponíveis", {"Prompts disponíveis"}),
    ("Antipadrões que este agente rejeita", {"Antipadrões que este agente rejeita"}),
]
# O archaeologist usa "Definição de pronto do Estágio 1"; agentes de persona
# usam apenas "Definição de pronto".
AGENT_DOD_TITLES = {"Definição de pronto"}
AGENT_DOD_PT_BR_PREFIX = "Definição de pronto do Estágio "
# É comum, mas não universal; portanto, a ausência gera aviso, não erro.
AGENT_RECOMMENDED_SECTIONS = [
    ("Integração com o Spec-Kit", {"Integração com o Spec-Kit"})
]

# Prompts: presença E ordem relativa canônica. Seções extras (por exemplo, um
# bloco "## Regras de <arquivo>" entre "Formato da saída" e "Definição de pronto")
# são permitidas e simplesmente ignoradas pela verificação de ordem.
PROMPT_REQUIRED_SECTIONS = [
    ("Objetivo", {"Objetivo"}),
    ("Quando usar", {"Quando invocar", "Quando usar"}),
    ("Pré-condições", {"Pré-condições"}),
    ("Entradas que a equipe deve fornecer", {"Entradas que a equipe deve fornecer"}),
    ("O que farei", {"O que farei"}),
    ("O que não farei", {"O que NÃO farei", "O que não farei"}),
    ("Formato da saída", {"Formato da saída"}),
    ("Definição de pronto", {"Definição de pronto"}),
    ("Corpo do prompt", {"Corpo do prompt"}),
    ("Exemplo de chamada", {"Exemplo de invocação", "Exemplo de chamada"}),
]

# Habilidades: comparação sem diferenciar maiúsculas de minúsculas, pois habilidades
# nativas usam caixa de frase, enquanto algumas importações usam caixa de título.
SKILL_REQUIRED_SECTIONS = [
    ("Quando usar", {"Quando usar", "Quando invocar"}),
    ("Modelo de saída", {"Modelo de saída"}),
    ("Critérios de qualidade", {"Critério de qualidade", "Critérios de qualidade"}),
]

# Instruções: somente presença, com correspondência exata do título.
INSTRUCTION_REQUIRED_SECTIONS = [
    ("Convenções", {"Convenções"}),
    ("Faça / Não faça", {"Faça / Não faça"}),
    ("Lista de verificação antes de abrir uma PR", {
        "Lista de verificação antes de abrir uma PR",
    }),
]


def h2_sections(rel: str) -> list[tuple[str, int]]:
    """Retorna (título, linha baseada em 1) para cada título ## real em um arquivo Markdown.

    Reutiliza a máscara de blocos cercados e o detector de frontmatter para que
    linhas ## dentro de blocos de exemplo ou do frontmatter YAML não sejam
    contabilizadas como seções.
    """
    lines = read_text(rel).split("\n")
    mask = fence_mask(lines)
    start = frontmatter_end(lines)
    sections: list[tuple[str, int]] = []
    for i in range(start, len(lines)):
        if mask[i]:
            continue
        heading = H2_RE.match(lines[i])
        if heading:
            title = ATX_CLOSING_RE.sub("", heading.group(1)).strip()
            sections.append((title, i + 1))
    return sections


def _report_missing_sections(
    rel: str,
    present: set[str],
    required: list[tuple[str, set[str]]],
    reporter: Reporter,
) -> None:
    for section, aliases in required:
        if present.isdisjoint(aliases):
            reporter.error(
                STRUCTURE_CHECK, rel, None, f"seção obrigatória ausente: '## {section}'"
            )


def check_agent_structure(rel: str, reporter: Reporter) -> None:
    titles = [title for title, _ in h2_sections(rel)]
    present = set(titles)
    _report_missing_sections(rel, present, AGENT_REQUIRED_SECTIONS, reporter)
    has_definition_of_done = any(
        title in AGENT_DOD_TITLES
        or (
            title.startswith("Stage ")
            and title.endswith(" Definition of Done")
        )
        or title.startswith(AGENT_DOD_PT_BR_PREFIX)
        for title in titles
    )
    if not has_definition_of_done:
        reporter.error(
            STRUCTURE_CHECK, rel, None,
            "seção obrigatória de definição de pronto ausente "
            "(por exemplo, '## Definição de pronto' ou "
            "'## Definição de pronto do Estágio 1')",
        )
    for section, aliases in AGENT_RECOMMENDED_SECTIONS:
        if present.isdisjoint(aliases):
            reporter.warning(
                STRUCTURE_CHECK, rel, None,
                f"seção recomendada ausente: '## {section}'",
            )


def check_prompt_structure(rel: str, reporter: Reporter) -> None:
    sections = h2_sections(rel)
    present = {title for title, _ in sections}
    _report_missing_sections(rel, present, PROMPT_REQUIRED_SECTIONS, reporter)

    # Verifica se as seções obrigatórias aparecem na ordem relativa canônica.
    # Percorre os títulos do documento e acompanha a seção obrigatória de maior
    # posição já vista; uma seção com posição menor aparece tarde demais e é
    # relatada em relação à seção que deveria ter antecedido.
    canonical = {
        alias: (index, name)
        for index, (name, aliases) in enumerate(PROMPT_REQUIRED_SECTIONS)
        for alias in aliases
    }
    highest_rank = -1
    highest_title: str | None = None
    seen: set[int] = set()
    for title, lineno in sections:
        if title not in canonical:
            continue
        rank, canonical_title = canonical[title]
        if rank in seen:
            continue
        seen.add(rank)
        if rank < highest_rank:
            reporter.error(
                STRUCTURE_CHECK, rel, lineno,
                f"a seção '## {canonical_title}' está fora de ordem: deve aparecer antes de "
                f"'## {highest_title}'",
            )
            return
        highest_rank = rank
        highest_title = canonical_title


def check_skill_structure(rel: str, reporter: Reporter) -> None:
    sections = h2_sections(rel)
    lower_titles = [title.lower() for title, _ in sections]
    for section, aliases in SKILL_REQUIRED_SECTIONS:
        lower_aliases = {alias.lower() for alias in aliases}
        if set(lower_titles).isdisjoint(lower_aliases):
            reporter.error(
                STRUCTURE_CHECK, rel, None, f"seção obrigatória ausente: '## {section}'"
            )
    # Uma habilidade em conformidade coloca pelo menos uma seção de procedimento entre
    # seu gatilho ("Quando usar") e seu "Modelo de saída". Uma distância de um
    # significa que os dois títulos são adjacentes (sem procedimento); isso gera aviso.
    trigger_aliases = {alias.lower() for alias in SKILL_REQUIRED_SECTIONS[0][1]}
    output_aliases = {alias.lower() for alias in SKILL_REQUIRED_SECTIONS[1][1]}
    first = next((i for i, title in enumerate(lower_titles) if title in trigger_aliases), None)
    last = next((i for i, title in enumerate(lower_titles) if title in output_aliases), None)
    if first is not None and last is not None:
        if last - first < 2:
            reporter.warning(
                STRUCTURE_CHECK, rel, sections[last][1],
                "não há seção de procedimento entre '## Quando usar' e "
                "'## Modelo de saída'; documente as etapas executadas pela habilidade",
            )


def check_instruction_structure(rel: str, reporter: Reporter) -> None:
    present = {title for title, _ in h2_sections(rel)}
    _report_missing_sections(
        rel, present, INSTRUCTION_REQUIRED_SECTIONS, reporter)


# --- Verificações de política do repositório --------------------------------

PRAGMA_RE = re.compile(r"<!--\s*markdownlint-disable")
# O evento é uma imersão. "hackath?on" também cobre a grafia incorreta "hackaton";
# uma regex anterior, `hackat[o]?on`, não correspondia a nenhuma das duas grafias.
EVENT_TERM_RE = re.compile(r"hackath?ons?|workshops?", re.IGNORECASE)
# Identificadores técnicos reais podem conter o termo sem nomear o evento.
EVENT_TERM_ALLOWED_RE = re.compile(
    r"serpro-workshop-fortaleza|workshop-gbb|software-gbb-workshops|workshop-datacorp|"
    r"workshop-legacy-modernization|team=workshop-XX"
)
STALE_RE = re.compile("|".join(re.escape(name) for name in STALE_PATHS))


def check_pragmas(markdown_files: list[str], reporter: Reporter) -> None:
    for rel in markdown_files:
        if rel in PRAGMA_ALLOWED_FILES or rel in POLICY_EXEMPT_FILES:
            continue
        for lineno, line in iter_prose(rel):
            if PRAGMA_RE.search(line):
                reporter.error(
                    "policy-pragma", rel, lineno,
                    "pragma inline do markdownlint é proibido; o arquivo "
                    ".markdownlint-cli2.jsonc da raiz é a fonte única da verdade",
                )


GLOBAL_INSTRUCTIONS = ".github/copilot-instructions.md"
GLOBAL_INSTRUCTIONS_MAX_LINES = 100


def check_global_instructions_size(reporter: Reporter) -> None:
    """Limita o arquivo de instruções do repositório: ele é injetado em toda solicitação."""
    if not (REPO_ROOT / GLOBAL_INSTRUCTIONS).is_file():
        return
    count = len(read_text(GLOBAL_INSTRUCTIONS).splitlines())
    if count > GLOBAL_INSTRUCTIONS_MAX_LINES:
        reporter.error(
            "global-instructions-size", GLOBAL_INSTRUCTIONS, count,
            f"{count} linhas excedem o limite de {GLOBAL_INSTRUCTIONS_MAX_LINES} linhas; "
            "este arquivo é carregado em toda solicitação ao Copilot. Mova regras específicas "
            "de caminhos para .github/instructions/*.instructions.md "
            "(consulte .github/PRIMITIVE-STANDARD.md)",
        )


def check_event_terminology(text_files: list[str], reporter: Reporter) -> None:
    for rel in text_files:
        if rel in TERMINOLOGY_EXEMPT_FILES:
            continue
        source = iter_prose(rel) if rel.lower().endswith(
            ".md") else _iter_all_lines(rel)
        for lineno, line in source:
            if EVENT_TERM_RE.search(EVENT_TERM_ALLOWED_RE.sub("", line)):
                reporter.error(
                    "policy-event-term", rel, lineno,
                    "chame o evento de imersão; \"workshop\", \"hackathon\" "
                    "e \"hackaton\" são proibidos",
                )


def check_stale_paths(text_files: list[str], reporter: Reporter) -> None:
    for rel in text_files:
        if rel in POLICY_EXEMPT_FILES:
            continue
        source = iter_prose(rel) if rel.lower().endswith(
            ".md") else _iter_all_lines(rel)
        for lineno, line in source:
            match = STALE_RE.search(line)
            if match:
                reporter.error(
                    "policy-stale-path", rel, lineno,
                    f"nome de diretório obsoleto '{match.group(0)}' (o repositório foi renomeado; "
                    "atualize para o caminho atual)",
                )


def _iter_all_lines(rel: str):
    for lineno, line in enumerate(read_text(rel).split("\n"), start=1):
        yield lineno, line


def check_competing_tools(markdown_files: list[str], reporter: Reporter) -> None:
    for rel in markdown_files:
        if rel in POLICY_EXEMPT_FILES:
            continue
        lines = read_text(rel).split("\n")
        mask = fence_mask(lines)
        for lineno, raw in enumerate(lines, start=1):
            if mask[lineno - 1]:
                continue
            _scan_competing_line(rel, lineno, raw, reporter)


def _scan_competing_line(rel: str, lineno: int, line: str, reporter: Reporter) -> None:
    for match in TOOL_RE.finditer(line):
        clause, tool_start = _recommendation_clause(line, match.start(), match.end())
        window = clause[max(0, tool_start - RECOMMEND_WINDOW):tool_start]
        if not RECOMMEND_VERB_RE.search(window):
            continue
        if NEGATION_RE.search(clause) or INTERROGATIVE_RE.search(clause):
            continue
        reporter.error(
            "policy-competing-tool", rel, lineno,
            f"parece recomendar '{match.group(1)}'; somente a cadeia de ferramentas "
            "aprovada (VS Code + GitHub Copilot) pode ser recomendada",
        )
        return


def _recommendation_clause(line: str, start: int, end: int) -> tuple[str, int]:
    """Isola a oração que contém a ferramenta e retorna seu deslocamento local."""
    cuts = _clause_cuts(line)
    left = max(position for position in cuts if position <= start)
    right = min(position for position in cuts if position >= end)
    return line[left:right], start - left


def _clause_cuts(line: str) -> list[int]:
    cuts = {0, len(line)}
    for index, character in enumerate(line):
        if character in HARD_CLAUSE_BOUNDARIES:
            cuts.add(index + 1)
        elif character == "." and _is_sentence_period(line, index):
            cuts.add(index + 1)
    cuts.update(match.end() for match in CONTRAST_BOUNDARY_RE.finditer(line))
    return sorted(cuts)


def _is_sentence_period(line: str, index: int) -> bool:
    next_index = index + 1
    if index > 0:
        initial = line[index - 1].lower()
        remainder = line[next_index:]
        if initial == "p" and re.match(r"\s*ex\.", remainder, re.IGNORECASE):
            return False
    if next_index < len(line) and not line[next_index].isspace():
        return False
    if index > 0 and next_index < len(line):
        if line[index - 1].isdigit() and line[next_index].isdigit():
            return False
    token_match = re.search(r"([A-Za-zÀ-ÿ.]+)$", line[:index])
    token = token_match.group(1).lower() if token_match else ""
    if token == "etc":
        following = line[next_index:].lstrip()
        return not following or following[0].isupper()
    return token not in PERIOD_ABBREVIATIONS


# --- Seletores de conjuntos de arquivos ------------------------------------

def match(rel: str, pattern: str) -> bool:
    return re.match(pattern, rel) is not None


def main() -> int:
    reporter = Reporter()
    # Um checkout novo da CI materializa todos os arquivos versionados, mas uma
    # árvore local pode listar arquivos que uma renomeação concorrente deixou no
    # índice, embora não existam no disco. Restringe aos arquivos existentes para
    # que a verificação nunca falhe ao tentar acessá-los.
    files = [f for f in tracked_files() if (REPO_ROOT / f).is_file()]

    agent_files = [f for f in files if match(
        f, r"\.github/agents/[^/]+\.agent\.md$")]
    prompt_files = [f for f in files if match(
        f, r"\.github/prompts/[^/]+\.prompt\.md$")]
    instruction_files = [f for f in files if match(
        f, r"\.github/instructions/[^/]+\.instructions\.md$")]
    skill_files = [f for f in files if match(
        f, r"\.github/skills/[^/]+/SKILL\.md$")]
    hook_files = [f for f in files if match(f, r"\.github/hooks/[^/]+\.json$")]
    subdir_hook_files = [f for f in files if match(
        f, r"\.github/hooks/[^/]+/.+/?hooks\.json$")]
    github_markdown = [f for f in files if f.startswith(
        ".github/") and f.lower().endswith(".md")]
    all_markdown = [f for f in files if f.lower().endswith(".md")]
    text_files = [
        f for f in files
        if not looks_binary(read_bytes(f))
    ]

    valid_agent_ids = build_agent_registry(agent_files, reporter)

    check_agents(agent_files, reporter)
    check_prompts(prompt_files, valid_agent_ids, reporter)
    check_instructions(instruction_files, reporter)
    check_skills(skill_files, reporter)
    check_handoffs(agent_files, valid_agent_ids, reporter)

    check_hooks(hook_files, subdir_hook_files, reporter)

    for rel in github_markdown:
        # Os modelos de solicitação, alteração e discussão do GitHub intencionalmente não têm
        # H1: o `name:` do frontmatter fornece o título renderizado pelo GitHub.
        # Seus links ainda são verificados.
        if not match(rel, r"\.github/(ISSUE_TEMPLATE|PULL_REQUEST_TEMPLATE|DISCUSSION_TEMPLATE)(/|\.md$)"):
            check_markdown_structure(rel, reporter)
        check_markdown_links(rel, reporter)

    check_pragmas(all_markdown, reporter)
    check_global_instructions_size(reporter)
    check_event_terminology(text_files, reporter)
    check_stale_paths(text_files, reporter)
    check_competing_tools(all_markdown, reporter)

    reporter.summarize()

    counts = (
        f"agentes={len(agent_files)} prompts={len(prompt_files)} "
        f"instruções={len(instruction_files)} habilidades={len(skill_files)} "
        f"ganchos={len(hook_files)} markdown-github={len(github_markdown)}"
    )
    print(f"Verificados: {counts}")
    return 1 if reporter.error_count else 0


if __name__ == "__main__":
    sys.exit(main())
