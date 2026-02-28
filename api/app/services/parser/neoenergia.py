import re
from app.core.utils import normalizar_referencia, extrair_codigo_pagamento
import logging
logger = logging.getLogger(__name__)

def parse(texto):

    logger.debug(f"Parseando texto - {__name__}")

    dados = extrair_dados_principais(texto)
    codigo = extrair_codigo_pagamento(texto)
    unidade = extrair_codigo_unidade(texto)

    logger.debug(f"Dados extraídos: {dados}, Código de pagamento: {codigo}, Unidade: {unidade}")
    return {
        "tipo": "boleto",
        "unidade_consumidora": unidade,
        "referencia": dados["referencia"] if dados else None,
        "valor": dados["valor"] if dados else None,
        "vencimento": dados["vencimento"] if dados else None,
        "codigo_pagamento": codigo,
        "descricao": "conta de energia"
    }    

def extrair_codigo_unidade(texto):

    match = re.search(
        r"(\d{1,3}(?:\.\d{3})*-\d)\s+\d{2}/\d{2}/\d{4}\s+\d+,\d{2}",
        texto
    )

    if match:
        return match.group(1).replace(".", "")

    return None


def extrair_dados_principais(texto):

    padrao = r"([A-Z]{3}/\d{4})\s+(\d+,\d{2})\s+(\d{2}/\d{2}/\d{4})"

    match = re.search(padrao, texto)

    if match:
        return {
            "referencia": normalizar_referencia(match.group(1)),
            "valor": match.group(2),
            "vencimento": match.group(3),
        }

    return None
