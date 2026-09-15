# Padrão de primitivas do Copilot

`.github/` contém as **primitivas** do Copilot deste kit: agentes, prompts, instruções, skills e hooks. Este arquivo é o padrão escrito e citável para a estrutura de cada uma delas. Assim, uma nova primitiva pode corresponder ao conjunto existente sem engenharia reversa. A referência de excelência definida pela equipe é o agente archaeologist ([`archaeologist.agent.md`](agents/archaeologist.agent.md)); os padrões abaixo derivam dele e de seus pares.

> [!IMPORTANT]
> O guia de estilo da documentação ([`../docs/DOC-STYLE-GUIDE.md`](../docs/DOC-STYLE-GUIDE.md), regra R4) rege deliberadamente **somente** `docs/` e as pastas numeradas dos estágios, nunca `.github/`. As primitivas do Copilot seguem *este* padrão. Portanto, uma revisão de documentação não deve reestruturar uma primitiva como prosa.

## O modelo de harness

Uma primitiva é uma superfície do harness de agentes do repositório. O modelo usado pelo kit é:

```text
Suporte = Instruções + Restrições + Retorno + Memória + Avaliação + Governança
```

| Camada | Primitiva que a contém |
|---|---|
| Instruções | `copilot-instructions.md`, `instructions/*.instructions.md` |
| Restrições | `hooks/*.json` que bloqueiam uma chamada de ferramenta; escopo `applyTo` das instruções |
| Retorno | prompts e agentes que executam verificações e informam os resultados |
| Memória | ADRs, especificações, testes e histórico Git mantidos pelo time |
| Avaliação | `workflows/spec-quality.yml` mais `scripts/validate-copilot-primitives.py` |
| Governança | este padrão, imposto pelo job de CI `copilot-primitives` |

Prefira atualizar uma primitiva existente em vez de adicionar outra quase duplicada.

Os [metadados de idioma](language.json) identificam a edição em português do Brasil deste kit. Adaptar a prosa nunca altera os schemas do frontmatter nem identificadores técnicos.

## Regras aplicáveis a todas as primitivas

### Markdown e estilo

- [ ] Português do Brasil na edição `portugues-br`, incluindo a prosa das primitivas. Respeite o [escopo do kit dos participantes](../README.md), preservando caminhos, identificadores e schemas. Mantenha os nomes técnicos oficiais. Não use emojis; comunique NOTE, TIP, IMPORTANT, WARNING e CAUTION com alertas GFM como `> [!NOTE]`.
- [ ] Exatamente um H1 (`#`) por arquivo: o título do documento, abaixo do frontmatter. O validador de primitivas impõe esta regra; a MD025 do markdownlint (vários títulos de nível superior) está desativada.
- [ ] A linha em branco entre o `---` de fechamento e o H1 é opcional, e as duas formas passam no lint: agentes, prompts e skills a omitem, enquanto os arquivos de instruções a mantêm. A MD022 não dispara no limite do frontmatter e não é sobrescrita. Siga os arquivos vizinhos no mesmo diretório em vez de forçar um diff sem outra finalidade.
- [ ] Nunca pule um nível de título; use `#`, depois `##` e então `###`.
- [ ] Todo bloco de código cercado declara uma linguagem (por exemplo, `java`, `json`, `text` ou `bash`). Esta é uma convenção interna mantida na revisão, pois a MD040 do markdownlint está desativada.
- [ ] Use tabelas GFM reais (com a linha separadora `|---|`) sempre que houver duas ou mais dimensões e checklists `- [ ]` para tudo que a pessoa leitora precisar verificar.
- [ ] Termine com exatamente uma quebra de linha. Não use espaços ao fim da linha, tabs rígidos nem linhas em branco consecutivas.
- [ ] Nunca desative uma regra do markdownlint inline com um pragma em comentário HTML (falha nº 2). O arquivo [`../.markdownlint-cli2.jsonc`](../.markdownlint-cli2.jsonc) da raiz é a única configuração de lint. Um pragma inline a duplica e consome tokens da janela de contexto sem valor instrutivo. Os pragmas removidos de 158 arquivos desativavam exatamente as regras que essa configuração já desativa: redundância que não alterava nada e somente consumia tokens.

### Conteúdo e precisão

- [ ] **Cite a fonte autoritativa de cada convenção**; não a repita a partir do resumo em `copilot-instructions.md`. Os nomes de branches vêm de [`../00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md); as regras de leitura do legado, de [`instructions/natural-adabas.instructions.md`](instructions/natural-adabas.instructions.md); EARS e `source_legacy`, de [`skills/ears-validate/SKILL.md`](skills/ears-validate/SKILL.md).
- [ ] **Prefixos de branch** (tabela autoritativa em [`../00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md)): `spec/<NNN>-<feature>`, `impl/<NNN>-<feature>`, `infra/<component>`, `docs/<topic>` e `agent/<issue-NN>`, todos criados a partir de `develop`. Nunca transforme `impl/` em `spec/` (falha nº 1).
- [ ] **Nunca invente fatos sobre o SIFAP.** Uma primitiva ensina *como descobrir* o comportamento legado; nunca declara qual é uma regra de negócio. O corpus em `01-archaeology/legacy-sifap/` possui 24 membros Natural (12 `.NSP`, 5 `.NSN`, 2 `.NSC`, 2 `.NSA`, 1 `.NSL`, 2 `.jcl`), 4 DDMs `.ddm` e 1 listagem FDT `.txt`. Não existe arquivo `.NSD`.
- [ ] **Somente a cadeia de ferramentas aprovada.** Nunca recomende, instale nem migre para Cursor, Windsurf, Codex, Cline, Continue, Aider, Codeium, Tabnine, IntelliJ, Eclipse ou Neovim; VS Code com GitHub Copilot é o único editor e assistente aprovado.
- [ ] Chame o evento de imersão, nunca de `workshop` ou `hackathon`.
- [ ] Use somente os paths atuais em inglês; os nomes aposentados de diretórios em português são rejeitados pela verificação de paths obsoletos do validador (falha nº 5). `backend/`, `frontend/` e `infra/` **ainda não** existem; a equipe os cria nos Estágios 3 e 4 conforme o recorte selecionado.

## Frontmatter por tipo de primitiva

O frontmatter possui um schema fechado para cada tipo: uma chave desconhecida, aposentada ou inválida **reprova no portão `copilot-primitives`**. Chaves marcadas como específicas de plataforma são ignoradas silenciosamente em outras superfícies e podem ser mantidas. Coloque os valores de string de `name` e `description` entre aspas, conforme a convenção interna seguida atualmente por todos os agentes, prompts, instruções e skills do kit.

### Frontmatter de agente

Arquivo: `agents/<id>.agent.md`.

| Chave | Observações |
|---|---|
| `name` | ID do agente; presente por convenção. Renomear um agente quebra silenciosamente todo prompt vinculado a ele por `agent:`. |
| `description` | A única chave estritamente exigida pelo portão. |
| `tools` | Por exemplo, `[read, search, edit]`; adicione `execute` ou `"github/*"` somente quando necessário. |
| `model` | Opcional. |
| `handoffs` | Somente agentes de estágio (e somente no VS Code). Agentes de persona nunca a usam. |
| `target`, `user-invocable`, `disable-model-invocation`, `metadata`, `agents` | Opcionais. |
| `mcp-servers` | Somente GitHub.com e CLI. |
| `argument-hint` | Somente VS Code. |

A chave `infer:` foi aposentada; remova-a.

> [!NOTE]
> Somente os agentes sequenciais de **estágio** possuem a chave `handoffs`, e apenas quando existe um próximo estágio: `archaeologist -> architect -> builder` passam o trabalho ao próximo, enquanto o agente terminal do Estágio 4 (`evolution`) não possui transição. Nenhum agente de persona possui `handoffs`.

### Frontmatter de prompt

Arquivo: `prompts/<name>.prompt.md`. O nome do comando slash deriva do nome do arquivo, salvo quando `name:` o sobrescreve. Chaves válidas: `name`, `description`, `agent`, `model`, `tools`, `argument-hint`.

- `agent:` deve resolver para um agente integrado (`ask`, `agent` ou `plan`) ou para um arquivo em `agents/`.
- `mode:` está obsoleta (sintaxe antiga de modo de chat, substituída por `agent:`); remova-a.
- `tested_with:` foi inventada e não produz efeito; remova-a.

### Frontmatter de instrução

Arquivo: `instructions/<name>.instructions.md`. Chaves válidas: `applyTo`, `name`, `description`, `excludeAgent`.

- Limite `applyTo` a globs concretos. `applyTo: "**"` injeta o arquivo em toda solicitação e **reprova no portão**; vários arquivos disputando um path como `**/*.tf` causaram a falha nº 6.

### Instruções para todo o repositório (`copilot-instructions.md`)

Este arquivo **não possui frontmatter** e é injetado em toda solicitação de Chat, agente e revisão de código em cada superfície. Portanto, cada linha gera um custo recorrente de tokens. Mantenha-o com **até 100 linhas**.

- Coloque aqui somente conteúdo **amplamente aplicável**: contexto do projeto, stack-alvo, regras transversais e lista rígida de proibições. A orientação do GitHub é que as instruções sejam "declarações curtas e autocontidas".
- **Não repita regras específicas de linguagem ou path.** Arquivos com escopo por path existem para "evitar sobrecarregar as instruções de todo o repositório". Detalhes de Java, TypeScript, Terraform, banco de dados e segurança pertencem a `instructions/*.instructions.md`, carregados automaticamente nos paths correspondentes.
- Mantenha aqui a **declaração da stack**, embora os arquivos com escopo a repitam: não está documentado se `applyTo` corresponde a um diretório que ainda não existe, e `backend/` e `frontend/` são criados somente no Estágio 3.
- Evite os antipadrões documentados: instruções para ler outro documento, roteamento por ferramenta ou extensão, imposições de tom e limites de tamanho de resposta.

### Frontmatter de skill

Arquivo: `skills/<dir>/SKILL.md`. Somente `name` e `description` são válidas.

- `name` **deve ser exatamente igual ao nome do diretório pai** (letras minúsculas, dígitos e hifens; no máximo 64 caracteres), ou a skill deixa de carregar silenciosamente (falha nº 4).
- `description` deve informar **quando usar** a skill, pois controla o carregamento automático semântico, e possui limite de 1.024 caracteres.
- `license`, `allowed-tools`, `compatibility` e `metadata` **não** pertencem ao schema; remova-as.

### Configuração de hook

Um hook é um arquivo JSON plano em `hooks/<name>.json`. Um `<name>/hooks.json` aninhado **nunca é descoberto** nem executado (falha nº 3). O script manipulador fica em `hooks/<name>/` e deve ser executável.

- `version` deve ser `1`; `hooks` mapeia um evento para uma lista de manipuladores.
- Os eventos incluem `sessionStart`, `sessionEnd`, `userPromptSubmitted`, `preToolUse` e `postToolUse`. O `type` de um manipulador é `command`, `http` ou `prompt`.

Um hook `preToolUse` bloqueia uma chamada de ferramenta ao escrever este objeto em stdout:

```json
{"permissionDecision":"deny","permissionDecisionReason":"..."}
```

## Seções obrigatórias do corpo

A estrutura das seções é verificada por `scripts/validate-copilot-primitives.py`. Use estes títulos, na ordem indicada.

| Primitiva | Seções `##` obrigatórias, na ordem |
|---|---|
| Agente | `Missão`, `Personas líderes`, `Princípios operacionais`, `O que este agente sabe`, `O que este agente NÃO sabe`, `Prompts disponíveis`, um título terminado em `Definição de pronto`, `Antipadrões que este agente rejeita`, `Integração com o Spec-Kit` |
| Prompt | `Objetivo`, `Quando invocar`, `Pré-condições`, `Entradas que a equipe deve fornecer`, `O que farei`, `O que NÃO farei`, `Formato da saída`, `Regras de <arquivo>` opcional, `Definição de pronto`, `Corpo do prompt`, `Exemplo de invocação` |
| Instrução | seções de tópicos concretos, depois `Convenções`, `Faça / Não faça`, `Lista de verificação antes de abrir uma PR` |
| Skill | `Quando invocar`, uma seção de procedimento substancial, `Modelo de saída`, `Portão de qualidade` |

## Esqueletos

Copie um esqueleto, mantenha o frontmatter e a ordem das seções e substitua todos os placeholders entre sinais de maior e menor.

### Esqueleto de agente

````markdown
---
name: "<agent-id>"
description: "Assistente de <Estágio N ou Persona> — uma linha"
tools: [read, search, edit]
# handoffs:                 # Somente agentes de estágio e apenas se houver próximo estágio
#   - label: "Iniciar o Estágio <N+1>"
#     agent: <next-agent-id>
#     prompt: "<o que o próximo agente faz com os artefatos deste estágio>"
#     send: false
---
# @<agent-id>-agent

## Missão

<O que o agente ajuda a equipe a fazer e o limite que não ultrapassará.>

## Personas líderes

| Papel | Envolvimento |
|------|-----------|
| **<Persona>** | LÍDER — <responsabilidade> |

## Princípios operacionais

- **<Princípio>.** <Uma ou duas frases de julgamento ou encaminhamento.>

## O que este agente sabe

<Padrões gerais e transferíveis, nunca respostas específicas do sistema.>

## O que este agente NÃO sabe

<Tudo que deve emergir da própria investigação da equipe.>

## Prompts disponíveis

| Comando | Finalidade |
|---------|---------|
| [`/<command>`](../prompts/<file>.prompt.md) | <finalidade> |

## Definição de pronto

- [ ] <resultado verificável>

## Antipadrões que este agente rejeita

1. **<Antipadrão>.** <Por que ele é rejeitado e qual é o encaminhamento.>

## Integração com o Spec-Kit

<Onde o agente atua no fluxo /speckit.*.>
````

Um agente de estágio pode prefixar o antepenúltimo título com seu estágio, por exemplo, `## Definição de pronto do Estágio 1`.

### Esqueleto de prompt

`## Corpo do prompt` é Markdown simples dirigido ao agente na segunda pessoa, nunca um bloco de código. Comece com uma linha de papel como `Você é o @<agent-id>.` e conduza o trabalho com títulos de etapa em negrito, como `**Etapa 1 — ...**` e `**Etapa 2 — ...**`, cada um seguido por itens.

````markdown
---
name: "<slash-command>"
description: "<uma linha>"
argument-hint: "<arg=... arg=...>"
agent: "<agent-id>"
tools: ["read", "search", "edit"]
---
# /<slash-command>

## Objetivo

<O único resultado produzido por este prompt.>

## Quando invocar

## Pré-condições

## Entradas que a equipe deve fornecer

## O que farei

## O que NÃO farei

## Formato da saída

```markdown
<o formato exato que o prompt acrescenta ou emite>
```

## Definição de pronto

- [ ] <resultado verificável>

## Corpo do prompt

Você é o `@<agent-id>`. <Enquadramento da tarefa em uma linha.>

**Etapa 1 — <ação>**

- <instrução>

**Etapa 2 — <ação>**

- <instrução>

## Exemplo de invocação

```text
/<slash-command> arg=<value>
```
````

Quando o prompt depender de uma instrução ou skill, adicione uma seção opcional `## Regras de <arquivo>` que incorpore as regras aplicadas, imediatamente antes de `## Definição de pronto`.

### Esqueleto de instrução

````markdown
---
description: "Use quando <situação delimitada por este arquivo>."
applyTo: "<glob>,<glob>"
---

# <Tópico> — Guia

<Um parágrafo: o que ativa este arquivo, o que ele abrange e qual instrução vizinha é responsável pelo restante.>

## <Tópico concreto>

<Orientação com exemplos.>

## Convenções

| Regra | Justificativa |
|---|---|
| <regra> | <motivo> |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| <faça> | <não faça> |

## Lista de verificação antes de abrir uma PR

- [ ] <item verificável>
````

### Esqueleto de skill

`name` deve ser igual ao nome do diretório `skills/<dir>/`.

````markdown
---
name: "<dir>"
description: "Use quando <gatilho>. Os gatilhos incluem \"<palavra-chave>\", \"<palavra-chave>\"."
---
# <Título da skill>

## Quando invocar

- "<paráfrase de uma solicitação que deve carregar esta skill>"

## <Procedimento substancial>

<Um checklist, uma tabela ou etapas numeradas: o núcleo operacional.>

## Modelo de saída

```markdown
<o formato produzido pela skill>
```

## Portão de qualidade

- [ ] <verificação objetiva de aprovação/reprovação>
````

### Esqueleto de hook

Arquivo plano `hooks/<name>.json`, com o script referenciado em `hooks/<name>/` e marcado como executável.

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "type": "command",
        "bash": ".github/hooks/<name>/<script>.sh",
        "cwd": ".",
        "env": { "MODE": "block" },
        "timeoutSec": 10
      }
    ]
  }
}
```

## Como o padrão é imposto

- O job **`copilot-primitives`** em [`workflows/spec-quality.yml`](workflows/spec-quality.yml) executa [`scripts/validate-copilot-primitives.py`](scripts/validate-copilot-primitives.py): schemas de frontmatter, integridade de `prompt -> agent` e `handoff -> agent`, um H1, uma única quebra de linha final, resolução de links relativos em `.github/`, pragmas e ferramentas proibidos, paths obsoletos e as seções obrigatórias acima.
- O job **`markdown-lint`** executa o arquivo [`../.markdownlint-cli2.jsonc`](../.markdownlint-cli2.jsonc) da raiz; **`spec-traceability`** e **`legacy-traceability`** impõem a cobertura de REQ-ID e `source_legacy`.
- Essa configuração desativa `MD025` e `MD040`, entre outras. Não confunda os dois portões: "exatamente um H1" reprova no validador de primitivas, nunca no markdownlint; "todo bloco cercado declara uma linguagem" é uma convenção de revisão, não uma falha de lint.
- Todo erro recorrente recebe uma proteção nomeada no código ou na CI e, quando altera uma decisão durável, um ADR. Postmortems do facilitador e materiais de resposta permanecem fora deste repositório público.

Implementações de referência para copiar: [`agents/archaeologist.agent.md`](agents/archaeologist.agent.md), [`prompts/stage-archaeologist-extract-business-rules.prompt.md`](prompts/stage-archaeologist-extract-business-rules.prompt.md), [`skills/ears-validate/SKILL.md`](skills/ears-validate/SKILL.md) e [`instructions/modular-monolith.instructions.md`](instructions/modular-monolith.instructions.md).

## Lista de verificação de autoria

- [ ] A primitiva está na pasta correta, com o sufixo correto (`.agent.md`, `.prompt.md`, `.instructions.md`, `SKILL.md` ou um `hooks/<name>.json` plano).
- [ ] O frontmatter usa somente chaves válidas, sem chaves aposentadas (`infer`, `mode`) ou inventadas (`tested_with`), e o `name` da skill é igual ao seu diretório.
- [ ] Todas as seções obrigatórias estão presentes e na ordem.
- [ ] Há exatamente um H1, nenhum nível de título foi pulado, todo bloco cercado possui linguagem, há uma quebra de linha final e não existe pragma do markdownlint.
- [ ] Toda convenção cita seu documento autoritativo; não há fatos inventados sobre o SIFAP nem ferramentas proibidas; o conteúdo está em português do Brasil e sem emojis.
- [ ] Todo link relativo resolve para um arquivo no disco.
- [ ] `python3 .github/scripts/validate-copilot-primitives.py` e `npx markdownlint-cli2 "<file>"` informam zero problemas.
