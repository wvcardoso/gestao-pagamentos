from app.core.utils import normalizar_referencia

def parse(texto):

    dados = {}

    for linha in texto.split("\n"):

        linha_lower = linha.lower()

        if ":" not in linha:
            continue

        chave, valor = linha.split(":", 1)

        chave = chave.strip().lower()
        valor = valor.strip().replace('"', '')

        if chave == "referencia":
            valor = normalizar_referencia(valor)

        dados[chave] = valor

    return dados
