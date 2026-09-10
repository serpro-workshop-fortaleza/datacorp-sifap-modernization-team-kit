# Modelo de runbook do time

![Tipo: runbook](https://img.shields.io/badge/Tipo-Manual%20operacional-171717?style=flat-square)
![Responsável: DevOps](https://img.shields.io/badge/Respons%C3%A1vel-DevOps-737373?style=flat-square)

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Runbook**

**Modelo para documentar como executar, verificar e diagnosticar a solução criada pelos participantes.**
Preencha-o com comandos e evidências do próprio time; ele não descreve nem dá acesso a ambientes do instrutor.

| Campo | Valor |
|---|---|
| **Público-alvo** | DevOps Engineer e o time inteiro |
| **Pré-requisitos** | Setup local concluído conforme [`00-SETUP.md`](../00-SETUP.md) |
| **Resultado esperado** | Execução da solução do time documentada, CI compreensível e bloqueios registrados |

---

## Verificações iniciais (primeiro uso)

- [ ] **Verifique os pré-requisitos** — execute cada linha e confirme que nenhum erro ocorre:

```bash
git --version
java -version
node --version
docker --version
specify version
```

> [!NOTE]
> O kit não inclui um protótipo pronto. Quando o time criar `backend/`, `frontend/` e, se necessário, `infra/`, registre aqui os comandos reais de execução.

Depois de criar o protótipo, documente:

| Serviço | URL / Comando |
|---|---|
| Health do backend | — |
| Swagger UI | — |
| Frontend local | — |
| Forma de configurar a autenticação local, sem registrar senhas | — |

---

## Rotina diária

- [ ] **Verifique o estado do repositório:**

```bash
git status
```

- [ ] **Execute os testes do backend** (quando `backend/` existir):

```bash
cd backend && ./mvnw test
```

- [ ] **Execute os testes do frontend** (quando `frontend/` existir):

```bash
cd frontend && pnpm test
```

---

## CI — Entenda os fluxos de trabalho

A CI também cobre a edição `portugues-br` do template. No repositório do time, acompanha o fluxo de `main`, `develop`, `spec/**` e `impl/**`.

| Arquivo de fluxo de trabalho | O que verifica | Quando é executado |
|---|---|---|
| `ci.yml` | Backend `mvn verify`, frontend lint + test + typecheck, Terraform fmt + validate | Em cada push e PR |
| `spec-quality.yml` | markdownlint e rastreabilidade dos REQ-IDs | Quando arquivos `.md` ou `specs/` mudam |

- [ ] **Quando a CI falhar** — abra a aba Actions no GitHub, selecione a execução que falhou e leia o log.
- [ ] **Corrija localmente** — reproduza o erro com os comandos do protótipo criado pelo time antes de fazer outro push.

---

## Infraestrutura criada pelo time — Estágio 4

O kit não inclui recursos provisionados, arquivos de estado nem configuração de uma assinatura.
Se o escopo do time incluir infraestrutura, use o [guia do Estágio 4](../04-evolution/GUIDE.md) e documente somente o que a equipe criar.

- [ ] Registre os módulos e arquivos de configuração realmente existentes.
- [ ] Registre os comandos de validação e o resultado da revisão do plano.
- [ ] Confirme permissões e limites antes de qualquer implantação.
- [ ] Descreva a autenticação sem versionar segredos, tokens ou arquivos de estado.
- [ ] Se não houver implantação, registre essa limitação; não apresente um ambiente como pronto.

---

## Problemas comuns

| Sintoma | Causa provável | Correção | Como confirmar |
|---|---|---|---|
| O ambiente local trava | A porta 5432, 8080 ou 3000 já está em uso | Execute `lsof -i :5432` e encerre o processo | O serviço inicia sem erro de porta |
| `mvn verify` falha no Testcontainers | O Docker não está em execução | Inicie o Docker Desktop | Os testes passam na próxima execução |
| `pnpm test` falha nos snapshots | O componente foi alterado intencionalmente | Execute `pnpm test -- -u` para atualizar os snapshots | Os testes passam após a atualização |
| O plano de infraestrutura é rejeitado | A configuração não atende aos limites ou políticas autorizados para o time | Leia o diagnóstico e revise o plano antes de implantar | O plano revisado passa nas validações |
| O GitHub Actions não consegue acessar o Azure | A configuração de autenticação não corresponde ao repositório, à branch ou ao ambiente do time | Confira a configuração OIDC autorizada e solicite ajuda ao responsável pelo acesso | O fluxo de trabalho autentica sem segredos versionados |

---

## Quando escalar para o facilitador

- [ ] O build falha há mais de 20 minutos sem solução.
- [ ] A assinatura do Azure parece estar suspensa.
- [ ] Uma ação irreversível foi executada por engano, como `terraform destroy`.

Use o formato de escalonamento em três linhas descrito em [`00-TEAM-FLOW.md §4`](../00-TEAM-FLOW.md).

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [FAQ](FAQ.md)<br/><sub>Perguntas frequentes.</sub> | [Solução de problemas](troubleshooting.md)<br/><sub>Erros comuns e soluções.</sub> |

<sub>[Voltar ao índice do kit](README.md)</sub>
