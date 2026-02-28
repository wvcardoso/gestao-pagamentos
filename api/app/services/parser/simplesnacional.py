import re
from app.core.utils import normalizar_referencia


def parse(texto):

    valor = extrair_valor(texto)
    vencimento = extrair_vencimento(texto)
    referencia = extrair_referencia(texto)
    codigo = extrair_codigo_barras(texto)

    return {
        "tipo": "boleto",
        "favorecido": "simplesnacional",
        "residencia": None,
        "unidade_consumidora": None,
        "valor": valor,
        "vencimento": vencimento,
        "referencia": referencia,
        "codigo_pagamento": codigo,
        "descricao": "DAS - Simples Nacional"
    }

def extrair_valor(texto):
    match = re.search(r"Valor\s+Total\s+do\s+Documento\s+(\d+,\d{2})", texto, re.IGNORECASE)

    if match:
        return match.group(1)

    # fallback (OCR bagunçado)
    match = re.search(r"Valor[:\s]+(\d+,\d{2})", texto)
    if match:
        return match.group(1)

    return None

def extrair_vencimento(texto):

    # prioridade → pagar até
    match = re.search(r"Pagar\s+até[:\s]+(\d{2}/\d{2}/\d{4})", texto, re.IGNORECASE)
    if match:
        return match.group(1)

    # fallback
    match = re.search(r"Data\s+de\s+Vencimento\s+(\d{2}/\d{2}/\d{4})", texto)
    if match:
        return match.group(1)

    return None


def extrair_referencia(texto):

    match = re.search(r"(Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro)/(\d{4})", texto, re.IGNORECASE)

    if match:
        return normalizar_referencia(f"{match.group(1)}/{match.group(2)}")

    return None


def extrair_codigo_barras(texto):

    match = re.search(r"(\d{11}\s\d\s\d{11}\s\d\s\d{11}\s\d\s\d{11}\s\d)", texto)

    if match:
        return match.group(1).replace(" ", "")

    return None


def tem_pix(texto):
    return "PIX" in texto.upper()