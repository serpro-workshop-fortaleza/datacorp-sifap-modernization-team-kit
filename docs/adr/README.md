# Registros de decisão de arquitetura (ADRs)

> **Trilha:** [Kit do Time](../../README.md) › [Documentação](../README.md) › **ADRs**

**Índice dos registros de decisão de arquitetura do time** — uma decisão por arquivo, com numeração sequencial.

| Campo | Valor |
|---|---|
| **Público-alvo** | O time inteiro, especialmente o Software Architect e o Technical Lead |
| **Quando criar** | Para toda decisão difícil de rever depois (mais de uma hora para reverter) |
| **Resultado esperado** | Histórico auditável das decisões tomadas sob pressão de tempo |

---

## Por que escrever ADRs

Decisões tomadas sob pressão de tempo são esquecidas. No futuro, você redescobrirá as mesmas opções e perderá horas. Escrever um ADR agora leva cinco minutos e economiza 50 minutos depois.

## Quando escrever um ADR

Escreva um quando:

- A decisão for difícil de rever depois (mais de uma hora para reverter).
- Duas ou mais pessoas do time naturalmente fariam escolhas diferentes.
- A decisão afetar mais de um contexto delimitado ou persona.

Não escreva um ADR para nomes de variáveis, configurações de formatação ou versões secundárias de bibliotecas.

---

## Índice

| ADR | Título | Status | Data |
|---|---|---|---|
| 0000 | [Modelo](0000-template.md) | template | 2026-04-29 |
| 0001 | [Fonte única de verdade para instruções de agentes](0001-agent-instructions-single-source-of-truth.md) | accepted | 2026-08-17 |

> [!NOTE]
> Adicione novos ADRs a esta tabela quando forem criados, primeiro com o status `proposed` e depois `accepted`, após o acordo do time.

---

## Como adicionar um ADR

- [ ] **Abra uma issue** usando o [modelo de issue de ADR](../../.github/ISSUE_TEMPLATE/adr.yml).
- [ ] **Copie o modelo** — `0000-template.md` → `NNNN-your-title.md` (próximo número sequencial).
- [ ] **Preencha todas as seções** — contexto, decisão, alternativas, consequências e status.
- [ ] **Abra um pull request** — exija pelo menos uma revisão de uma persona de arquitetura.
- [ ] **Integre com o status `accepted`** — atualize este índice.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Documentação transversal](../README.md)<br/><sub>Glossário, fluxo do SDLC, matriz persona-agente e runbook.</sub> | [Estágio 2 — Especificação moderna](../../02-modern-spec/GUIDE.md)<br/><sub>14:00–15:00 — Escreva EARS, ADRs e diagramas C4.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
