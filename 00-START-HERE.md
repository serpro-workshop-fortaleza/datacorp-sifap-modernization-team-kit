# Primeiros 15 minutos: comece aqui

> **Trilha:** [Kit do time](README.md) › **Comece aqui**

**Idioma:** português do Brasil (`portugues-br`). Este é o ponto de entrada do kit dos participantes.

**Se você acabou de chegar e quer saber "e agora, o que eu faço?", esta página é para você.** Não importa se você é Product Owner, Tech Writer, Developer, analista de negócio ou DBA. Os 15 minutos abaixo funcionam para todo mundo.

![Comece](https://img.shields.io/badge/Comece-00-171717?style=flat-square) ![Duração: 15 min](https://img.shields.io/badge/Dura%C3%A7%C3%A3o-15%20min-737373?style=flat-square) ![Público: time inteiro](https://img.shields.io/badge/P%C3%BAblico-Time%20inteiro-A3A3A3?style=flat-square)

| Campo | Valor |
|---|---|
| **Público-alvo** | Qualquer participante, independentemente do perfil técnico |
| **Pré-requisitos** | Nenhum - isto é só leitura |
| **Tempo estimado** | 15 minutos |
| **Estágio** | Aquecimento (antes do Estágio 1) |
| **Resultado esperado** | Você sabe em qual dupla está, o que faz hoje e o que acontece no Estágio 1 |

---

## Cronograma dos 15 minutos

| Minuto | O que fazer | Tempo |
|---|---|---|
| 0-2 | Passo 1 - Confirme sua dupla | 2 min |
| 2-4 | Passo 2 - Abra o cronograma do dia | 2 min |
| 4-6 | Passo 3 - Abra o glossário visual | 2 min |
| 6-11 | Passo 4 - Leia o `PERSONA.md` do seu papel | 5 min |
| 11-15 | Passo 5 - Abra o Estágio 1 e o cartão de referência do Copilot | 4 min |

> [!NOTE]
> Ainda falta o setup técnico completo? Tudo bem. Estes 15 minutos são só leitura. O setup técnico vem depois, guiado por `00-SETUP.md`.

---

## Passo 1: Confirme sua dupla (2 min)

O time tem **cinco pessoas e 10 personas** (cada pessoa cobre duas personas, em uma dupla).

| Dupla | Personas | O que você faz |
|---|---|---|
| **1 - Visão** | Product Owner + Requirements Engineer | Decide **o que** será modernizado |
| **2 - Arquitetura** | Enterprise Architect + Software Architect | Decide **como** o sistema é organizado |
| **3 - Implementação** | Technical Lead + Developer | Escreve o **código** |
| **4 - Qualidade** | DBA + QA Engineer | Cuida dos **dados** e dos **testes** |
| **5 - Operações** | DevOps Engineer + Tech Writer | Cuida do **deploy** e da **documentação** |

- [ ] **Confirme sua dupla.** Pergunte ao facilitador em qual dupla você está. Anote: Minha dupla: _______ - Minhas personas: _______ + _______

> [!TIP]
> Você não é programador? Tudo bem. PO, RE, Tech Writer e parte de QA não precisam programar. Toda persona tem uma missão clara. Você não vai passar o dia assistindo alguém compilar Java em silêncio.

---

## Passo 2: Abra o cronograma do dia (2 min)

- [ ] **Abra `00-TEAM-FLOW.md` em uma aba.** Olhe só o cronograma. O dia tem quatro estágios.

![Timeline do dia: pré-evento, quatro estágios e demo, com os três handoffs H1, H2 e H3](assets/timeline-stages.svg)

**No que prestar atenção:**

- Você não pode pular estágios. O Estágio 2 depende do que sai do Estágio 1.
- **Existe um handoff entre estágios** - a dupla de um estágio passa o trabalho para a dupla seguinte (um sync ao vivo de cinco minutos). É isso que mantém o dia andando.
- Se você ficar bloqueado por mais de **20 minutos**, levante a mão. Essa regra vale para todos os times.

---

## Passo 3: Abra o glossário visual (2 min)

Você vai ver siglas e termos técnicos hoje (EARS, ADR, REQ-ID, DDM, Flyway, JPA...). Você não precisa memorizar nenhum deles. Abra esta página em uma aba e volte quando precisar:

[`07-concepts/03-visual-glossary.md`](07-concepts/03-visual-glossary.md)

Cada termo tem três linhas: **o que é**, uma **analogia do dia a dia** e **onde aparece**. Use à vontade.

- [ ] **Abra o glossário em uma aba do navegador ou do VS Code.**

> **Exemplo:** o termo "EARS" pode parecer intimidante. O glossário traduz assim: "um jeito padronizado de escrever requisitos sem ambiguidade - cada requisito segue um template com condição, sujeito, ação e resultado esperado."

---

## Passo 4: Leia o `PERSONA.md` do seu papel (5 min)

Você tem **duas personas**. Leia o `PERSONA.md` de cada uma:

```text
05-personas/01-product-owner/PERSONA.md
05-personas/02-requirements-engineer/PERSONA.md
05-personas/03-enterprise-architect/PERSONA.md
05-personas/04-software-architect/PERSONA.md
05-personas/05-technical-lead/PERSONA.md
05-personas/06-developer/PERSONA.md
05-personas/07-dba/PERSONA.md
05-personas/08-qa-engineer/PERSONA.md
05-personas/09-devops-engineer/PERSONA.md
05-personas/10-tech-writer/PERSONA.md
```

- [ ] **Leia o `PERSONA.md` da persona A.**
- [ ] **Leia o `PERSONA.md` da persona B.**

**Foque em três seções de cada `PERSONA.md`:**

1. **"Onde você aparece em cada estágio"** - uma tabela de quatro linhas. Ela mostra se você lidera, apoia ou observa em cada estágio.
2. **"Se você travar (padrões de emergência)"** - o que fazer quando se sentir perdido.
3. **"Três prompts de exemplo"** - prompts prontos para copiar e colar no Copilot.

> [!TIP]
> Se suas duas personas parecerem "a mesma coisa", olhe **quando** cada uma lidera. Elas raramente lideram juntas. É por isso que duas personas em uma dupla conseguem cobrir o dia inteiro sem ficar ociosas.

---

## Passo 5: Abra o Estágio 1 e o cartão de referência do Copilot (4 min)

### 5a. Abra o guia do Estágio 1

[`01-archaeology/GUIDE.md`](01-archaeology/GUIDE.md)

Leia só:

- A seção **"Passo a passo cronometrado"** (entregáveis do Estágio 1)
- A tabela **"Quem lê o quê"** (quais três programas Natural sua dupla lê)
- O cronograma **11:00-12:00 + 13:30-14:00** (o que sua dupla faz no Estágio 1)

- [ ] **Leia a seção "Passo a passo cronometrado" do `GUIDE.md` do Estágio 1.**

### 5b. Abra o cartão de referência dos três modos do Copilot

[`09-cheat-sheets/copilot-3-modes.md`](09-cheat-sheets/copilot-3-modes.md)

Isso economiza 30 minutos de confusão. O Copilot tem três modos:

| Modo | Quando usar | Exemplo no Sistema de Fiscalização e Administração de Pagamentos (SIFAP) |
|---|---|---|
| **Ask** | Você quer entender alguma coisa | *"Explique esta seção do subprograma Natural CALCBENF.NSN"* |
| **Plan** | Você quer mudar código com cuidado | *"Planeje a validação de CPF. Mostre o plano antes de mudar qualquer coisa."* |
| **Agent** | Você quer delegar uma feature inteira | Issue do Estágio 4 para o Copilot Agent |

- [ ] **Abra o cartão de referência em uma aba.**

### 5c. Se você nunca abriu o GitHub Copilot

- VS Code -> ícone do Copilot na barra de atividades -> abra o chat
- Não vê o ícone? Pergunte ao facilitador. A extensão pode não estar habilitada.

---

## Checklist dos primeiros 15 minutos

Antes de seguir, verifique isto:

- [ ] Sei em qual dupla estou e quais duas personas eu tenho
- [ ] Estou com `00-TEAM-FLOW.md` aberto em uma aba (o cronograma do dia)
- [ ] Estou com `visual-glossary.md` aberto em outra aba (para consultar o jargão)
- [ ] Li os arquivos `PERSONA.md` das minhas duas personas (e foquei nas três seções recomendadas)
- [ ] Sei o que vai acontecer no Estágio 1
- [ ] Conheço os três modos do Copilot (Ask, Plan, Agent)

Se tudo estiver marcado, **você está pronto**. Vá para o setup técnico (`00-SETUP.md`) ou direto para o Estágio 1, conforme o cronograma do dia.

---

## Primeira hora: passo a passo minuto a minuto (para quem nunca usou VS Code ou Copilot)

Se você nunca abriu VS Code, Docker ou Copilot, este passo a passo literal deixa você pronto em 60 minutos. Siga **na ordem**, sem pular passos.

> [!TIP]
> Faça isso com alguém da sua dupla ao lado. Duas pessoas resolvem problemas de setup na metade do tempo.

| Minuto | Ação | Como saber que funcionou |
|---:|---|---|
| **00** | Abra um terminal e rode `cd ~/Code/immersion-team-XX` | O nome do repositório aparece no prompt |
| **02** | Rode `code .` para abrir o VS Code | O VS Code abre e mostra a lista de pastas (`00-...`, `01-...`) |
| **04** | Abra o terminal integrado (`` Ctrl+` ``) e rode `git status` | A branch e o estado do repositório aparecem sem erro |
| **08** | Valide as ferramentas: `java -version`, `node --version`, `git --version` | Cada comando imprime uma versão |
| **13** | Valide o Docker (não suba nada ainda): `docker --version` | O comando imprime uma versão do Docker |
| **18** | Valide o Spec-Kit: `specify version` | O comando imprime uma versão do Specify CLI |
| **20** | Abra o painel do GitHub Copilot pelo ícone na barra de atividades do VS Code | O painel do GitHub Copilot abre à direita |
| **22** | No chat, digite: *"Olá. O que você consegue fazer?"* | O Copilot responde e explica os três modos |
| **25** | Selecione o agente do dia na lista suspensa do chat | Você vê `@archaeologist`, `@architect`, `@builder` e `@evolution` na lista |
| **28** | Abra duas abas no navegador: [`00-TEAM-FLOW.md`](00-TEAM-FLOW.md) e [`07-concepts/03-visual-glossary.md`](07-concepts/03-visual-glossary.md) | Duas abas fixadas continuam abertas para consulta |
| **32** | Abra as pastas das suas duas personas em `05-personas/0X-.../` e leia cada `PERSONA.md` | Você sabe suas duas missões do dia |
| **42** | Valide o `.github/` consolidado: `ls .github/agents .github/prompts .github/skills` | As pastas existem e já contêm agentes, prompts e skills |
| **45** | Recarregue o VS Code: `Cmd+Shift+P` -> *Reload Window* | Slash commands como `/ears-convert` aparecem quando você digita `/` no Chat |
| **50** | Abra [`01-archaeology/GUIDE.md`](01-archaeology/GUIDE.md) e leia a seção "Quem lê o quê" | Você sabe quais três programas `.NSN` sua dupla vai ler |
| **55** | Combine com sua dupla quem cobre qual persona | Vocês dois sabem quem faz o quê |
| **60** | Você está pronto para começar o Estágio 1 | - |

### Se algo travar neste passo a passo

| Travou em... | Vá para |
|---|---|
| Minuto 04 (terminal/Git) | [`docs/troubleshooting.md`](docs/troubleshooting.md) - seção *Setup* |
| Minuto 13 (Docker) | [`docs/troubleshooting.md`](docs/troubleshooting.md) - seção *Docker* |
| Minuto 20 (o Copilot não abre) | [`docs/troubleshooting.md`](docs/troubleshooting.md) - seção *Copilot* |
| Minuto 45 (o slash command não funciona) | [`docs/troubleshooting.md`](docs/troubleshooting.md) - seção *"Slash command não aparece"* |

> [!WARNING]
> Bloqueado por mais de 20 minutos? Pare e peça ajuda. Essa regra está definida em `00-TEAM-FLOW.md` §6.

---

## Situações comuns nos primeiros 15 minutos

<details>
<summary><strong>FAQ - clique para expandir</strong></summary>

| Situação | O que fazer |
|---|---|
| Não sei em qual dupla estou | Pergunte ao facilitador da sala |
| Não encontro meu `PERSONA.md` | A pasta é `05-personas/0X-name/PERSONA.md` - confirme o número no Passo 1 |
| Um termo do glossário ainda não está claro | Abra `07-concepts/03-visual-glossary.md` e use Ctrl+F |
| O VS Code ou o Copilot não abre | Vá para `00-SETUP.md` § "Passo 1: Verifique os pré-requisitos do seu laptop" |
| O cronograma parece muito apertado | E está mesmo. Confie na divisão em duplas. Você não vai fazer tudo sozinho |
| Eu não programo. Vou me perder? | Não. Veja `01-archaeology/legacy-sifap/HOW-TO-READ-NATURAL.md` (para o Estágio 1) e os padrões do seu `PERSONA.md` |

</details>

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Kit do time](README.md)<br/><sub>Hub principal deste repositório. Comece por ele se esta é a primeira vez que você abre o kit.</sub> | [Fluxo do time](00-TEAM-FLOW.md)<br/><sub>Cronograma de 8 horas, handoffs entre duplas, regra dos 20 minutos, definição de pronto.</sub> |

<sub>[Voltar ao índice do kit](README.md)</sub>
