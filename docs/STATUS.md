# STATUS diário — Painel de progresso

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **STATUS**

**Modelo de acompanhamento do próprio time:** preencha o status dos estágios, handoffs e métricas com as evidências produzidas durante a imersão. Este arquivo não informa a disponibilidade de ambientes externos.

![Painel de status diário](https://img.shields.io/badge/Painel-Status%20di%C3%A1rio-171717?style=flat-square) ![Atualização a cada 30 minutos](https://img.shields.io/badge/Atualiza%C3%A7%C3%A3o-A%20cada%2030%20min-737373?style=flat-square) ![Responsável: Technical Lead](https://img.shields.io/badge/Respons%C3%A1vel-Technical%20Lead-A3A3A3?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Technical Lead (atualiza) e demais participantes do time (consultam) |
| **Frequência de atualização** | A cada 30 minutos ou em cada transição de estágio |
| **Resultado esperado** | Visão de uma página do que está pronto, em andamento e bloqueado |

---

## Status geral

| Indicador | Status | Observações |
|---|---|---|
| Time inteiro presente | — | Atualize: OK ou Parcial |
| Ferramentas locais validadas em 5/5 laptops | — | — |
| Branch `develop` protegida | — | — |
| CI verde em `develop` | — | — |
| Demonstração ensaiada | — | — |

---

## Progresso nos quatro estágios

| Estágio | Status | Responsável | Início | DoD concluída? | Observações |
|---|---|---|---|---|---|
| **1 — Arqueologia** | Não iniciado | Todas as duplas | — | Não | — |
| **2 — Especificação** | Aguardando o handoff H1 | Dupla 2 | — | Não | — |
| **3 — Implementação** | Aguardando o handoff H2 | Duplas 3 e 4 | — | Não | — |
| **4 — Evolução** | Aguardando o handoff H3 | Dupla 5 | — | Não | — |

**Legenda de status:** Não iniciado · Em andamento · Concluído · Atrasado · Bloqueado

---

## Handoffs dos estágios

| Handoff | Origem e destino | Quando | Status |
|---|---|---|---|
| **H1** | Dupla 1 para Dupla 2 | Fim do Estágio 1 | Não concluído |
| **H2** | Dupla 2 para Duplas 3 e 4 | Fim do Estágio 2 | Não concluído |
| **H3** | Duplas 3 e 4 para Dupla 5 | Fim do Estágio 3 | Não concluído |

> [!NOTE]
> Cada handoff é uma conversa síncrona de cinco minutos entre as duplas que entregam e recebem. O cronograma detalhado está em [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md).

---

## Métricas do dia

| Métrica | Meta | Atual |
|---|---|---|
| Fontes do legado confirmadas para o escopo | Todo REQ-ID | — |
| Especificação formal (`spec.md`, `plan.md`, `tasks.md`) | Uma funcionalidade completa | — |
| Decisões de escopo registradas | Pelo menos uma | — |
| Primeiro incremento implementado | Um | — |
| Cobertura de testes do backend | Pelo menos 70% | — |
| Cobertura de testes do frontend | Pelo menos 60% | — |
| Issues criadas para o modo Agent | Pelo menos uma | — |
| PRs integrados em `develop` | — | — |

---

## Alertas ativos

> [!WARNING]
> Adicione uma entrada abaixo sempre que surgir um bloqueio ou risco. O Technical Lead a lê em voz alta no próximo stand-up.

- [ ] (nenhum alerta atual)

---

## Marcos alcançados

Marque cada marco quando ele for alcançado:

- [ ] **Primeira regra de negócio documentada com `Programa de origem`** — entrada do Estágio 1 concluída.
- [ ] **Primeira especificação EARS escrita** com o campo `source_legacy:` preenchido.
- [ ] **Primeira decisão de escopo registrada** e vinculada ao plano.
- [ ] **CI verde no primeiro Pull Request** — pipeline de integração aprovado.
- [ ] **Primeiro endpoint REST funcionando** e visível pelo Swagger.
- [ ] **Cobertura de testes do backend igual ou superior a 70%**.
- [ ] **Primeiro Pull Request do modo Agent revisado e integrado**.
- [ ] **Plano do Terraform concluído sem erros**.
- [ ] **Demonstração final do SIFAP 2.0 concluída com sucesso**.

---

## Registro do stand-up (uma frase por dupla em cada transição)

### H1 — fim do Estágio 1

| Dupla | Persona | Registro |
|---|---|---|
| Dupla 1 | Visão (PO + RE) | ___ |
| Dupla 2 | Arquitetura (EA + SA) | ___ |
| Dupla 3 | Implementação (TL + Dev) | ___ |
| Dupla 4 | Qualidade (DBA + QA) | ___ |
| Dupla 5 | Operações (DevOps + TW) | ___ |

### H2 — fim do Estágio 2

| Dupla | Registro |
|---|---|
| Dupla 1 | ___ |
| Dupla 2 | ___ |
| Dupla 3 | ___ |
| Dupla 4 | ___ |
| Dupla 5 | ___ |

### H3 — fim do Estágio 3

| Dupla | Registro |
|---|---|
| Dupla 1 | ___ |
| Dupla 2 | ___ |
| Dupla 3 | ___ |
| Dupla 4 | ___ |
| Dupla 5 | ___ |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Roteiro da demonstração](demo-script.md)<br/><sub>Roteiro para a demonstração final de três minutos.</sub> | [Checklist do líder](CHECKLIST-LIDER.md)<br/><sub>Guia hora a hora para o Technical Lead.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
