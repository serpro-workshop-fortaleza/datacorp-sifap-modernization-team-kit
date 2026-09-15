# Estágio 1 — Arqueologia

> **Trilha:** [Kit do Time](../README.md) › **Estágio 1 — Arqueologia**

**Visão geral do Estágio 1.** Leia esta página antes de abrir o GUIDE; ela apresenta o objetivo, os artefatos esperados e os participantes.

| Campo | Valor |
|---|---|
| **Público-alvo** | As 5 duplas do time |
| **Pré-requisitos** | Nenhum — este é o ponto de partida |
| **Tempo estimado** | 90 min (11:00–12:00 + 13:30–14:00) |
| **Estágio** | Estágio 1 — Arqueologia |
| **Resultado esperado** | Catálogo de regras, mapa de dependências, glossário e relatório de descoberta |

![Estágio 1](https://img.shields.io/badge/Est%C3%A1gio-1%20%C2%B7%20Arqueologia-171717?style=flat-square) ![Gate obrigatório](https://img.shields.io/badge/Crit%C3%A9rio-Obrigat%C3%B3rio-404040?style=flat-square) ![Todas as duplas em paralelo](https://img.shields.io/badge/Duplas-Todas%20em%20paralelo-737373?style=flat-square)

> [!IMPORTANT]
> **Leia primeiro:** [`LEGACY-EXPLORATION-CHECKLIST.md`](LEGACY-EXPLORATION-CHECKLIST.md) — gate obrigatório antes de começar o Estágio 2. Nenhum requisito EARS é aceito sem rastreabilidade até o código legado.

> [!TIP]
> **Use o corpus local como evidência.** Os programas Natural, DDMs, FDT e documentos históricos estão em [`legacy-sifap/`](legacy-sifap/). A investigação deste estágio não depende de acesso a um sistema em execução.

---

## O que é o Estágio 1

**Arqueologia de software** é a prática de extrair conhecimento de sistemas legados lendo o código-fonte de forma sistemática, sem modificá-lo. Nesta imersão, a arqueologia tem um objetivo preciso: reunir evidência suficiente para escrever requisitos rastreáveis no Estágio 2.

O SIFAP, o Sistema de Fiscalização e Administração de Pagamentos, opera há 29 anos. A maior parte do conhecimento sobre suas regras de negócio está no código Natural, não em documentação. Sem ler o código, o time escreveria especificações baseadas em suposições — o que o CI rejeita, porque exige um `source_legacy:` válido.

---

## Onde isto se encaixa no fluxo da imersão

![Timeline do dia: pré-evento, 4 estágios e demo, com os três handoffs H1, H2 e H3](../assets/timeline-stages.svg)

---

## Quem trabalha aqui

As 5 duplas trabalham em paralelo, cada uma responsável por 3 programas Natural. A Dupla 1 (Visão) lidera a síntese no fim do estágio. Veja [`GUIDE.md`](GUIDE.md) para a distribuição completa.

---

## Artefatos do Estágio 1

| Arquivo | Finalidade |
|---|---|
| [`LEGACY-EXPLORATION-CHECKLIST.md`](LEGACY-EXPLORATION-CHECKLIST.md) | **Gate obrigatório.** Responsabilidade por programa em cada dupla e critérios de conclusão antes do Estágio 2. |
| [`GUIDE.md`](GUIDE.md) | Guia passo a passo com cronograma cronometrado. |
| [`glossary.md`](glossary.md) | Glossário dos termos e abreviações do domínio SIFAP. |
| [`business-rules-catalog.md`](business-rules-catalog.md) | Catálogo das regras de negócio extraídas, com `Programa de origem` obrigatório. |
| [`dependency-map.md`](dependency-map.md) | Mapa de dependências entre programas e DDMs. |
| [`discovery-report.md`](discovery-report.md) | Relatório de descoberta que consolida as evidências do estágio. |
| [`mysteries-checklist.md`](mysteries-checklist.md) | Checklist de rastreabilidade das questões em aberto. |
| [`mysteries-found.md`](mysteries-found.md) | Registro detalhado das questões em aberto, com evidência e responsável. |

O código legado está em [`legacy-sifap/`](legacy-sifap/) (compartilhado pelo kit).

Esses arquivos são insumos de leitura dos participantes. Não os altere nem tente usá-los para implantar um laboratório; registre suas descobertas nos artefatos do estágio.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Kit do Time](../README.md)<br/><sub>Hub principal do repositório.</sub> | [GUIDE do Estágio 1](GUIDE.md)<br/><sub>Cronograma cronometrado de 90 minutos para ler o sistema legado e catalogar regras.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
