import re
from utils import normalizar_referencia, extrair_codigo_pagamento


def parse(texto):

    dados = extrair_dados_principais(texto)
    codigo = extrair_codigo_pagamento(texto)
    unidade = extrair_codigo_unidade(texto)

    return {
        "tipo": "boleto",
        "unidade_consumidora": unidade,
        "referencia": dados["referencia"] if dados else None,
        "valor": dados["valor"] if dados else None,
        "vencimento": dados["vencimento"] if dados else None,
        "codigo_pagamento": codigo,
        "descricao": "conta de agua"
    }


def extrair_codigo_unidade(texto):

    match = re.search(r"INSCRIÇÃO:\s*(\d+-\d+)", texto)
    if match:
        return match.group(1)

    return None


def extrair_dados_principais(texto):

    padrao = r"\d+-\d+\s+(\d{2}/\d{4})\s+\d+\s+(\d{2}/\d{2}/\d{4})\s+(\d+,\d{2})"

    match = re.search(padrao, texto)

    if match:
        return {
            "referencia": normalizar_referencia(match.group(1)),
            "vencimento": match.group(2),
            "valor": match.group(3),
        }

    return None
