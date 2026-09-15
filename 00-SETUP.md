# Guia de configuração: do zero ao código

> **Trilha:** [Kit do time](README.md) › **Configuração**

**Este guia leva você de "ainda não temos nada" a "repositório criado, Copilot funcionando, todas as personas prontas" em 45 minutos.**

![Configuração](https://img.shields.io/badge/Configura%C3%A7%C3%A3o-00-171717?style=flat-square) ![Duração: 45 min](https://img.shields.io/badge/Dura%C3%A7%C3%A3o-45%20min-737373?style=flat-square) ![Quando: antes do Dia 2](https://img.shields.io/badge/Quando-Antes%20do%20Dia%202-A3A3A3?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Líder do time + cada integrante no seu próprio laptop |
| **Pré-requisitos** | Conta GitHub com o Copilot habilitado |
| **Tempo estimado** | 45 minutos |
| **Resultado esperado** | Repositório protegido, Copilot ativo, personas validadas, teste de fumaça verde |

> [!WARNING]
> **Usuários de Windows:** os blocos de terminal com heredoc ou `for` assumem **Git Bash** ou **WSL**. Não use PowerShell nem CMD nesses blocos.

**Vocês são cinco pessoas. Cada pessoa usa duas personas. Vocês têm um dia de trabalho.** Todo mundo acompanha no próprio laptop. Uma pessoa compartilha a tela nos passos, e as outras quatro repetem. No fim, todo laptop está configurado.

## Sumário

- [Antes de começar: modelo mental](#antes-de-começar-modelo-mental)
- [Passo 1: Verifique os pré-requisitos do seu laptop](#passo-1-verifique-os-pré-requisitos-do-seu-laptop)
- [Passo 2: Crie o repositório do time a partir do template (só o líder)](#passo-2-crie-o-repositório-do-time-a-partir-do-template-só-o-líder)
- [Passo 3: Clone o repositório e crie a branch `develop` (só o líder)](#passo-3-clone-o-repositório-e-crie-a-branch-develop-só-o-líder)
- [Passo 4: Proteja a branch `main` (só o líder)](#passo-4-proteja-a-branch-main-só-o-líder)
- [Passo 5: Adicione os outros quatro integrantes (só o líder)](#passo-5-adicione-os-outros-quatro-integrantes-só-o-líder)
- [Passo 6: Cada integrante clona o repositório](#passo-6-cada-integrante-clona-o-repositório)
- [Passo 7: Ative o GitHub Copilot no VS Code (todos)](#passo-7-ative-o-github-copilot-no-vs-code-todos)
- [Passo 8: Valide os agentes e prompts das suas personas (todos)](#passo-8-valide-os-agentes-e-prompts-das-suas-personas-todos)
- [Passo 9: Instale o Spec-Kit (todos)](#passo-9-instale-o-spec-kit-todos)
- [Passo 10: Use o fluxo do Spec-Kit (todos)](#passo-10-use-o-fluxo-do-spec-kit-todos)
- [Passo 11: Entenda a estratégia de branches](#passo-11-entenda-a-estratégia-de-branches)
- [Passo 12: Fluxo diário por persona](#passo-12-fluxo-diário-por-persona)
- [Passo 13: Teste de fumaça (time inteiro, às 10:30)](#passo-13-teste-de-fumaça-time-inteiro-às-1030)
- [Solução de problemas](#solução-de-problemas)

---

## Antes de começar: modelo mental

Você vai trabalhar com **dois repositórios do GitHub**:

```text
GitHub
├── <TEMPLATE_ORG>/immersion-preto-00/       (repositório principal da imersão, usado uma vez como template)
└── <IMMERSION_ORG>/immersion-team-XX/        (repositório de trabalho do SEU time - onde você commita)
```

No seu laptop, você clona só o repositório do seu time:

```bash
~/Code/immersion-team-XX/
```

| Repositório | O que você faz com ele | Onde ele vive |
|---|---|---|
| `immersion-preto-00` | Use uma vez como template, no começo | `github.com/<TEMPLATE_ORG>/immersion-preto-00` |
| `immersion-team-XX` | Todo o seu trabalho vai para cá | `github.com/<IMMERSION_ORG>/immersion-team-XX` (privado, você cria) |

> [!NOTE]
> A organização desta edição é [`serpro-workshop-fortaleza`](https://github.com/serpro-workshop-fortaleza). Nos comandos abaixo, substitua `<IMMERSION_ORG>` por esse nome e use o repositório do seu time.

> [!IMPORTANT]
> Nunca faça push no repositório principal da imersão. Os commits do seu time vão só para `immersion-team-XX`. O **Sistema de Fiscalização e Administração de Pagamentos (SIFAP)** legado já vem no kit em `01-archaeology/legacy-sifap/` e é material de leitura, não de edição.

---

## Passo 1: Verifique os pré-requisitos do seu laptop

**Cada integrante do time roda este checklist no próprio laptop.**

- [ ] **Verifique as ferramentas.**

| Ferramenta | Versão mínima | Como verificar | Se estiver faltando |
|---|---|---|---|
| **Git** | 2.40+ | `git --version` | <https://git-scm.com/downloads> |
| **Conta GitHub** | - | Entre em github.com | <https://github.com/signup> |
| **GitHub CLI** | 2.40+ | `gh --version` | <https://cli.github.com> |
| **VS Code** | 1.93+ | Help -> About | <https://code.visualstudio.com/download> |
| **Docker Desktop** | 4.30+ | `docker --version` e abra o app | <https://www.docker.com/products/docker-desktop> |
| **Java 21 JDK** | 21 | `java -version` | <https://learn.microsoft.com/java/openjdk/download> |
| **Node.js** | 20 LTS | `node --version` | <https://nodejs.org/en/download> |

> [!CAUTION]
> Falta a maior parte desses itens? Instale as ferramentas antes de a imersão começar. Este kit não vem com ambiente pronto nem bootstrap automático.

### Verificação de licença (uma pessoa verifica pelo time)

- [ ] **Abra <https://github.com/settings/copilot>** - você deve ver "Active subscription" (Individual) ou "Business plan". Se aparecer "Get GitHub Copilot", chame um facilitador.

---

## Passo 2: Crie o repositório do time a partir do template (só o líder)

**Escolham uma pessoa para ser o líder do time** (normalmente quem cobre a persona Technical Lead, na Dupla 3). Só o líder executa os Passos 2 a 5. Os outros quatro esperam e seguem a partir do Passo 6.

### Usando o template no GitHub

> [!IMPORTANT]
> Este fluxo exige **Template repository** habilitado no kit público do time. Se **Use this template** não estiver disponível, fale com um facilitador antes de criar o repositório do time.

- [ ] **Crie o repositório a partir do template.**

1. Abra o [kit público dos participantes](https://github.com/serpro-workshop-fortaleza/datacorp-sifap-modernization-team-kit/tree/portugues-br).
2. Clique em **Use this template** -> **Create a new repository**.
3. Preencha:

- **Owner**: `serpro-workshop-fortaleza`. Não escolha seu usuário pessoal.
- **Repository name**: `immersion-team-XX` (troque XX pelo número do seu time, por exemplo `immersion-team-01`)
- **Description**: `Imersão DATACORP 2026 - Time XX`
- **Visibility**: Private
- **Include all branches**: deixe desmarcado. Copie somente a edição `portugues-br`; o Passo 3 prepara as branches de trabalho na cópia do time.

4. Clique em **Create repository**.

Agora você deve ver uma cópia completa do kit em `https://github.com/<IMMERSION_ORG>/immersion-team-XX`, incluindo documentação, código legado, templates, workflows e arquivos `.github/`.

O template usa `portugues-br` como branch padrão. A cópia contém o material dos participantes em português, sem site, demos prontas ou ambientes do instrutor.
As branches `main` e `develop` do exercício são preparadas **somente no repositório do time**, no passo seguinte.

---

## Passo 3: Clone o repositório e crie a branch `develop` (só o líder)

- [ ] **Clone o repositório e crie a branch `develop`.**

```bash
# 1. Escolha uma pasta para todo o seu código
mkdir -p ~/Code && cd ~/Code

# 2. Clone o repositório do seu time
git clone https://github.com/<IMMERSION_ORG>/immersion-team-01.git
cd immersion-team-01

# 3. Confirme que o template veio intacto
ls 01-archaeology/legacy-sifap .github/agents .github/prompts .github/instructions .github/skills

# 4. Prepare main na cópia recém-criada e torne-a a branch padrão do time
# Se main já existir localmente, selecione-a; caso contrário, crie-a a partir da cópia.
if git show-ref --verify --quiet refs/heads/main; then
  git checkout main
else
  git checkout -b main
fi
git push -u origin main
gh repo edit <IMMERSION_ORG>/immersion-team-01 --default-branch main

# 5. Crie a branch de integração do time
git checkout -b develop
git push -u origin develop
```

> [!WARNING]
> Deste ponto em diante, nunca faça push direto em `main`. O Passo 4 protege essa branch.

`develop` é onde as branches de feature de todo mundo são integradas. As promoções para `main` acontecem via PR depois de cada estágio.

---

## Passo 4: Proteja a branch `main` (só o líder)

Isso impede que qualquer pessoa, exceto um admin do repositório, faça push direto em `main`. Toda mudança precisa passar por um Pull Request.

> [!NOTE]
> Faça essa configuração somente no repositório do seu time. Se a opção de proteção não estiver disponível, peça ajuda para verificar as permissões da organização.

### Usando o site

- [ ] **Crie a regra de proteção.**

1. Vá em **Settings** -> **Branches** (barra lateral esquerda).
2. Em **Branch protection rules**, clique em **Add rule**.
3. Branch name pattern: `main`
4. Marque:
   - **Require a pull request before merging**
   - **Require approvals** - defina como `1`
   - **Require conversation resolution before merging**
5. Clique em **Create**.

### Usando a CLI

```bash
gh api -X PUT "repos/<IMMERSION_ORG>/immersion-team-01/branches/main/protection" \
  --input - <<'JSON'
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false
  },
  "restrictions": null,
  "required_conversation_resolution": true
}
JSON
```

> **Por que isso importa.** Sem essa regra, alguém do time acaba mandando um erro para `main` no minuto 90, e a demo falha no minuto 480. Custo: 30 segundos. Economia: horas.

---

## Passo 5: Adicione os outros quatro integrantes (só o líder)

### Opção A: usar o site

- [ ] **Convide os outros quatro colegas de time.**

1. Abra o repositório no GitHub: `https://github.com/<IMMERSION_ORG>/immersion-team-XX`
2. Clique em **Settings** -> **Collaborators and teams** -> **Manage access**.
3. Clique em **Add people**.
4. Digite o usuário do GitHub e selecione na lista.
5. Escolha o papel **Write** (não Admin, não Read).
6. Clique em **Add ... to this repository**.
7. Repita para as outras três pessoas.

> [!TIP]
> Se os facilitadores criaram um time no GitHub para cada time da imersão, adicione o time inteiro com permissão Write em vez de convidar pessoa por pessoa. Cada pessoa convidada recebe um e-mail e precisa clicar em **Accept invitation** antes de conseguir fazer push.

### Opção B: usar a CLI

```bash
for user in alice bob carla dani; do
  gh api -X PUT "repos/<IMMERSION_ORG>/immersion-team-01/collaborators/${user}" \
    -f permission=write
done
```

---

## Passo 6: Cada integrante clona o repositório

**Agora todo mundo entra.** Os outros quatro integrantes do time fazem isto.

### 6.1 Aceite o convite

- [ ] **Aceite o convite pelo e-mail ou pela notificação do GitHub.**

### 6.2 Clone e mude para `develop`

- [ ] **Clone o repositório e confirme o acesso.**

```bash
mkdir -p ~/Code && cd ~/Code

# Troque 01 pelo número real do seu time e <IMMERSION_ORG> pela organização informada no dia
git clone --branch main https://github.com/<IMMERSION_ORG>/immersion-team-01.git
cd immersion-team-01

# Mude para a branch develop, onde acontece o trabalho do dia a dia
git checkout develop
```

### 6.3 Abra no VS Code

```bash
code .
```

### 6.4 Confirme as ferramentas locais

Este kit não inclui ambiente pronto, protótipo pré-fabricado nem containerização herdada. Cada pessoa valida as próprias ferramentas localmente. O protótipo é criado do zero no Estágio 3.

```bash
git --version
java -version
node --version
docker --version
specify version
```

### 6.5 Confirme que o template veio intacto

```bash
ls 01-archaeology/legacy-sifap .github/agents .github/prompts .github/instructions .github/skills
```

---

## Passo 7: Ative o GitHub Copilot no VS Code (todos)

### 7.1 Entre na sua conta

- [ ] **Autentique no Copilot.**

1. No VS Code, clique no ícone do Copilot na barra de status inferior.
2. Escolha **Sign in with GitHub**.
3. Uma janela do navegador abre. Clique em **Authorize Visual Studio Code**.
4. Volte ao VS Code. Espere aparecer "Copilot ready" perto do canto inferior direito.

### 7.2 Abra o painel do GitHub Copilot

| SO | Atalho |
|---|---|
| Mac | Cmd+Ctrl+I |
| Windows / Linux | Ctrl+Alt+I |

### 7.3 Verifique se os três modos estão disponíveis

| Modo | Quando usar |
|---|---|
| **Ask** | Fazer perguntas, explorar código, discutir opções |
| **Plan** | Planejar mudanças em vários arquivos antes de executar |
| **Agent** | Delegar uma feature inteira por uma Issue e depois revisar o PR |

- [ ] **Confirme que Ask, Plan e Agent aparecem na lista suspensa.**

Se **Plan** ou **Agent** não aparecer, atualize o VS Code para uma versão recente ou use o VS Code Insiders.

### 7.4 Teste de fumaça do Copilot

- [ ] **Envie uma pergunta de teste.**

No modo Ask do GitHub Copilot, digite:

```text
Qual stack estamos usando neste projeto?
```

Ele deve responder **Java 21 + Spring Boot 3.3 + Next.js 15 + PostgreSQL 16**. Se não responder, o arquivo de projeto `.github/copilot-instructions.md` não está sendo carregado. Veja [Solução de problemas](#solução-de-problemas).

---

## Passo 8: Valide os agentes e prompts das suas personas (todos)

### 8.1 Encontre seu papel

- [ ] **Leia o `PERSONA.md` das duas personas.**

Abra `05-personas/` no VS Code. Dentro da pasta de cada papel, leia o `PERSONA.md` do começo ao fim (~10 minutos). Ele diz:

- O que você faz nos quatro estágios
- Qual modo do Copilot usar
- Prompts específicos que você pode copiar e colar
- De quem você depende e quem depende de você

### 8.2 Valide seu kit

```bash
# Deve listar agentes, prompts, instruções e skills consolidados
ls .github/agents .github/prompts .github/instructions .github/skills
```

Não copie `.github/*` na mão. O repositório consolidado já inclui tudo.

### 8.3 Mapeamento de persona para kit

| Persona | Kit consolidado |
|---|---|
| Product Owner | `05-personas/01-product-owner/PERSONA.md` |
| Requirements Engineer | `05-personas/02-requirements-engineer/PERSONA.md` |
| Enterprise Architect | `05-personas/03-enterprise-architect/PERSONA.md` |
| Software Architect | `05-personas/04-software-architect/PERSONA.md` |
| Technical Lead | `05-personas/05-technical-lead/PERSONA.md` |
| Developer | `05-personas/06-developer/PERSONA.md` |
| DBA | `05-personas/07-dba/PERSONA.md` |
| QA Engineer | `05-personas/08-qa-engineer/PERSONA.md` |
| DevOps Engineer | `05-personas/09-devops-engineer/PERSONA.md` |
| Tech Writer | `05-personas/10-tech-writer/PERSONA.md` |

### 8.4 Atualize o `copilot-instructions.md` do time

- [ ] **O líder atualiza `.github/copilot-instructions.md` com os nomes do time.**

Encontre a seção:

```markdown
## Active Personas on This Team

- [ ] 01 — Product Owner
- [ ] 02 — Requirements Engineer
      ...
```

Marque as caixas e escreva o nome ao lado de cada papel:

```markdown
- [x] 01 — Product Owner — Maria Santos
- [x] 02 — Requirements Engineer — João Silva
- [x] 03 — Enterprise Architect — Ana Costa
      ...
```

Faça commit e push para `develop`. As sugestões do Copilot agora sabem quem está no seu time.

---

## Passo 9: Instale o Spec-Kit (todos)

O [**Spec-Kit**](https://github.com/github/spec-kit) é o toolkit oficial do GitHub para desenvolvimento guiado por especificação. Use para **rascunhos rápidos de feature** no Estágio 2.

### 9.1 Instale o Specify CLI no seu laptop

- [ ] **Instale o Specify CLI.**

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
specify version
```

Troque `vX.Y.Z` pela versão mais recente em <https://github.com/github/spec-kit/releases>.

### 9.2 Inicialize no repositório do time

- [ ] **Inicialize na raiz do repositório.**

```bash
specify init . --integration copilot
```

Isso cria a configuração `.specify/`, os scripts de automação e os slash commands `/speckit.*` para o GitHub Copilot.

### 9.3 Verifique os comandos no GitHub Copilot

| Comando | Quando usar |
|---|---|
| `/speckit.constitution` | Definir princípios, padrões e gates do projeto |
| `/speckit.specify` | Criar a spec da feature |
| `/speckit.clarify` | Resolver ambiguidade antes do plano |
| `/speckit.plan` | Criar o plano técnico |
| `/speckit.tasks` | Gerar tarefas implementáveis |
| `/speckit.analyze` | Verificar consistência e cobertura |
| `/speckit.implement` | Implementar a feature guiado pela spec |

### 9.4 Escreva uma feature

No modo Ask do GitHub Copilot:

```text
/speckit.specify <descreva a feature identificada pelo time no código legado>. Preserve a rastreabilidade do legado com source_legacy em cada requisito.
```

O Spec-Kit cria uma branch numerada e esta estrutura:

```text
specs/<NNN>-<feature>/
└── spec.md
```

Depois rode:

```text
/speckit.clarify
/speckit.plan Use Java 21, Spring Boot 3.3, PostgreSQL 16, Next.js 15 e a arquitetura de monolito modular da imersão.
/speckit.tasks
```

### 9.5 Regra da imersão

Todo requisito vindo do sistema legado ainda precisa de `source_legacy:` apontando para um `.NSN` ou `.ddm`. Requisitos sem equivalente no legado usam `[GREENFIELD]` com uma justificativa.

---

## Passo 10: Use o fluxo do Spec-Kit (todos)

| Fase | Comando | Saída principal | Persona responsável |
|---|---|---|---|
| Constituição | `/speckit.constitution` | `.specify/memory/constitution.md` | Technical Lead + Architect |
| Spec | `/speckit.specify` | `specs/<NNN>-<feature>/spec.md` | Requirements Engineer |
| Esclarecimento | `/speckit.clarify` | Dúvidas resolvidas na spec | Requirements Engineer + Product Owner |
| Plano | `/speckit.plan` | `specs/<NNN>-<feature>/plan.md` | Software Architect |
| Tarefas | `/speckit.tasks` | `specs/<NNN>-<feature>/tasks.md` | Technical Lead |
| Análise | `/speckit.analyze` | Lacunas e inconsistências | QA Engineer + Architect |
| Implementação | `/speckit.implement` | Código + testes guiados pela spec | Developer + QA Engineer |

> [!IMPORTANT]
> O time revisa explicitamente `spec.md`, `plan.md` e `tasks.md` antes de a implementação começar (gates de LGTM).

---

## Passo 11: Entenda a estratégia de branches

```text
main                    <- pronta para release, protegida, exige 1 revisão
develop                 <- integração de todas as features
spec/NNN-feature        <- trabalho de especificação (Estágio 2)
impl/NNN-feature        <- trabalho de implementação (Estágio 3)
infra/NNN-azure         <- trabalho de infraestrutura (Estágio 4)
```

### Convenção de nomes

| Tipo | Padrão | Exemplo |
|---|---|---|
| Spec | `spec/<NNN>-<feature>` | `spec/001-calculo-beneficio` |
| Implementação | `impl/<NNN>-<feature>` | `impl/001-calculo-beneficio` |
| Infraestrutura | `infra/<componente>` | `infra/azure-postgres` |

`NNN` é o número da feature (bate com a pasta em `specs/<NNN>-<feature>/`).

### Crie uma branch de feature

- [ ] **Crie uma branch a partir de `develop`.**

```bash
git checkout develop
git pull

git checkout -b spec/<NNN>-<feature>

git add -A
git commit -m "feat: draft EARS requirements"
git push -u origin spec/<NNN>-<feature>
```

### Abra um Pull Request

- [ ] **Abra o PR e preencha o template.**

1. Depois do push, o GitHub imprime uma URL para criar o PR. Clique nela.
2. Título: use Conventional Commits - `feat: add feature spec`
3. Preencha o template (`.github/PULL_REQUEST_TEMPLATE.md`): o que mudou, REQ-IDs, como testar, issues vinculadas.
4. Adicione pelo menos um revisor de outra persona.
5. Clique em **Create pull request**.
6. Espere a CI ficar verde.
7. Depois da aprovação, clique em **Rebase and merge** (não Merge commit, não Squash).
8. Apague a branch de feature quando for perguntado.

---

## Passo 12: Fluxo diário por persona

### Product Owner / Requirements Engineer

```text
1. Leia os achados do Estágio 1 (glossário, catálogo de regras de negócio)
2. Rode /speckit.specify "feature-name" com orientação de source_legacy
3. Rode /speckit.clarify e valide com as personas de stakeholder (PO + EA)
4. Rode /speckit.plan com a stack e as escolhas de arquitetura da imersão
5. Rode /speckit.tasks depois que o plano for aprovado
6. Abra um PR na branch spec/<NNN>-<feature>
7. Passe o trabalho para o Software Architect (gate de LGTM)
```

### Enterprise Architect / Software Architect

```text
1. Faça pull da develop mais recente
2. git checkout spec/NNN-feature (leia a spec EARS)
3. Rode /speckit.plan -> produz plan.md, research.md e contratos
4. Adicione ADRs em docs/adr/ para decisões não triviais
5. Abra um PR e revise a seção de design do PR da spec
6. Passe o trabalho para o Technical Lead (gate de LGTM)
```

### Technical Lead

```text
1. Leia o plan.md aprovado e os ADRs
2. Rode /speckit.tasks -> produz tasks.md com IDs de tarefa (T001, T002, ...)
3. Abra uma GitHub Issue por tarefa usando .github/ISSUE_TEMPLATE/task.yml
4. Atribua cada issue para Developer / DBA / QA
5. Acompanhe a CI verde/vermelha e desbloqueie as pessoas
```

### Developer

```text
1. Pegue uma issue de tarefa (T-NNN) no board do time
2. git checkout -b impl/NNN-feature (a partir de develop)
3. No Copilot, rode /implement (prompt ativo: .github/prompts/persona-developer-implement.prompt.md)
4. Testes primeiro (vermelho), código (verde), refatore
5. Rode o gate local definido pelo protótipo (./mvnw verify, npm test, npm run lint ou equivalente)
6. git commit, git push, abra o PR
7. Marque a issue com "Closes #NN" no corpo do PR
```

### DBA

```text
1. Pegue uma tarefa de schema ou migração
2. git checkout -b impl/NNN-feature
3. Adicione a migração Flyway em backend/src/main/resources/db/migration/
4. Rode o prompt /migration (prompt ativo: .github/prompts/persona-dba-migration.prompt.md)
5. Teste localmente contra o Postgres do time ou com Testcontainers
6. Abra o PR e peça revisão ao Developer
```

### QA Engineer

```text
1. Acompanhe todo PR de implementação
2. Rode o prompt /coverage-gaps para achar REQ-IDs sem cobertura
3. Adicione testes na branch de implementação (em dupla com o Developer)
4. O prompt /test-strategy produz um plano de testes para novas features
5. Bloqueie o merge se a cobertura cair abaixo de 70%
```

### DevOps Engineer

```text
1. Pegue uma tarefa de infraestrutura (config do Azure, CI/CD, deploy)
2. git checkout -b infra/NNN-azure-foo
3. Edite os módulos Terraform em infra/
4. Rode terraform fmt + terraform validate localmente
5. Rode o prompt /iac-module (prompt ativo: .github/prompts/persona-devops-engineer-iac-module.prompt.md)
6. Abra o PR; workflows/ci.yml roda a validação do Terraform
```

### Tech Writer

```text
1. Depois de cada merge em develop, procure drift nos ADRs e no glossário
2. Rode o prompt /doc-drift (prompt ativo: .github/prompts/persona-tech-writer-doc-drift.prompt.md)
3. Atualize 01-archaeology/glossary.md, docs/adr/ e os READMEs
4. Abra um PR pequeno por atualização de documentação
```

---

## Passo 13: Teste de fumaça (time inteiro, às 10:30)

O líder do time lê cada item em voz alta. Cada pessoa confirma o item no próprio laptop.

- [ ] Todos os integrantes clonaram `immersion-team-XX`
- [ ] Todos os integrantes conseguem executar `git checkout develop && git pull origin develop` (acesso de escrita confirmado)
- [ ] A CI rodou no commit inicial do template, com uma marca de verificação verde na aba **Actions**
- [ ] O time confirmou que não existe um protótipo pronto: `backend/`, `frontend/` e os arquivos de Docker/infra serão criados no Estágio 3 quando necessário
- [ ] Em todos os laptops, o GitHub Copilot responde corretamente à pergunta "Qual stack estamos usando neste projeto?"
- [ ] Todos os integrantes instalaram o Spec-Kit oficial: `specify version` exibe uma versão
- [ ] Os comandos `/speckit.*` aparecem no Copilot depois de executar `specify init . --integration copilot`
- [ ] Ao abrir **New issue** no GitHub, aparecem três templates (spec, adr e task)
- [ ] Os cinco integrantes do time aparecem em **Settings** -> **Collaborators** no repositório
- [ ] Cada persona leu seu cartão em `05-personas/XX-role/PERSONA.md`
- [ ] O líder do time atualizou `.github/copilot-instructions.md` com os nomes de todas as pessoas
- [ ] `.github/agents`, `.github/prompts`, `.github/instructions` e `.github/skills` estão presentes e consolidados
- [ ] [`00-TEAM-FLOW.md`](00-TEAM-FLOW.md) foi lido uma vez em voz alta (o cronograma do dia)

Quando os 13 itens estiverem verdes, seu time estará pronto para o **Estágio 1: arqueologia**.

---

## Solução de problemas

<details>
<summary><strong>Erros comuns e como corrigi-los</strong> - clique para expandir</summary>

### O Copilot não lê `copilot-instructions.md`

- O VS Code precisa estar aberto **na raiz do repositório**, não dentro de uma subpasta.
- Reinicie o VS Code depois de editar o arquivo.
- Em **Settings**, confirme que `github.copilot.chat.useProjectInstructions` está definido como `true` (valor padrão na versão 1.93 ou posterior).

### O botão **Use this template** não aparece

- Confirme que você abriu o repositório principal da imersão, não o repositório de outro time.
- Se o botão ainda não aparecer, peça aos facilitadores que confirmem se **Template repository** está habilitado em **Settings** -> **General**.
- Não use **Import repository**. O caminho oficial da imersão é **Use this template**.

### O nome `immersion-team-XX` já está em uso

- Confirme que você está usando o número correto do time.
- Se os facilitadores permitirem, adicione um sufixo curto, por exemplo, `immersion-team-01b`.

### `specify init` falha ou os comandos `/speckit.*` não aparecem

- Confirme que `uv`, Python 3.11 ou posterior e Git estão instalados.
- Execute `specify version` para confirmar que você instalou a CLI oficial.
- Execute `specify init . --integration copilot` novamente na raiz do repositório.
- Recarregue o VS Code: **Command Palette** -> **Developer: Reload Window**.

### A CI falha no primeiro push com a mensagem `no tests found`

- Esse comportamento é esperado. O workflow `ci.yml` executa somente os jobs cujos caminhos foram alterados. Quando o código de backend ou frontend for adicionado, os jobs relevantes serão executados.

### O Docker não está disponível quando o time precisa dele

- As portas 5432, 8080 ou 3000 podem já estar em uso. Execute:

  ```bash
  lsof -i :5432 -i :8080 -i :3000
  ```

  Encerre o processo que está usando a porta (`kill -9 <PID>`) antes de iniciar o ambiente criado pelo time.

- Confirme que o Docker Desktop está **em execução** (o ícone na barra de menus deve estar estático, não animado).

### O modo Agent do Copilot não aparece na lista suspensa

- Atualize o VS Code para a versão **1.93 ou posterior** (ou instale o **VS Code Insiders**).
- Recarregue a janela: **Command Palette** -> **Developer: Reload Window**.

### A mensagem `Permission denied` aparece ao fazer push para `main`

- A proteção da branch (Passo 4) está funcionando. Em vez de fazer push para `main`, abra um Pull Request a partir da sua branch de feature.

### Atualizei `develop`, mas meu IDE ainda mostra o código antigo

- Recarregue a janela do VS Code: **Command Palette** -> **Developer: Reload Window**.
- Se o VS Code ainda mostrar o estado anterior, feche e reabra a pasta do repositório.

### A pasta `.github/` parece estar corrompida

- Não copie manualmente os kits de persona sobre a pasta `.github/` consolidada.
- Se algo parecer corrompido, restaure a pasta com `git checkout develop -- .github/` ou peça ajuda a um facilitador antes de tentar sobrescrever arquivos.

</details>

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Fluxo do time](00-TEAM-FLOW.md)<br/><sub>Cronograma de oito horas, handoffs entre duplas, regra dos 20 minutos e definição de pronto.</sub> | [Visão geral das 10 personas](05-personas/OVERVIEW.md)<br/><sub>Tabela comparativa: dupla, liderança por estágio e padrões para emergências.</sub> |

<sub>[Voltar ao índice do kit](README.md)</sub>
