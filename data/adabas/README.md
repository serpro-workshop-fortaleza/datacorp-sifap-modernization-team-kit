# Massa sintética completa de benefícios

> **Trilha:** [Kit do Time](../../README.md) › **Dados Adabas**

Use o mesmo conjunto de registros para preparar a carga do Adabas, consultar o legado e conferir a migração para PostgreSQL, sem inventar outra massa para as telas.

| Campo | Valor |
|---|---|
| **Público-alvo** | DBA, QA, desenvolvimento e operação autorizada |
| **Pré-requisitos** | Python 3.10+; para a importação local, PostgreSQL 16 e `psql` |
| **Estágios** | Arqueologia e implementação |
| **Resultado esperado** | Dados completos e comparação campo a campo |

## O que está incluído

**Todos os dados são sintéticos.** Não foram extraídos de pessoas reais nem de produção. CPF, NIS, contas, contatos, hashes e valores existem apenas para testes. Identificadores com dígitos verificadores válidos não autorizam seu uso em serviços reais.

| Arquivo Adabas | DDM | Snapshot legível | Registros | Campos elementares | Bytes por registro fixo |
|---|---|---|---:|---:|---:|
| 150 — beneficiários | [BENEFIC](../../01-archaeology/legacy-sifap/adabas-ddms/BENEFIC.ddm) | [beneficiary.jsonl](snapshot/beneficiary.jsonl) | 500 | 69 | 1.739 |
| 151 — programas | [SOCPROG](../../01-archaeology/legacy-sifap/adabas-ddms/SOCPROG.ddm) | [social-program.jsonl](snapshot/social-program.jsonl) | 6 | 41 | 361 |
| 152 — pagamentos | [PAYMENT](../../01-archaeology/legacy-sifap/adabas-ddms/PAYMENT.ddm) | [payment.jsonl](snapshot/payment.jsonl) | 2.000 | 57 | 855 |
| 153 — auditoria | [AUDIT](../../01-archaeology/legacy-sifap/adabas-ddms/AUDIT.ddm) | [audit.jsonl](snapshot/audit.jsonl) | 200 | 32 | 4.995 |

Os seis programas são `PBF1`, `BPC1`, `PETI`, `AUX1`, `GASF` e `IDOS`. Cada beneficiário possui quatro pagamentos, nas competências `201710`, `201711`, `201712` e `201801`.

**Completo significa preservar todos os campos físicos dos quatro DDMs**, incluindo endereço, benefício, banco, datas de processamento, descontos, conciliação, controle e auditoria. Inclui todas as posições dos grupos periódicos e dos campos multivalorados: dez dependentes, oito descontos, faixas e regiões dos programas, telefones e vinte posições de antes/depois da auditoria.

Campos opcionais continuam vazios ou zerados quando assim estavam na origem. Descritores derivados não são novas colunas de dados. Esta massa não cobre todos os estados e combinações de regras possíveis.

## Uma única origem, sem novo sorteio

O [manifesto](manifest.json) registra a identificação da fixture, o commit de origem, os SHA-256 dos DDMs e snapshots e os hashes dos quatro arquivos binários originais do laboratório. Também fixa os hashes das entradas ADACMP produzidas pelo conversor original, comparadas byte a byte com as deste pacote.

- A referência histórica é **14/03/2018**, não a data atual.
- O JSONL é uma conversão sem perda da massa original, não uma nova execução de um gerador aleatório.
- A verificação reconstrói os `.dat` e exige igualdade de SHA-256 com os originais.
- A preparação deriva o layout dos DDMs atuais e não altera o corpus legado.
- Não se presume que o banco online ainda corresponda ao snapshot. A operação precisa conferir isso antes da demonstração.

Cada linha JSONL representa um registro. Campos `N` são strings com zeros à esquerda; campos `P` são strings decimais exatas, com ponto e escala preservada. Campos PE/MU são arrays de strings, alinhados pelo índice. Não converta CPF, NIS ou valores monetários automaticamente para números de ponto flutuante.

## Verificar e preparar

Na raiz do repositório:

```bash
python3 data/adabas/seed.py verify
python3 data/adabas/seed.py prepare
```

Esses comandos **não conectam a nenhum banco**, não executam Natural e não provisionam infraestrutura. A pasta gerada, `data/adabas/generated/`, é ignorada pelo Git:

| Saída gerada | Uso |
|---|---|
| `adabas/*.dat` | Registros fixos idênticos à massa binária original |
| `adabas/*.cmpin` | Entrada do ADACMP, com prefixo de comprimento e contadores PE/MU |
| `adabas/*.cmp` | Parâmetro `RECORD_STRUCTURE=E4LENGTH_PREFIX` |
| `adabas/layout-*.txt` | Campos, escalas, ocorrências e offsets de base zero |
| `*.csv` | Todos os campos dos quatro arquivos, com cabeçalhos DDM |
| `postgres-load.sql` | Carga transacional no schema isolado `sifap_seed` |
| `postgres-export.sql` | Exportação consistente e somente leitura para `actual/` |
| `summary.json` | Contagens, situações, totais por competência e anomalias observadas |
| `checksums.json` | SHA-256 dos arquivos preparados |

Para gerar fora dessa pasta:

```bash
python3 data/adabas/seed.py prepare --output /tmp/sifap-benefits
```

Repetir a preparação substitui somente os arquivos de saída previstos; não modifica o snapshot nem apaga os exports em `actual/`. Não edite os arquivos gerados como se fossem uma nova origem.

### Formato físico do Adabas

Os `.dat` contêm **BCD binário**, não apenas texto. Cada registro tem a largura da tabela mais um byte LF. Não use `splitlines()` binário, conversão de encoding ou um editor de texto nesses arquivos.

O `.cmpin` usa comprimento de quatro bytes little-endian, excluindo o próprio prefixo. Cada MU ou PE começa com um contador de um byte. Os PE são transpostos de ordem por campo para ordem por ocorrência, preservando todas as posições da massa original. Esse é o contrato do conversor do laboratório Adabas CE 7.4.0; outras versões ou plataformas exigem validação operacional.

## Carregar e conferir

Siga o [roteiro de carga, consulta e reconciliação](../../docs/benefits-data.md):

1. **Adabas:** a operação autorizada recebe o pacote e carrega uma cópia aprovada com os arquivos vazios. O perfil `viewer` nunca realiza essa etapa.
2. **Natural:** o time consulta os registros pelo visualizador, sem cadastros ou jobs batch.
3. **PostgreSQL:** o time importa os CSVs em um banco local de desenvolvimento, no schema `sifap_seed`.
4. **Aplicação modernizada:** o time mapeia os dados desse schema para suas tabelas de domínio e faz as telas consultarem a API. O kit não contém uma aplicação pronta.
5. **Reconciliação:** os dados exportados são comparados com a origem:

```bash
python3 data/adabas/seed.py compare --actual-dir data/adabas/generated/actual
```

A comparação verifica todos os campos de todos os registros, identifica chaves ausentes/duplicadas e não depende da ordem das linhas. Normaliza escalas numéricas equivalentes e espaços de formatação de arrays JSON, mas **não arredonda valores divergentes** nem corrige dados.

## Anomalias preservadas

A massa original contém casos didáticos e inconsistências. A migração não deve escondê-los:

| Observação medida | Quantidade |
|---|---:|
| Pagamentos em que bruto menos desconto difere do líquido | 20 |
| Pagamentos pendentes com data de confirmação preenchida | 288 |
| Pagamentos sem indicador de estorno, mas com origem preenchida | 1.976 |

Os vinte desequilíbrios monetários foram incluídos na massa para exercícios de relatórios. As outras contagens registram inconsistências observadas, sem presumir que sejam regras corretas do domínio. Não interprete uma data isolada como prova de crédito e não use o snapshot como oráculo de um cálculo novo: ele é referência de **dados armazenados**.

Uma correção de negócio exige decisão rastreável e uma nova versão da fixture. Nunca atualize apenas os hashes para fazer a verificação passar.

## Testes

Sem instalar dependências Python:

```bash
python3 -m unittest discover -s data/adabas/tests -v
```

Os testes cobrem completude, precisão, zeros à esquerda, vínculos, Maria, preservação binária, contadores/ordem PE/MU, determinismo e rejeição de exports alterados. O job `adabas-seed` da [CI](../../.github/workflows/ci.yml) também importa e exporta a massa em PostgreSQL 16 real e verifica que uma segunda carga é recusada sem substituir o schema.

Essas verificações não equivalem a executar ADACMP/ADAMUP ou a observar as telas no laboratório online. A evidência operacional precisa ser obtida separadamente pelo facilitador.
