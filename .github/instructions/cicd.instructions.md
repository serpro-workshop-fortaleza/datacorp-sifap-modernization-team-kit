---
description: "Use ao criar ou revisar GitHub Actions, workflows de CI/CD, portões de pipeline YAML, verificações de build e automação de implantação."
applyTo: ".github/workflows/**,.github/actions/**,**/action.yml,**/action.yaml"
---

# Convenções de CI/CD — Portões do GitHub Actions

Este arquivo é ativado quando você edita workflows em `.github/workflows/`, actions compostas em `.github/actions/` ou qualquer `action.yml`/`action.yaml`. Ele ensina a estruturar o pipeline, fixar actions, delimitar permissões e manter os portões confiáveis. Os dois workflows ativos, [`ci.yml`](../workflows/ci.yml) e [`spec-quality.yml`](../workflows/spec-quality.yml), são a referência; leia-os antes de alterar um portão.

## Portões ativos

| Workflow · Job | O que impõe | Bloqueante? |
|---|---|---|
| `ci.yml` · `detect-changes` | `dorny/paths-filter` define outputs de `backend`/`frontend`/`infra` para que os jobs posteriores executem somente em mudanças pertinentes | n/a |
| `ci.yml` · `natural-format` | Falha quando o código Natural usa declarações de formato decimal com vírgula, como `(P9,2)`, em vez do formato com ponto `(P9.2)` do Natural CE | Sim |
| `ci.yml` · `backend` | JDK 21 (temurin) + `./mvnw -B verify`; envia o relatório Jacoco | Sim |
| `ci.yml` · `frontend` | pnpm 9 + Node 20; `pnpm lint`, `pnpm typecheck`, `pnpm test --run --coverage` | Sim |
| `ci.yml` · `infra` | `terraform fmt -check -recursive`, depois `init -backend=false` + `validate` por módulo | Sim |
| `spec-quality.yml` · `markdown-lint` | `markdownlint-cli2` em `**/*.md` | Sim |
| `spec-quality.yml` · `spec-traceability` | Informa REQ-IDs em `specs/` ainda não referenciados por um teste (emite `::warning::`) | Não |
| `spec-quality.yml` · `legacy-traceability` | Todo REQ-ID em `specs/` deve possuir uma linha `source_legacy:` válida | Sim |

> [!IMPORTANT]
> `legacy-traceability` reprova o build; `spec-traceability` somente alerta. Consulte [`requirements.instructions.md`](requirements.instructions.md) para ver o formato exato de `source_legacy:` aceito pelo portão.

## Fixe toda action pelo SHA do commit

Referencie actions pelo SHA completo de 40 caracteres do commit, com a tag legível em um comentário ao fim. Tags são mutáveis; SHAs não.

```yaml
# Correto — referência imutável
- uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
# Errado — uma tag pode ser movida para código malicioso
- uses: actions/checkout@v6
```

## Permissões de privilégio mínimo

Declare `permissions` no início de todo workflow com o menor escopo e amplie por job somente quando necessário.

```yaml
permissions:
  contents: read # padrão para todo o workflow

jobs:
  detect-changes:
    permissions:
      contents: read
      pull-requests: read # somente este job precisa dela
```

## Jobs condicionais filtrados por path

Coloque jobs pesados atrás de `detect-changes` para que uma PR somente de documentação não execute Maven nem Terraform.

```yaml
backend:
  needs: detect-changes
  if: needs.detect-changes.outputs.backend == 'true'
```

## Concorrência e timeouts

Todo workflow cancela execuções substituídas, e todo job define `timeout-minutes` para impedir que uma etapa travada consuma o runner.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Implantação com OIDC (planejamento futuro)

Ainda não existe job de implantação. Ao adicioná-lo, autentique no Azure com federação OIDC, nunca com segredo de cliente armazenado, e solicite `id-token: write` somente nesse job.

```yaml
permissions:
  id-token: write # solicita o token OIDC de curta duração
  contents: read
steps:
  - uses: azure/login@<full-sha> # fixe-o
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
      subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

As cargas de trabalho implantadas usam Managed Identity para autenticação serviço a serviço (consulte [`infrastructure.instructions.md`](infrastructure.instructions.md)); os checklists de fortalecimento ficam na skill [`pipeline-hardening`](../skills/pipeline-hardening/SKILL.md).

## Convenções

| Regra | Justificativa |
|---|---|
| Fixe actions pelo SHA completo do commit | Impede o sequestro de tags na cadeia de suprimentos |
| Bloco `permissions:` em todo workflow, com `contents: read` por padrão | Privilégio mínimo por construção |
| `concurrency` + `cancel-in-progress` | Sem execuções desperdiçadas ou concorrentes na mesma ref |
| `timeout-minutes` em todo job | Uma etapa travada falha rapidamente |
| Federação OIDC, nunca segredo de nuvem armazenado | Sem credenciais de longa duração no repositório |

## Faça / Não faça

| Faça | Não faça |
|---|---|
| Referencie `@<sha> # vN` | Referencie `@v4`, `@main` ou uma branch |
| Conceda `id-token: write` por job de implantação | Conceda `write-all` no nível do workflow |
| Leia o workflow antes de editar um portão | Adivinhe o que um portão verifica |
| Permita que `detect-changes` pule jobs irrelevantes | Execute todo job em toda PR |

## Lista de verificação antes de abrir uma PR

- [ ] Todo `uses:` está fixado em um SHA completo de commit com comentário de versão
- [ ] O workflow declara um bloco `permissions:` de nível superior com privilégio mínimo
- [ ] Cada job define `timeout-minutes`, e o workflow define `concurrency`
- [ ] Novos portões estão descritos com precisão no arquivo de instruções pertinente
- [ ] Toda etapa de nuvem usa OIDC, não um segredo armazenado, e solicita `id-token: write` de forma restrita
- [ ] `markdownlint-cli2` e os jobs de CI existentes passam localmente quando reproduzíveis
