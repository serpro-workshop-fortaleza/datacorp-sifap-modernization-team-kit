# Carregar e conferir os dados de benefícios

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Dados de benefícios**

Use a mesma massa sintética no Adabas e no banco modernizado para demonstrar registros comparáveis, não telas preenchidas com dados diferentes.

| Campo | Valor |
|---|---|
| **Público-alvo** | Time inteiro; carga Adabas somente pela operação autorizada |
| **Pré-requisitos** | [Acesso ao legado](legacy-system-access.md), Python 3.10+ e, para a etapa local, PostgreSQL 16 com `psql` |
| **Estágios** | Arqueologia e implementação |
| **Resultado esperado** | Mesmo beneficiário, programa e histórico conferidos na origem e no destino |

## Dados disponíveis

O pacote [data/adabas](../data/adabas/README.md) contém **500 beneficiários, seis programas, 2.000 pagamentos e 200 eventos de auditoria**. Todos os campos elementares dos quatro DDMs estão presentes, inclusive PE/MU. Os [snapshots JSONL](../data/adabas/snapshot/) podem ser abertos no VS Code e pesquisados por CPF, NIS ou número do benefício.

> [!IMPORTANT]
> São dados sintéticos históricos, não dados de produção nem extrato atualizado do ambiente online. Algumas inconsistências da massa original foram preservadas para os exercícios. Não apresente registros pendentes como pagamentos recebidos.

## 1. Preparar o pacote sem acessar bancos

Na raiz do repositório:

```bash
python3 data/adabas/seed.py verify
python3 data/adabas/seed.py prepare
```

- [ ] Os quatro arquivos passaram na verificação de hash, formato, vínculos e totais.
- [ ] O pacote foi gerado em `data/adabas/generated/`.
- [ ] O time registrou a fixture `sifap-benefits-20180314-v1`.
- [ ] Nenhuma senha, conexão real ou dado de produção foi incluído nos arquivos.

A preparação pode ser repetida. Ela não executa os SQLs nem faz carga automática no Adabas.

## 2. Popular o Adabas — operação autorizada

**Participantes não executam esta etapa pelo visualizador.** O laboratório compartilhado continua externo e somente leitura para o time. O pacote permite à operação levar a mesma massa ao seu procedimento autorizado, sem publicar credenciais ou infraestrutura administrativa neste repositório.

### Pré-condições obrigatórias

- [ ] A operação autorizou uma cópia de laboratório descartável ou uma janela formal de carga.
- [ ] DBID, arquivos 150–153 e biblioteca Natural foram conferidos; não se presumiu que o DBID `057` da listagem histórica seja o destino real.
- [ ] Os quatro arquivos estão criados, **vazios**, com FDTs compatíveis com os DDMs, campos únicos e descritores necessários às consultas.
- [ ] A operação conferiu o campo `CPF-REPRESENTATIVE` de `BENEFIC`; a listagem FDT histórica não substitui os DDMs atuais.
- [ ] A imagem/runtime e as ferramentas foram validados. O contrato deste pacote é Adabas CE 7.4.0.
- [ ] A sessão de escrita não é a conta `viewer`; a carga é executada no ambiente operacional apropriado, não na tela de consulta.
- [ ] Existe plano de retorno aprovado. Não se apagam arquivos nem registros para repetir a carga.

Se qualquer arquivo já contiver dados, **pare**. `add` não é um mecanismo de atualização idempotente. Uma tentativa anterior parcial exige análise da operação, não repetição indiscriminada.

### Entrada para o carregador

Entregue à operação a pasta gerada `adabas/`, o [manifesto](../data/adabas/manifest.json) e `checksums.json`. A ordem de carga é:

| Ordem | Arquivo | Entrada ADACMP | Registros esperados |
|---:|---:|---|---:|
| 1 | 151 | `social-program.cmpin` | 6 |
| 2 | 150 | `beneficiary.cmpin` | 500 |
| 3 | 152 | `payment.cmpin` | 2.000 |
| 4 | 153 | `audit.cmpin` | 200 |

Os `.dat` também são fornecidos para o procedimento operacional que já usa o conversor do laboratório. **Escolha apenas uma rota:** `.dat` pelo conversor existente ou `.cmpin` já preparado. Não carregue as duas.

O bloco abaixo documenta o contrato dos utilitários no **shell operacional de uma cópia autorizada com arquivos vazios**. Não é comando Natural, SQL, instrução para a conta `viewer` nem procedimento de provisionamento do laboratório compartilhado.

Depois que a operação definir `ADABAS_DBID` com o destino conferido e entrar na pasta `adabas/` preparada:

```bash
set -euo pipefail
: "${ADABAS_DBID:?A operacao deve informar e conferir o DBID autorizado}"
command -v adacmp
command -v adamup

for entry in social-program:151 beneficiary:150 payment:152 audit:153; do
  name="${entry%:*}"
  file="${entry#*:}"
  export CMPIN="$PWD/$name.cmpin"
  export CMPDTA="$PWD/$name.CMPDTA"
  export CMPDVT="$PWD/$name.CMPDVT"
  export MUPDTA="$CMPDTA"
  export MUPDVT="$CMPDVT"

  if [ -e "$CMPDTA" ] || [ -e "$CMPDVT" ]; then
    printf 'Pare: ja existem produtos de uma tentativa anterior.\n' >&2
    exit 1
  fi

  printf 'dbid=%s\nfile=%s\nRECORD_STRUCTURE=E4LENGTH_PREFIX\n' \
    "$ADABAS_DBID" "$file" | adacmp
  adamup "db=$ADABAS_DBID" "update=$file,add"
done
```

`adacmp` comprime conforme a FDT já instalada; `adamup` grava os registros. Não execute `ADAFDU`, criação de arquivos, exclusões ou `--force` a partir do kit do time. A escolha de outro carregador, como ADALOD, depende do runtime e do procedimento privado da operação; não é intercambiável por suposição.

### Evidência após a carga

- [ ] ADACMP informou **zero registros incorretos** em cada arquivo.
- [ ] Os quatro arquivos contêm exatamente as contagens da tabela, sem misturar outra massa.
- [ ] Os descritores usados por CPF e NIS resolvem o mesmo beneficiário.
- [ ] A consulta apresenta a Maria e os quatro pagamentos abaixo.
- [ ] A operação registrou versão da fixture, destino, data, contagens e resultado, sem credenciais ou identificadores pessoais em logs.
- [ ] O time foi informado se o ambiente online difere do snapshot.

Este repositório não inclui licença/runtime Adabas e sua CI não executa esses utilitários. A aprovação dessa etapa depende da verificação operacional real.

## 3. Conferir a Maria no Natural

Abra o [visualizador compartilhado](legacy-system-access.md) com `viewer`. Ele deve apresentar o formulário de `VIEWBENF`. Se aparecer um menu de desenvolvimento ou uma linha de comandos, avise o facilitador; não tente ampliar o acesso.

1. No formulário, selecione o tipo de pesquisa `C`.
2. Use Tab para chegar ao campo CPF e informe `78933359478`.
3. Pressione Enter; quando aparecer `MORE`, pressione Enter para continuar.
4. Confira cadastro e histórico.
5. Ao retornar ao formulário, repita com tipo `N` e NIS `28566181479`.
6. Encerre pela tecla PF3/F3 conforme o mapeamento do terminal.

### Cadastro esperado

| Campo | Valor sintético |
|---|---|
| Nome | MARIA MARTINS OLIVEIRA |
| CPF para pesquisa | `78933359478` |
| CPF mascarado | `***.***.594-78` |
| NIS | `28566181479` |
| Nascimento | `19460612` — 12/06/1946 |
| Município/UF | FORTALEZA / CE |
| Programa | `PBF1` |
| Situação do cadastro | `A` — ativo |
| Renda familiar | R$ 1.000,00 |
| Dependentes | 0 |
| Região | `02` |
| Data de cadastro | `20110524` — 24/05/2011 |

### Histórico esperado

| Competência | Bruto | Desconto | Líquido | Situação | Tipo |
|---|---:|---:|---:|---|---|
| `201710` | 236,67 | 0,00 | 236,67 | `P` | `N` |
| `201711` | 236,67 | 0,00 | 236,67 | `P` | `N` |
| `201712` | 236,67 | 0,00 | 236,67 | `P` | `A` |
| `201801` | 236,67 | 0,00 | 236,67 | `P` | `N` |

`P` é pendente; `N` é normal; `A`, na coluna de tipo, é abono. A consulta padrão mostra bruto e líquido, mas não uma coluna separada de desconto. Cadastro ativo não implica pagamento confirmado.

A fonte [CONSBENF](../01-archaeology/legacy-sifap/natural-programs/CONSBENF.NSP) apresenta até doze pagamentos por CPF, sem garantir ordem decrescente de competência. `VIEWBENF` é a variante operacional somente leitura; o programa original registra auditoria e não deve ser usado como substituto pelo participante.

Os campos de geração, emissão, confirmação, crédito, cancelamento, desconto detalhado e conciliação estão no [snapshot completo de pagamentos](../data/adabas/snapshot/payment.jsonl). Eles não aparecem todos na tela Natural. Não execute batch para preencher uma data durante a apresentação.

## 4. Popular o PostgreSQL local para conferência

Use um banco **local de desenvolvimento/teste**, nunca produção. Configure a conexão fora do repositório, por exemplo com um serviço `sifap-local` em seu `pg_service.conf` e senha em `.pgpass` com permissões restritas. A instrução abaixo pressupõe que esse serviço já existe e aponta para o banco conferido.

Na raiz do repositório, após preparar os arquivos:

```bash
cd data/adabas/generated
PGSERVICE=sifap-local psql -X --file=postgres-load.sql
```

O script:

- cria somente `sifap_seed`, com quatro tabelas e todos os campos;
- preserva identificadores, datas legadas e zeros como `text`, decimais como `numeric` e PE/MU como `jsonb`;
- verifica chaves únicas, vínculos entre beneficiário/programa/pagamento e contagens;
- carrega tudo em uma única transação com interrupção em erro;
- **recusa um schema `sifap_seed` já existente**, sem apagar, truncar ou sobrescrever registros.

Uma segunda execução deve falhar com “schema already exists”. Isso é uma proteção, não uma orientação para apagar o schema. Reutilize o carregado para conferir; para um novo ensaio, escolha outro banco descartável autorizado.

### Ver o mesmo cadastro e histórico no banco

Execute em uma sessão SQL conectada ao banco local:

```sql
SELECT b.num_registration, b.num_benefit, b.full_name,
       b.num_nis, b.city, b.uf, b.stat_beneficiary,
       s.cod_program, s.name_program, b.amt_family_income,
       b.qty_depend, b.dt_registration
FROM sifap_seed.beneficiary AS b
JOIN sifap_seed.social_program AS s USING (cod_program)
WHERE b.num_cpf = '78933359478';

SELECT num_payment, year_month_ref, amt_gross, amt_disc_total,
       amt_net, stat_payment, type_payment, dt_generation,
       dt_issue, dt_confirmation, dt_credit
FROM sifap_seed.payment
WHERE num_cpf = '78933359478'
ORDER BY year_month_ref, num_payment;
```

Os valores são sintéticos, mas o hábito de não publicar consultas com dados identificáveis em logs ou capturas continua válido.

### Comparar todos os registros, não só a Maria

Ainda em `data/adabas/generated/`:

```bash
PGSERVICE=sifap-local psql -X --file=postgres-export.sql
cd ../../..
python3 data/adabas/seed.py compare --actual-dir data/adabas/generated/actual
```

A exportação usa uma transação consistente e somente leitura. O comparador exige os mesmos 2.706 registros e todos os campos. Uma alteração de valor, campo, vínculo ou quantidade reprova a conferência.

## 5. Fazer os dados aparecerem no modernizado

**O schema de conferência não preenche uma aplicação automaticamente.** O time ainda cria `backend/` e `frontend/` no [Estágio 3](../03-implementation/GUIDE.md).

- [ ] Mapear os campos do snapshot para as entidades/tabelas do recorte escolhido, preservando as chaves legadas.
- [ ] Criar uma importação de desenvolvimento/teste para as tabelas de domínio, em vez de copiar valores para componentes da interface.
- [ ] Preservar dinheiro em `BigDecimal`/`numeric`; não arredondar ou recalcular pagamentos já armazenados.
- [ ] Definir explicitamente a conversão de datas zeradas para ausência e tratar datas/horas inválidas como achados, não como correções silenciosas.
- [ ] Mapear PE/MU mantendo a relação entre campos de uma ocorrência; não tratar dez posições como dez dependentes ativos.
- [ ] Fazer o endpoint do recorte consultar os registros persistidos, seguindo `/api/v1/{resource}`.
- [ ] Fazer as telas consumir esse endpoint e conferir o mesmo CPF/NIS, situação, programa e quatro pagamentos da Maria.
- [ ] Criar um teste de integração da importação/consulta e um teste da interface ligados aos REQ-IDs definidos pelo time.
- [ ] Exportar o destino no contrato dos CSVs DDM e usar `compare` para o pacote completo. Para um recorte menor, documentar a cobertura e escrever a comparação correspondente; não afirmar equivalência de toda a massa.

O SQL de exportação fornecido consulta **somente `sifap_seed`**. Passar nessa comparação comprova a cópia de conferência, não a persistência nas tabelas de domínio nem o funcionamento da UI. Para verificar a migração real, adapte a consulta de exportação ao schema da aplicação e registre essa evidência separadamente.

## Totais de controle

Os totais históricos estão no [manifesto](../data/adabas/manifest.json) e em `summary.json` após a preparação:

| Competência | Pagamentos | Bruto | Desconto | Líquido armazenado |
|---|---:|---:|---:|---:|
| `201710` | 500 | 160.077,84 | 2.190,80 | 157.887,19 |
| `201711` | 500 | 160.077,84 | 2.190,80 | 157.887,19 |
| `201712` | 500 | 181.771,34 | 2.853,01 | 178.918,48 |
| `201801` | 500 | 160.143,31 | 2.190,80 | 157.952,66 |

Há vinte desequilíbrios monetários preservados. Portanto, não “corrija” a coluna de líquido para igualar a subtração durante a importação. O valor de referência é o armazenado, e a inconsistência deve continuar visível.

## Se algo divergir

| Sintoma | Próxima ação |
|---|---|
| SHA-256 ou layout divergente | Pare a preparação; reveja a versão da fixture e do DDM |
| Maria ausente no visualizador | Peça à operação a conferência da carga; não cadastre outra Maria |
| Contagem acima do esperado no Adabas | Pare; pode haver mistura de massas ou carga duplicada |
| ADACMP rejeitou um registro | Não avance; confira FDT, framing e versão do runtime |
| Schema PostgreSQL já existe | Reutilize para leitura ou escolha outro banco local descartável |
| Comparação CSV falhou | Investigue arquivo, linha e campo informados; não atualize a origem para esconder a diferença |
| PostgreSQL correto, mas tela vazia | Confira importação de domínio, conexão usada pela API e consulta da UI |

---

### Continue lendo

| Anterior | Próximo |
|---|---|
| [Acesso somente leitura ao legado](legacy-system-access.md) | [Guia de implementação](../03-implementation/GUIDE.md) |
