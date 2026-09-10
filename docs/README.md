# Documentação

> **Trilha:** [Kit do Time](../README.md) › **Documentação**

**Idioma:** português do Brasil (`portugues-br`). Use o [seletor de idiomas](../README.md#idiomas-do-repositório) para abrir a documentação e as instruções do Copilot de cada branch.

**Índice da documentação transversal da imersão** — recursos usados em qualquer estágio do dia.

| Campo | Valor |
|---|---|
| **Público-alvo** | O time inteiro, especialmente o Tech Writer e o Technical Lead |
| **Pré-requisitos** | Leia [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md) |
| **Tempo estimado** | 5 min |
| **Resultado esperado** | Saber onde encontrar cada recurso transversal |

---

## Como usar esta pasta

- [ ] **Antes de começar o dia** — leia [sdlc-flow-guide.md](sdlc-flow-guide.md) para entender o mapa completo.
- [ ] **Ao escolher suas personas** — leia [persona-agent-matrix.md](persona-agent-matrix.md) para saber quando você lidera, apoia ou observa.
- [ ] **Durante o Estágio 1** — atualize o [glossário do Estágio 1](../01-archaeology/glossary.md) e registre os termos com uma fonte do legado.
- [ ] **Para cada decisão técnica** — crie um ADR em [adr/](adr/).
- [ ] **No fim do dia** — revise [runbook.md](runbook.md) para que outra pessoa consiga executar e operar o sistema.

## Estrutura

| Caminho | Finalidade |
|---|---|
| [`adr/`](adr/) | Registros de decisão de arquitetura (um arquivo por decisão) |
| [`../01-archaeology/glossary.md`](../01-archaeology/glossary.md) | Glossário do domínio — preenchido durante o Estágio 1 |
| [`legacy-system-access.md`](legacy-system-access.md) | Acesso somente leitura ao sistema Natural/Adabas compartilhado |
| [`benefits-data.md`](benefits-data.md) | Massa completa de benefícios, carga autorizada no Adabas e comparação no PostgreSQL e nas telas modernas |
| [`4-agents-explained.md`](4-agents-explained.md) | Explicação dos quatro agentes de estágio e de sua relação com os kits de persona |
| [`persona-agent-matrix.md`](persona-agent-matrix.md) | Matriz que mostra quem lidera, apoia ou observa em cada estágio |
| [`sdlc-flow-guide.md`](sdlc-flow-guide.md) | Fluxo completo do dia, handoffs e entregáveis |
| `api.md` _(criado pelo time)_ | Visão geral do OpenAPI e resumo dos endpoints |
| [`runbook.md`](runbook.md) | Como executar o sistema localmente, na CI e no Azure |

## Convenções

- Use um ADR por decisão. Numere-os sequencialmente: `0001-title.md`, `0002-title.md`.
- Mantenha os termos do glossário em ordem alfabética, com referências ao programa legado em que cada termo surgiu.
- Todo README em uma subpasta segue [`.github/copilot-instructions.md`](../.github/copilot-instructions.md).
- Toda decisão importante se torna um ADR. Uma conversa no GitHub Copilot não é um registro suficiente.
- Todo termo do glossário originado no sistema legado precisa de uma fonte (`.NSN`, `.ddm` ou documento histórico).

## Definição de pronto da documentação

- [ ] O glossário inclui fontes do legado.
- [ ] Os ADRs incluem contexto, opções, decisão e consequências.
- [ ] O runbook inclui comandos de execução, validação e solução de problemas.
- [ ] Os links internos apontam para os arquivos corretos.
- [ ] Os documentos explicam o motivo antes do procedimento.

## Links rápidos

- [Fluxo do time](../00-TEAM-FLOW.md)
- [Kits de persona consolidados](../05-personas/) — leia o `PERSONA.md` do seu papel dentro do kit
- [Guias dos estágios](../01-archaeology/GUIDE.md)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Cartões de referência](../09-cheat-sheets/README.md)<br/><sub>Três cartões de uma página: Copilot, Spec-Kit e modelos.</sub> | [Glossário visual](../07-concepts/03-visual-glossary.md)<br/><sub>Mais de 30 termos técnicos do domínio do SIFAP.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
