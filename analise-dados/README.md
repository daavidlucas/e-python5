# Sistema de Análise de Dados

Programa em Python que lê um arquivo CSV com e-mail, CPF, telefone, data e idade, valida cada campo com expressões regulares, trata erros com exceções e gera um relatório formatado.

## Como executar

```bash
python main.py
```

O programa pergunta o nome do arquivo. Pressionando Enter, usa o `dados.csv`. O relatório é exibido na tela e salvo em `relatorio.txt`.

## Arquivos

| Arquivo | Função |
|---|---|
| `main.py` | Script principal com validações, exceções e relatório |
| `dados.csv` | Exemplo de entrada com registros válidos e inválidos |
| `dados_sem_coluna.csv` | Entrada de teste sem a coluna `cpf` (gera `KeyError`) |
| `relatorio.txt` | Exemplo de saída gerada pelo programa |

## Validações aplicadas

Todos os padrões usam raw strings (`r"..."`) e as âncoras `^` e `$`, para que o campo inteiro seja conferido e não apenas um trecho dele.

| Campo | Padrão | Justificativa |
|---|---|---|
| E-mail | `^[\w.\-]+@[\w\-]+(\.[\w\-]+)+$` | Exige texto antes do `@` e pelo menos um domínio com ponto depois dele. Por isso `ana.souza@email` é recusado |
| CPF | `^\d{3}\.\d{3}\.\d{3}-\d{2}$` | Exige o formato com pontos e traço (`000.000.000-00`). `12345678900` é recusado |
| Telefone | `^\(\d{2}\)\s?9?\d{4}-\d{4}$` | Aceita DDD entre parênteses, espaço opcional (`\s?`) e o 9 opcional, cobrindo celular e fixo |
| Data | `^(0[1-9]\|[12]\d\|3[01])/(0[1-9]\|1[0-2])/\d{4}$` | Dia de 01 a 31, mês de 01 a 12 e ano com 4 dígitos. `32/01/1999` é recusado |
| Idade | `int()` + regra de negócio | Precisa ser numérica e estar entre 0 e 120 |

A validação por regex confere apenas o formato. Ela não calcula os dígitos verificadores do CPF nem confere se a data existe no calendário (por exemplo, `31/02`).

## Exceções tratadas

| Exceção | Quando ocorre | Como é tratada |
|---|---|---|
| `FileNotFoundError` | O arquivo informado não existe | Mostra mensagem de erro e encerra a análise |
| `KeyError` | Falta uma coluna esperada no CSV | Mostra qual coluna está ausente e encerra a análise |
| `ValueError` | A idade não é um número (ex.: `abc`) | O registro vai para a lista de inválidos |
| `FormatoInvalidoError` | E-mail, CPF, telefone ou data fora do padrão | O registro vai para a lista de inválidos |
| `IdadeInvalidaError` | Idade numérica fora do intervalo de 0 a 120 | O registro vai para a lista de inválidos |

`FormatoInvalidoError` e `IdadeInvalidaError` são exceções personalizadas que herdam de `Exception` e representam regras de negócio do sistema.

O `main()` usa `try/except/else/finally`:
- `try`: chama a análise do arquivo.
- `except`: captura `FileNotFoundError` e `KeyError`.
- `else`: gera e salva o relatório, apenas se não houve erro.
- `finally`: imprime "Analise finalizada." sempre, com ou sem erro.

A leitura e a escrita de arquivos usam `with open(..., encoding="utf-8")`, que fecha o arquivo automaticamente e preserva os acentos.

## Exemplo de entrada (`dados.csv`)

```csv
nome,email,cpf,telefone,data,idade
Maria Silva,maria.silva@email.com,123.456.789-09,(98) 99123-4567,15/03/1995,30
João Pereira,joao_pereira@empresa.com.br,987.654.321-00,(11) 3456-7890,22/07/1988,37
Ana Souza,ana.souza@email,111.222.333-44,(21) 98765-4321,10/10/2000,25
Carlos Lima,carlos.lima@email.com,12345678900,(31) 99876-5432,05/12/1990,35
Beatriz Costa,beatriz@email.com,222.333.444-55,98 99999-1111,18/04/1992,33
Pedro Alves,pedro.alves@email.com,333.444.555-66,(85) 98888-7777,32/01/1999,26
Lucas Rocha,lucas.rocha@email.com,444.555.666-77,(62) 97777-6666,09/09/1985,abc
Fernanda Dias,fernanda.dias@email.com,555.666.777-88,(71) 96666-5555,27/11/1970,150
Rafael Gomes,rafael.gomes@email.com,666.777.888-99,(41) 3333-2222,14/02/2001,24
Julia Martins,julia.martins@email.com,777.888.999-00,(51) 95555-4444,03/06/1998,28
```

## Exemplo de saída (`relatorio.txt`)

```text
================================================================
                 RELATORIO DE ANALISE DE DADOS                  
================================================================

ESTATISTICAS
Total de registros: 10
Registros validos: 4
Registros invalidos: 6
Taxa de aprovacao: 40.0%
Idade media dos validos: 29.8 anos

REGISTROS VALIDOS
Maria Silva      maria.silva@email.com        123.456.789-09
João Pereira     joao_pereira@empresa.com.br  987.654.321-00
Rafael Gomes     rafael.gomes@email.com       666.777.888-99
Julia Martins    julia.martins@email.com      777.888.999-00

REGISTROS INVALIDOS
Linha  4 | Ana Souza        | E-mail invalido: ana.souza@email
Linha  5 | Carlos Lima      | CPF invalido: 12345678900
Linha  6 | Beatriz Costa    | Telefone invalido: 98 99999-1111
Linha  7 | Pedro Alves      | Data invalida: 32/01/1999
Linha  8 | Lucas Rocha      | Idade nao numerica: abc
Linha  9 | Fernanda Dias    | Idade fora do intervalo permitido: 150
================================================================
```

## Exemplos de erro

Arquivo inexistente:

```text
Arquivo de dados (Enter para dados.csv): nao_existe.csv
Erro: arquivo nao encontrado: nao_existe.csv
Analise finalizada.
```

Coluna ausente (`dados_sem_coluna.csv`):

```text
Arquivo de dados (Enter para dados.csv): dados_sem_coluna.csv
Erro: coluna ausente no arquivo: 'cpf'
Analise finalizada.
```
