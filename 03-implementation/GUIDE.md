# Estágio 3 — Implementação (70 min)

> **Trilha:** [Kit do Time](../README.md) › [Estágio 3](README.md) › **GUIDE**

**Este guia conduz as Duplas 3 e 4 pela criação do protótipo funcional do SIFAP 2.0, desde a estrutura inicial até as features implementadas com testes, migrações e rastreabilidade até os REQ-IDs.**

![Estágio 3](https://img.shields.io/badge/Est%C3%A1gio-3%20%C2%B7%20Implementa%C3%A7%C3%A3o-171717?style=flat-square) ![Duração: 70 min](https://img.shields.io/badge/Dura%C3%A7%C3%A3o-70%20min-737373?style=flat-square) ![Horário: 15:00–16:10](https://img.shields.io/badge/Hor%C3%A1rio-15%3A00--16%3A10-A3A3A3?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | A Dupla 3 (TL + Developer) e a Dupla 4 (DBA + QA) lideram; a Dupla 5 prepara a estrutura da CI |
| **Pré-requisitos** | Handoff H2 aceito; `spec.md`, `plan.md` e `tasks.md` prontos com REQ-IDs e `source_legacy:` |
| **Tempo estimado** | 70 min |
| **Estágio** | Estágio 3 — Implementação |
| **Resultado esperado** | Backend e frontend funcionais; testes aprovados; commits com `Implements REQ-XXX` |

> [!IMPORTANT]
> Consulte o cronograma exato em [`00-TEAM-FLOW.md`](../00-TEAM-FLOW.md). Os badges mostram somente a duração do estágio.

---

## Conceito: Monólito Modular

Um Monólito Modular é uma arquitetura na qual os bounded contexts são módulos Java independentes dentro de uma única JVM, com fronteiras explícitas entre eles. É o ponto de partida recomendado para modernizar o SIFAP antes de qualquer extração futura de microsserviços.

**Por que isso importa:** o SIFAP legado tem acoplamento implícito entre módulos por meio da memória compartilhada (Natural/Adabas). O Monólito Modular torna esse acoplamento explícito e controlado. Cada módulo expõe somente a interface necessária aos demais módulos.

**Strangler Fig:** padrão de migração que envolve gradualmente o sistema legado. O protótipo do Estágio 3 não precisa substituir todo o SIFAP. Modernize um bounded context por vez enquanto mantém o sistema legado ativo para as partes que ainda não migraram.

---

## Conceito: Testcontainers

Testcontainers é uma biblioteca Java que inicia contêineres Docker reais durante os testes. Em vez de simular o PostgreSQL com um banco de dados em memória (H2), os testes usam o mecanismo real do banco de dados de produção.

**Por que isso importa:** testes com H2 podem passar e depois falhar com PostgreSQL devido a diferenças em SQL, tipos e comportamento de transações. O Testcontainers elimina essa divergência.

**Erro comum:** esquecer de iniciar o Docker Desktop antes de executar `./mvnw test`. O erro é `Could not find a valid Docker environment`.

---

## Conceito: TDD (Test-Driven Development)

TDD é a prática de escrever o teste antes da implementação. O ciclo consiste em escrever um teste que falha (vermelho), implementar o código mínimo necessário para passar (verde) e melhorar o código sem quebrar o teste (refatorar).

**No SIFAP:** antes de implementar o cálculo de reajuste do benefício (REQ-042), escreva um teste que valide os critérios de aceitação definidos no `spec.md`. O teste falha até que a lógica seja implementada.

---

## Definição de pronto para começar

> [!IMPORTANT]
> Confirme todos os itens antes de iniciar este estágio:

- [ ] O PO aceitou o handoff H2.
- [ ] A persona `@builder` está selecionada no GitHub Copilot.
- [ ] `specs/<NNN>-<feature>/spec.md` tem REQ-IDs com entradas `source_legacy:` válidas.
- [ ] `specs/<NNN>-<feature>/plan.md` contém as decisões necessárias para a primeira tarefa.
- [ ] O time definiu os caminhos iniciais do protótipo (`backend/`, `frontend/` e, se necessário, `infra/`).
- [ ] A branch `impl/<NNN>-<feature>` foi criada a partir da branch `develop` atualizada.

---

## Objetivo

Crie do zero o primeiro protótipo funcional do SIFAP 2.0 e implemente as features priorizadas no Estágio 2. O kit não fornece base de código, conteinerização pronta nem link simbólico para um protótipo. O time cria a estrutura, implementa as features e escreve os testes. Toda feature deve ser rastreável até um REQ-ID.

O Estágio 3 é onde a especificação encontra a realidade. Um requisito EARS bem escrito no Estágio 2 se torna um teste que passa ou falha. Todo commit inclui uma referência `Implements REQ-XXX:` na mensagem. Sem ela, a rastreabilidade termina.

---

## Primeiros 15 minutos: criação da estrutura

### Passo 1 — Crie as pastas do protótipo

```bash
mkdir -p backend frontend
```

### Passo 2 — Crie a estrutura mínima

- **Backend:** Spring Boot 3.3, Java 21, Maven Wrapper e pacote-base `br.gov.sifap`.
- **Frontend:** Next.js 15 App Router, TypeScript estrito e Tailwind CSS.
- **Banco de dados:** migrações Flyway em `backend/src/main/resources/db/migration/`.

> [!CAUTION]
> Não use código nem conteinerização de protótipos externos. O objetivo da imersão é que o time construa o protótipo moderno a partir da própria leitura do sistema legado.

### Passo 3 — Verifique se a configuração mínima funciona

- Backend: `cd backend && ./mvnw test` deve passar assim que a estrutura existir.
- Frontend: `cd frontend && npm test` (ou o comando definido pelo time) deve passar.
- Crie `infra/` somente quando o time começar a descrever IaC ou a composição local.

---

## Estrutura do backend

```text
src/main/java/br/gov/client/sifap/
└── <feature>/
    ├── domain/
    ├── application/
    └── infrastructure/
```

### Camadas (de dentro para fora)

| Camada | Responsabilidade | Exemplos |
|---|---|---|
| **domain** | Regras de negócio puras, sem dependência de framework | Enums de status, interfaces de repositório, objetos de valor |
| **application** | Casos de uso e orquestração | Serviços, DTOs de requisição/resposta |
| **infrastructure** | Detalhes técnicos e E/S | Controllers REST, entidades JPA, repositórios Spring Data |

> [!IMPORTANT]
> A camada `domain` nunca importa classes de `infrastructure`. O fluxo é sempre Controller → Service → Repository (interface no domínio, implementação na infraestrutura).

---

## Passo a passo: adicione uma feature

Para os recortes de beneficiários e pagamentos, use a [massa sintética completa e o roteiro de reconciliação](../docs/benefits-data.md). O pacote fornece todos os campos dos quatro DDMs e uma carga no schema local `sifap_seed`; o time ainda precisa importar para suas tabelas de domínio, consultar pela API e exibir esses registros na UI. Não substitua a massa por valores fixos nos componentes.

- [ ] **Releia o requisito EARS.** Abra o `spec.md` e releia o REQ-ID que será implementado.
- [ ] **Verifique a evidência legada.** Confirme o `source_legacy:` e releia o programa `.NSN` correspondente.
- [ ] **Modele o comportamento.** Defina a entidade, os casos de uso e os contratos REST no contexto correto.
- [ ] **Crie a migração Flyway.** Adicione `V<N>__description.sql` em `db/migration/`.
- [ ] **Escreva primeiro o teste.** Crie o teste de integração antes de implementar (TDD).
- [ ] **Implemente o código.** Controller → Service → Repository, seguindo as camadas.
- [ ] **Execute os testes.** `./mvnw test` deve passar com o Docker em execução.
- [ ] **Faça o commit da alteração.** Inclua `Implements REQ-XXX` na mensagem.

> [!CAUTION]
> Use Flyway. Nunca modifique migrações existentes. Sempre crie novas migrações (`V2__`, `V3__` e assim por diante). Editar uma migração antiga corrompe o histórico do schema e quebra os deployments.

---

## Fluxo com o Copilot Plan

Para implementar features com rastreabilidade:

1. Selecione os arquivos relevantes no VS Code (Ctrl+clique).
2. Abra o painel do GitHub Copilot e selecione o modo Plan.
3. Descreva a alteração em linguagem natural e solicite um plano antes da execução:
    > "Planeje a implementação do EARS `REQ-XXX`. Liste os arquivos envolvidos, os riscos e os testes necessários. Ainda não implemente."
4. Revise o plano e o diff antes de aceitá-los. Verifique se seguem a arquitetura.
5. Execute os testes para confirmar.

> [!TIP]
> Prefira o modo Plan para features pequenas. O modo Agent do Copilot é mais adequado ao Estágio 4, que concede maior autonomia de escopo.

---

## Testes

### Execute todos os testes

```bash
cd backend
./mvnw test
```

**Pré-requisito:** o Docker deve estar em execução. Os testes usam Testcontainers para iniciar uma instância real do PostgreSQL.

### Tipos de teste esperados

| Tipo | Classe | O que testa |
|---|---|---|
| Unitário | `*ServiceTest.java` | Lógica de negócio isolada |
| Integração | `*ControllerTest.java` | Endpoint completo (HTTP → DB) |
| Repositório | `*RepositoryTest.java` | Consultas personalizadas |

---

## Frontend

### Execute o frontend localmente

```bash
cd frontend
npm install
npm run dev
```

Abra `http://localhost:3000`.

### Arquitetura do frontend

O frontend usa Next.js 15 com App Router e Server Components:

```text
src/app/
├── layout.tsx
├── page.tsx
└── <feature>/
    └── page.tsx
```

| Tipo de componente | Quando usar |
|---|---|
| **Server Component** (padrão) | Busca de dados no servidor; sem JavaScript no lado do cliente |
| **Client Component** (`"use client"`) | Interatividade: formulários, modais e estado local |

---

## Rastreabilidade: requisito → código → teste

Documente a rastreabilidade de cada feature implementada:

| Requisito EARS | Arquivo de implementação | Arquivo de teste |
|---|---|---|
| `REQ-XXX` | `<!-- preencher -->` | `<!-- preencher -->` |

Todo commit que implementa um comportamento da especificação deve incluir `Implements REQ-XXX` na mensagem. Isso fecha o ciclo especificação → código → teste e permite que `/speckit.analyze` detecte desvios.

---

<details>
<summary><strong>Erros comuns — expandir</strong></summary>

| Se você estiver fazendo isto | Faça isto |
|---|---|
| Uma branch enorme com oito horas de trabalho | Use commits e PRs pequenos. Uma feature = um PR |
| Implementar sem testes e planejar "fazê-los depois" | Escreva o teste junto com o código |
| Editar uma migração Flyway antiga | Nunca faça isso. Sempre crie uma nova migração (`V5__`, `V6__`...) |
| Criar um endpoint sem `@Valid` no DTO | Sempre use Bean Validation no controller |
| Misturar lógica de domínio no controller | O controller chama um serviço. A lógica pertence ao serviço ou ao domínio |
| Importar classes de infraestrutura entre contextos | Preserve as fronteiras definidas pelo time |
| Fazer commit sem `Implements REQ-XXX` | A rastreabilidade valida o trabalho do estágio anterior |

</details>

---

<details>
<summary><strong>Solução de problemas — expandir</strong></summary>

| Problema | Solução |
|---|---|
| O ambiente local não inicia | Verifique Java 21, Node, variáveis de ambiente e se as portas 5432/8080/3000 estão livres |
| O backend não se conecta ao PostgreSQL | Verifique a URL configurada e se a instância PostgreSQL selecionada pelo time está em execução |
| O frontend mostra "Failed to load" | O backend está em execução? Teste com `curl http://localhost:8080/actuator/health` |
| O teste com Testcontainers falha | O Docker Desktop deve estar em execução. Alternativa: um teste unitário com Mockito |
| A migração falha na inicialização | Nunca edite uma migração existente. Crie uma nova (`V5__`, `V6__`...) |
| Erro de import no `mvn test-compile` | Verifique se o pacote segue `domain/` → `application/` → `infrastructure/` |
| A Swagger UI não aparece | Tente `http://localhost:8080/swagger-ui/index.html` |

</details>

---

## Critérios de conclusão

- [ ] O fluxo priorizado pelo time está implementado e documentado.
- [ ] A interface necessária para esse fluxo está disponível.
- [ ] Os testes definidos pelo time passam com `./mvnw test`.
- [ ] A execução local está documentada no protótipo.
- [ ] Os contratos expostos estão documentados com Swagger/OpenAPI.
- [ ] A regra priorizada no Estágio 1 está implementada e testada.
- [ ] Todo commit inclui `Implements REQ-XXX` na mensagem.

---

## Próxima etapa

Durante o handoff H3 (por volta das 17:00), a Dupla 3 entrega o código funcional à Dupla 5 (Operações), responsável por Terraform e CI/CD no Estágio 4. A Dupla 4 continua os testes finais.

Consulte [`../04-evolution/GUIDE.md`](../04-evolution/GUIDE.md) para o próximo estágio.

---

<details>
<summary><strong>Prompts úteis para o modo Ask do GitHub Copilot — expandir</strong></summary>

1. "Crie um endpoint REST para [feature] seguindo a arquitetura existente."
2. "Escreva um teste de integração para o endpoint [endpoint]."
3. "Adicione Bean Validation ao DTO [class]."
4. "Crie uma migração Flyway para adicionar [table/column]."
5. "Implemente a regra de negócio BR-XXX: [descrição da regra]."
6. "Crie um React Server Component para listar [entidade]."
7. "Adicione tratamento de erros para [cenário]."
8. "Refatore este serviço para separar a lógica de [responsabilidade]."

</details>

> [!TIP]
> Não tente implementar tudo. Priorize a qualidade, não a quantidade. Um endpoint bem construído, com testes, validação e documentação, vale mais do que cinco endpoints quebrados.

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Estágio 2 — Especificação](../02-modern-spec/GUIDE.md)<br/><sub>14:00–15:00 · Escreva requisitos EARS, ADRs e diagramas C4.</sub> | [Estágio 4 — Evolução](../04-evolution/GUIDE.md)<br/><sub>16:10–16:50 · Copilot Agent + Terraform + CI/CD.</sub> |

<sub>[Voltar ao índice do kit](../README.md)</sub>
