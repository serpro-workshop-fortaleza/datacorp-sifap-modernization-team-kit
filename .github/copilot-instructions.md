# Instruções do GitHub Copilot — Imersão de modernização de legado

> Estas instruções informam ao Copilot o que sua equipe está criando, qual stack usar,
> quais convenções seguir e o que NÃO fazer. Elas se aplicam a todo o repositório da
> equipe.

## Ferramentas aprovadas — somente estas

Esta imersão usa uma **cadeia de ferramentas fixa**: VS Code, GitHub Copilot (modos Ask + Plan + Agent), GitHub Spec-Kit, GitHub, Docker / Docker Compose e Terraform. Outros assistentes de IA, IDEs, interfaces de chat web e frameworks de SDD não são permitidos, pois misturar ferramentas quebra a rastreabilidade entre especificação, código e teste. Tabela completa: [`README.md`](../README.md).

## Contexto do projeto

Modernização do sistema legado Natural/Adabas **SIFAP** (Sistema de Fiscalização e Administração de Pagamentos), com 29 anos, para Java 21 + Next.js 15. O código legado está em [`01-archaeology/legacy-sifap/`](../01-archaeology/legacy-sifap/): 24 membros Natural, 4 DDMs `.ddm` e 1 listagem FDT. O README de [`natural-programs/`](../01-archaeology/legacy-sifap/natural-programs/README.md) documenta a divisão entre 15 atribuídos e 9 de apoio.

O kit usa **duas camadas de agentes** (um kit de persona por pessoa + um agente de estágio por equipe). Consulte [`06-stage-agents/README.md`](../06-stage-agents/README.md) para obter detalhes.

Use as skills em [`.github/skills/`](skills/) para fluxos de trabalho especializados. O Copilot seleciona a skill pertinente por sua descrição; não duplique fluxos especializados nestas instruções globais.

## Escopo e idioma do kit

- Este kit é exclusivo dos participantes: guias, modelos, primitivas do Copilot e fontes locais para os exercícios. Não inclua portal de documentação, apresentações do instrutor, demonstrações prontas, gabaritos ou soluções de referência.
- A edição publicada está em português do Brasil na branch `portugues-br`. Mantenha esse idioma na documentação e na prosa das primitivas desta edição.
- Preserve caminhos técnicos, identificadores e fontes legadas. Não crie links para branches ou edições de idioma que não existem neste repositório.
- Não publique endereços, credenciais nem instruções de acesso ou operação dos ambientes do instrutor. Os participantes constroem e documentam a própria solução durante a imersão.

## Stack-alvo

- **Backend:** Java 21 + Spring Boot 3.3 + JPA/Hibernate + PostgreSQL 16
- **Frontend:** Next.js 15 (App Router) + TypeScript 5 (strict) + Tailwind CSS + shadcn/ui
- **Contêineres:** Docker + Docker Compose criados pela equipe nos Estágios 3/4 quando necessário
- **IaC:** Terraform (Azure provider ~> 3.x)
- **CI/CD:** GitHub Actions
- **Testes:** JUnit 5 + Testcontainers (backend); Vitest + Testing Library (frontend)

## Regras transversais de implementação

As regras detalhadas de Java, TypeScript, banco de dados, segurança, infraestrutura e testes ficam em [`.github/instructions/`](instructions/) e são carregadas automaticamente para os paths correspondentes.

- Use nomes de classes em inglês e comentários em português do Brasil.
- Defina os paths das APIs REST como `/api/v1/{resource}`.
- Valide entradas em todos os limites do sistema.
- Nunca codifique diretamente segredos, chaves de API ou credenciais.
- Nunca exponha dados sensíveis (CPF, valores de benefícios) em logs; mascare-os.
- Configure o CORS explicitamente; não use o curinga `*` em produção.
- Use Managed Identity para autenticação serviço a serviço no Azure.
- Escreva testes durante a implementação, não depois.

## Desenvolvimento orientado por especificações (Spec-Kit)

- Todo requisito usa a **notação EARS** (Easy Approach to Requirements Syntax).
- Todo requisito possui um **REQ-ID** exclusivo no formato `REQ-NNN`.
- **Todo requisito inclui uma linha `source_legacy:`** que aponta para arquivos legados ou contém `[GREENFIELD] + justificativa.`
  Use `01-archaeology/legacy-sifap/natural-programs/*.{NSP,NSN,NSS,NSA,NSL,NSC,NSM,jcl}` ou `01-archaeology/legacy-sifap/adabas-ddms/*.{NSD,ddm,txt}` para requisitos fundamentados no legado.
  O job de CI `legacy-traceability` rejeita PRs que violam esta regra. Consulte [`01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md`](../01-archaeology/LEGACY-EXPLORATION-CHECKLIST.md).
- Os testes são rastreados até os REQ-IDs por comentários inline.
- Estratégia de branches: um prefixo por persona/estágio, sempre criado a partir de `develop` (nunca de `spec/*`) e integrado de volta em `develop` → `main`; não existe branch `stage`.
  - `spec/<NNN>-<feature>` — Especialista em Requisitos + Arquiteto de Software, Estágio 2
  - `impl/<NNN>-<feature>` — Pessoa Desenvolvedora + Administrador de Banco de Dados + Engenheiro de Qualidade, Estágio 3
  - `infra/<component>` — Engenheiro DevOps, Estágio 4
  - `docs/<topic>` — Redator Técnico
  - `agent/<issue-NN>` — Copilot Agent
  - Não transforme `impl/`, nem qualquer outro prefixo, em `spec/`.
  - Tabela completa por persona: [`00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md)
- Antes de escrever requisitos EARS no Estágio 2, a dupla DEVE ter lido os programas Natural atribuídos (PORTÃO RÍGIDO; consulte o checklist acima).

## Regras rígidas — não faça isto

- Não presuma um protótipo de aplicação preexistente, uma conteinerização herdada nem infraestrutura da imersão. `backend/`, `frontend/` e `infra/` ainda não existem; a equipe cria apenas o necessário para o recorte selecionado nos Estágios 3 e 4. Os fontes locais são insumos para leitura e rastreabilidade, não um laboratório para implantar ou administrar.
- Não escreva um requisito EARS sem `source_legacy:`; a CI rejeitará a PR.
- Não adicione dependências sem justificativa em um ADR.
- Não escreva testes depois; escreva-os durante a implementação.
- Não exponha segredos em mensagens de commit, logs ou descrições de PR.
- Não faça merge em `main` sem ao menos uma revisão por pares.
- Não pule as conversas orientadas de transição durante as mudanças de estágio (consulte [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md)).
- Não crie `AGENTS.md`, `CLAUDE.md` ou `GEMINI.md` na raiz. Este arquivo é a fonte única de verdade para instruções de agentes em todo o repositório; toda superfície do Copilot que lê `AGENTS.md` também lê este arquivo, que possui precedência. Um segundo arquivo somente aumenta o risco de desvio. Consulte [`docs/adr/0001-agent-instructions-single-source-of-truth.md`](../docs/adr/0001-agent-instructions-single-source-of-truth.md).
- Não adicione nem edite uma primitiva do Copilot (agente, prompt, instrução, skill ou hook) que não siga [`PRIMITIVE-STANDARD.md`](PRIMITIVE-STANDARD.md); o job de CI `copilot-primitives` impõe sua estrutura.

## Referências

- Cronograma + duplas: [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md)
- Fluxo de trabalho Git: [`00-GIT-WORKFLOW.md`](../00-GIT-WORKFLOW.md)
- Três modos do Copilot (Ask · Plan · Agent): [`09-cheat-sheets/copilot-3-modes.md`](../09-cheat-sheets/copilot-3-modes.md)
- Kits de persona (leia 2 por pessoa; os artefatos ativos já estão consolidados em `.github/`): [`05-personas/`](../05-personas/)
- Agentes de estágio: [`06-stage-agents/`](../06-stage-agents/)
- Sistema legado SIFAP: [`01-archaeology/legacy-sifap/`](../01-archaeology/legacy-sifap/)
- SDD com Spec-Kit: <https://github.com/github/spec-kit>
