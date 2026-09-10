# Tech Writer — Kit do Copilot

> **Trilha:** [Kit do Time](../../README.md) › [Personas](../OVERVIEW.md) › **Tech Writer**

**Kit de referência para a persona Tech Writer na imersão de modernização do SIFAP.**

![Persona](https://img.shields.io/badge/Persona-Tech%20Writer-171717?style=flat-square) ![Dupla 5](https://img.shields.io/badge/Dupla-5%20%C2%B7%20Opera%C3%A7%C3%B5es-404040?style=flat-square) ![Atuação transversal](https://img.shields.io/badge/Atua%C3%A7%C3%A3o-Transversal-737373?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Pessoa que assume a persona Tech Writer na imersão |
| **Foco** | Documentação de API, evolução do README, `CODEMAP.md`, ADRs, changelog e detecção de desvio |
| **Fase do SDLC** | Transversal a todos os estágios; lidera o Estágio 4 — Evolução (relatório do Agent) |
| **Resultado esperado** | README completo, ADRs formalizados, glossário consistente e relatório honesto do Estágio 4 |

Leia primeiro: [PERSONA.md](PERSONA.md).

---

## Conceito

A pessoa Tech Writer transforma decisões e código em uma memória duradoura do projeto. Na modernização do SIFAP (Sistema de Fiscalização e Administração de Pagamentos), essa persona mantém o glossário de termos do legado Natural/Adabas, formaliza as decisões de arquitetura como ADRs (Architecture Decision Records) e garante que o README reflita o estado real da aplicação a cada hora da imersão, não apenas no final.

Por que isso importa: sem documentação intencional, os ADRs permanecem vazios, o README continua com "TODO: adicionar instruções" e o conhecimento descoberto durante a imersão desaparece depois dela. A pessoa Tech Writer torna o aprendizado do time rastreável.

## Kit de persona

Todos os artefatos ativos ficam no diretório `.github/` da raiz do repositório. Esta pasta serve como referência; quando precisar fazer manutenção, edite os arquivos em `.github/`.

| Arquivo | Tipo | Finalidade |
|---|---|---|
| `PERSONA.md` | Perfil | Responsabilidades, estágios, prompts e rubricas de Tech Writer |
| `.github/agents/tech-writer.agent.md` | Agente | Documentação de API, README, `CODEMAP.md`, changelog e detecção de desvio |
| `.github/prompts/persona-tech-writer-generate-docs.prompt.md` | Prompt | `/generate-docs` |
| `.github/prompts/persona-tech-writer-update-codemap.prompt.md` | Prompt | `/update-codemap` |
| `.github/prompts/persona-tech-writer-doc-drift.prompt.md` | Prompt | `/doc-drift` |

> [!NOTE]
> Edite e revise o Markdown do time diretamente no repositório. Esta persona dos participantes não distribui servidor de implantação no Pages; a publicação do site pertence ao repositório do instrutor.

## Onde ficam os artefatos ativos

- Agentes: `.github/agents/`
- Prompts: `.github/prompts/persona-*.prompt.md`
- Skills: `.github/skills/`
- Instruções: `.github/instructions/`

## Boas práticas

- [ ] **Trate a documentação como uma feature.** Entregue, versione e revise a documentação com o código, não depois dele.
- [ ] **Comece pela resposta e depois apresente o contexto.** Escreva para quem dispõe de 30 segundos.
- [ ] **Use Mermaid nos diagramas.** Diagramas como código evoluem com o sistema.
- [ ] **Inclua verificações de desvio na CI.** Documentação desatualizada é pior do que nenhuma documentação.

## Exemplo do SIFAP

No Estágio 1, a pessoa Tech Writer documenta no glossário os termos confirmados nos programas e DDMs atribuídos. No Estágio 3, atualiza `README.md` com os endpoints e comandos reais do protótipo. No Estágio 4, acompanha o Agent e escreve `04-evolution/agent-experience-report.md` em tempo real.

## Referências

- [Diátaxis Framework](https://diataxis.fr/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Write the Docs](https://www.writethedocs.org/)
- [Mermaid — Diagramas como código](https://mermaid.js.org/)

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Visão geral das personas](../OVERVIEW.md)<br/><sub>Tabela das 10 personas e suas duplas.</sub> | [PERSONA.md](PERSONA.md)<br/><sub>Perfil completo da persona Tech Writer.</sub> |

<sub>[Voltar ao índice do kit](../../README.md)</sub>
