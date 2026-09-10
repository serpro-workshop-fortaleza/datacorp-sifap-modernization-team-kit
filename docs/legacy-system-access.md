# Sistema legado compartilhado — acesso de consulta

> **Trilha:** [Kit do Time](../README.md) › [Documentação](README.md) › **Visualizador do legado**

A imersão oferece um ambiente Natural/Adabas compartilhado com dados sintéticos do SIFAP. Participantes usam um perfil restrito de consulta; o facilitador opera o ambiente separadamente.

## Entre no sistema

| Campo | Valor |
|---|---|
| URL | <https://sifap-lab-438k30.eastus2.cloudapp.azure.com/terminal/> |
| Usuário | `viewer` |
| Senha | Compartilhada em particular pelo facilitador |

## Permissões do visualizador

O terminal de consulta abre o programa Natural gerado `VIEWBENF`.

- Pode consultar dados de beneficiários e histórico de pagamentos.
- Não possui caminho de escrita no Adabas.
- Não pode abrir o console de administração do Adabas.
- Não pode acessar a linha de comando do Natural.
- Não pode executar programas de cadastro ou jobs batch.
- Não pode implantar, iniciar, parar nem configurar recursos do Azure.

O visualizador fornece acesso somente leitura no nível da aplicação a um runtime compartilhado. Ele não é um tenant separado nem uma cópia privada do banco de dados.

## Dados para conferir

Use o [roteiro de dados de benefícios](benefits-data.md) para consultar a Maria por CPF/NIS e comparar os quatro pagamentos esperados. O [pacote de dados completo](../data/adabas/README.md) contém os registros sintéticos dos quatro arquivos Adabas, com preparação offline de carga, exportação CSV e importação local no PostgreSQL.

O snapshot não comprova o estado atual do ambiente online. Se os dados divergirem, peça ao facilitador que confira a carga; não execute manutenção pelo visualizador.

## Se o acesso falhar

1. Confirme que você usou a URL exata com `/terminal/`.
2. Confirme que o usuário é `viewer`.
3. Peça ao facilitador que verifique a senha atual e o estado do ambiente.

Não tente provisionar, reparar nem administrar o laboratório compartilhado a partir deste repositório.

---

<sub>[Voltar ao índice do kit](../README.md)</sub>
