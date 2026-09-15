# Checklist do líder do time

![Tipo: checklist](https://img.shields.io/badge/Tipo-Lista%20de%20verifica%C3%A7%C3%A3o-171717?style=flat-square)
![Persona: Technical Lead](https://img.shields.io/badge/Persona-Technical%20Lead-737373?style=flat-square)
![Duração: o dia inteiro](https://img.shields.io/badge/Dura%C3%A7%C3%A3o-O%20dia%20todo-A3A3A3?style=flat-square)

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Checklist do líder**

**Checklist cronológico para o Technical Lead** — desde o período anterior à imersão até a demonstração final.

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa com a persona Technical Lead (Dupla 3) |
| **Pré-requisitos** | Leia [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md) |
| **Resultado esperado** | O time mantém o ritmo, os handoffs ocorrem no horário e a demonstração é apresentada |

---

## Antes do início da imersão (D-1, noite anterior)

- [ ] **Verifique os laptops** — cinco laptops têm o VS Code Insiders instalado.
- [ ] **Verifique as contas do GitHub** — cinco contas têm acesso ativo ao Copilot (confirme em <https://github.com/settings/copilot>).
- [ ] **Verifique o repositório** — `immersion-team-XX` foi criado e clonado por todos.
- [ ] **Valide as ferramentas locais** — Git, Java 21, Node, Docker e Spec-Kit funcionam em pelo menos um laptop.
- [ ] **Proteja a branch** — `develop` existe e está protegida.
- [ ] **Confirme a presença** — os cinco integrantes estão confirmados (uma dupla e duas personas por pessoa).

---

## Pontos de verificação hora a hora

### 10:00–11:00 · Setup e personas

- [ ] **10:15** — Todos os laptops abriram o repositório no VS Code.
- [ ] **10:30** — Git, Java/Node, Docker e Spec-Kit foram validados em todos os laptops.
- [ ] **10:45** — Todos leram seus dois arquivos `PERSONA.md` e confirmaram que `.github/` está consolidado.
- [ ] **10:55** — Todos testaram um slash command de sua persona.

### 11:00–12:00 · Estágio 1 — Arqueologia (parte 1)

- [ ] **11:00** — O time inteiro selecionou `@archaeologist` no GitHub Copilot.
- [ ] **11:10** — Cada dupla sabe quais três programas Natural lerá.
- [ ] **11:10** — Cada dupla sabe **quais quatro mistérios canônicos** são seus (`SIFAP-M-NN`; consulte [`mysteries-checklist.md`](../01-archaeology/mysteries-checklist.md)).
- [ ] **11:30** — Stand-up de dois minutos: cada dupla relata uma descoberta.
- [ ] **11:45** — Cada dupla registrou evidências e perguntas sobre seus programas atribuídos.

> [!TIP]
> **Os mistérios usam um denominador de 20** (quatro por dupla). Registre as evidências descobertas pelo time, sem antecipar respostas. Se uma dupla ficar bloqueada por mais de 40 minutos, peça uma dica para continuar a investigação.

### 13:30–14:00 · Estágio 1 — Síntese e handoff H1

- [ ] **13:35** — O catálogo contém fontes para as regras consideradas no escopo.
- [ ] **13:40** — Pontuação dos mistérios consolidada: **≥16/20**, sem nenhuma dupla abaixo de 2/4.
- [ ] **13:45** — O Product Owner selecionou uma funcionalidade fina e registrou os adiamentos.
- [ ] **13:50** — O facilitador validou `LEGACY-EXPLORATION-CHECKLIST.md`.
- [ ] **14:00** — **Handoff H1**: a Dupla 1 entrega `discovery-report.md` à Dupla 2.

> [!WARNING]
> Se alguma regra não tiver um `Programa de origem` às 13:50, pause tudo e preencha-o. A CI rejeita pull requests sem esse campo.

### 14:00–15:00 · Estágio 2 — Especificação moderna

- [ ] **14:05** — O time selecionou `@architect`.
- [ ] **14:30** — O Product Owner aprovou uma funcionalidade fina.
- [ ] **14:45** — `spec.md`, `plan.md` e `tasks.md` estão na pasta da funcionalidade.
- [ ] **15:00** — **Handoff H2**: artefatos formais entregues às Duplas 3 e 4.

> [!WARNING]
> Qualquer REQ-ID sem `source_legacy:` bloqueia o pull request. Verifique todos os requisitos antes do handoff.

### 15:00–16:10 · Estágio 3 — Implementação

- [ ] **15:05** — O time selecionou `@builder`.
- [ ] **15:30** — A migração V2 do Flyway foi criada e é executada localmente.
- [ ] **15:50** — Um ou mais endpoints REST funcionam pelo Swagger.
- [ ] **16:00** — Pelo menos um teste passa.
- [ ] **16:10** — **Handoff H3**: código integrado em `develop`, CI verde.

> [!WARNING]
> Se a CI falhar ou a cobertura ficar abaixo de 70%, priorize a correção antes de adicionar funcionalidades.

### 16:10–16:50 · Estágio 4 — Evolução com Agent

- [ ] **16:15** — O time selecionou `@evolution`.
- [ ] **16:20** — Existe pelo menos uma Issue bem escrita para o Copilot Agent.
- [ ] **16:35** — Pull request disponível revisado; se não houver PR, o próximo passo foi registrado.
- [ ] **16:45** — Status da CI/IaC registrado, sem criar infraestrutura apenas para cumprir uma métrica.
- [ ] **16:50** — `agent-experience-report.md` preenchido.

### 16:50–17:00 · Preparação da demonstração

- [ ] **Coordene os papéis de fala** — cada dupla tem um segmento definido de 30 segundos.
- [ ] **Teste a execução** — execute a demonstração uma vez com a abordagem criada pelo time.
- [ ] **Prepare o navegador** — Swagger, frontend e PR integrado estão abertos e prontos.

### 17:00–17:30 · Demonstrações

- [ ] O Product Owner apresenta e controla o tempo.
- [ ] O time inteiro aparece na câmera.
- [ ] O SIFAP 2.0 é demonstrado ao vivo.

---

## Três perguntas que o Technical Lead faz a cada 30 minutos

```text
1. Alguém está bloqueado há mais de 20 minutos?
2. A CI está verde?
3. O próximo handoff (H1/H2/H3) está dentro do cronograma?
```

Qualquer resposta negativa exige intervenção imediata.

---

## Respostas de emergência

| Situação | Ação do Technical Lead |
|---|---|
| A dupla está sem direção há 15 minutos | Sente-se com ela e pergunte: "Qual é o objetivo agora?" |
| A CI falha há 30 minutos | Interrompa os outros trabalhos e concentre o time na correção |
| O Product Owner muda o escopo após o H2 | Rejeite a mudança. O escopo é congelado no H2. |
| O Developer quer refatorar sem um teste existente | Rejeite. Interrompa a refatoração sem cobertura. |
| O Agent gera um pull request de baixa qualidade | Não integre. Solicite mudanças ou implemente manualmente. |
| Restam 30 minutos e a demonstração não funciona | Reduza o escopo da demonstração em vez de tentar corrigir o problema. |
| O Copilot está indisponível | Use o Plano B em [troubleshooting.md](troubleshooting.md#plano-b--indisponibilidade-do-copilot). |

---

## Objetivo do Technical Lead

> O papel do Technical Lead não é fazer o trabalho de todos: é garantir que ninguém fique ocioso.

Você contribui com código na mesma proporção que todos os demais. Sua responsabilidade específica é manter o **ritmo** e o **escopo**.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [TEAM-FLOW](../00-TEAM-FLOW.md)<br/><sub>Cronograma completo do dia.</sub> | [Lições aprendidas](lessons-learned.md)<br/><sub>Erros comuns dos times.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
