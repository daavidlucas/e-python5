import csv
import re


class FormatoInvalidoError(Exception):
    pass


class IdadeInvalidaError(Exception):
    pass


PADRAO_EMAIL = r"^[\w.\-]+@[\w\-]+(\.[\w\-]+)+$"
PADRAO_CPF = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
PADRAO_TELEFONE = r"^\(\d{2}\)\s?9?\d{4}-\d{4}$"
PADRAO_DATA = r"^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$"


def validar_email(valor):
    if not re.match(PADRAO_EMAIL, valor):
        raise FormatoInvalidoError(f"E-mail invalido: {valor}")


def validar_cpf(valor):
    if not re.match(PADRAO_CPF, valor):
        raise FormatoInvalidoError(f"CPF invalido: {valor}")


def validar_telefone(valor):
    if not re.match(PADRAO_TELEFONE, valor):
        raise FormatoInvalidoError(f"Telefone invalido: {valor}")


def validar_data(valor):
    if not re.match(PADRAO_DATA, valor):
        raise FormatoInvalidoError(f"Data invalida: {valor}")


def validar_idade(valor):
    idade = int(valor)
    if idade < 0 or idade > 120:
        raise IdadeInvalidaError(f"Idade fora do intervalo permitido: {idade}")


def analisar(caminho):
    validos = []
    invalidos = []
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        for numero, linha in enumerate(leitor, start=2):
            try:
                linha["nome"]
                validar_email(linha["email"])
                validar_cpf(linha["cpf"])
                validar_telefone(linha["telefone"])
                validar_data(linha["data"])
                validar_idade(linha["idade"])
            except (FormatoInvalidoError, IdadeInvalidaError) as erro:
                invalidos.append((numero, linha, str(erro)))
            except ValueError:
                invalidos.append((numero, linha, f"Idade nao numerica: {linha['idade']}"))
            else:
                validos.append(linha)
    return validos, invalidos


def gerar_relatorio(validos, invalidos):
    total = len(validos) + len(invalidos)
    taxa = (len(validos) / total * 100) if total else 0.0
    idades = [int(r["idade"]) for r in validos]
    media = sum(idades) / len(idades) if idades else 0.0

    linhas = [
        "=" * 64,
        f"{'RELATORIO DE ANALISE DE DADOS':^64}",
        "=" * 64,
        "",
        "ESTATISTICAS",
        f"Total de registros: {total}",
        f"Registros validos: {len(validos)}",
        f"Registros invalidos: {len(invalidos)}",
        f"Taxa de aprovacao: {taxa:.1f}%",
        f"Idade media dos validos: {media:.1f} anos",
        "",
        "REGISTROS VALIDOS",
    ]
    for r in validos:
        linhas.append(f"{r['nome']:<16} {r['email']:<28} {r['cpf']}")
    linhas.append("")
    linhas.append("REGISTROS INVALIDOS")
    for numero, r, motivo in invalidos:
        linhas.append(f"Linha {numero:>2} | {r['nome']:<16} | {motivo}")
    linhas.append("=" * 64)
    return "\n".join(linhas)


def main():
    caminho = input("Arquivo de dados (Enter para dados.csv): ").strip() or "dados.csv"
    try:
        validos, invalidos = analisar(caminho)
    except FileNotFoundError:
        print(f"Erro: arquivo nao encontrado: {caminho}")
    except KeyError as erro:
        print(f"Erro: coluna ausente no arquivo: {erro}")
    else:
        relatorio = gerar_relatorio(validos, invalidos)
        print(relatorio)
        with open("relatorio.txt", "w", encoding="utf-8") as saida:
            saida.write(relatorio)
    finally:
        print("Analise finalizada.")


if __name__ == "__main__":
    main()
