import pdfplumber
import re
import json
from pdf2image import convert_from_bytes
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import os
from app.core.settings import settings
import hashlib
from io import BytesIO

import logging
logger = logging.getLogger(__name__)

def calcular_hash(file_obj):
    hasher = hashlib.sha256()

    while chunk := file_obj.read(8192):
        hasher.update(chunk)

    file_obj.seek(0)  # importante resetar ponteiro
    return hasher.hexdigest()

def extrair_codigo_pagamento(texto):
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)

    # pega qualquer sequência grande que começa com 8
    candidatos = re.findall(r"8\d{30,50}", texto)

    for c in candidatos:
        if len(c) == 48:
            return c

    # fallback com blocos
    padrao = r"(8\d{11}\s\d{11,12}\s\d{11,12}\s\d{11,12})"
    match = re.search(padrao, texto)

    if match:
        return match.group(1)

    return None


'''
def extrair_texto_pdf(caminho_pdf):      

    try:
        texto = ""

        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                conteudo = pagina.extract_text()
                texto += conteudo or "\n"

        # 🔍 valida qualidade
        if precisa_ocr(caminho_pdf):
            raise ValueError("Texto insuficiente ou ruim")

        return texto

    except Exception as e:

        print(f"⚠️ Falha no pdfplumber: {e}")
        print("➡️ Partindo para OCR...")

        from PIL import Image, ImageEnhance, ImageFilter
        import pytesseract
        import fitz

        doc = fitz.open(caminho_pdf)
        texto_total = ""

        for i, page in enumerate(doc):  # ✅ corrigido

            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            # 🔥 preprocessamento
            img = img.convert("L")
            img = img.filter(ImageFilter.SHARPEN)

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)

            texto = pytesseract.image_to_string(
                img,
                lang="por",
                config="--oem 3 --psm 6"
            )

            texto_total += texto + "\n"

        print("✅ OCR finalizado")

        return texto_total
'''

def texto_eh_ruim(texto: str) -> bool:
    if not texto or not texto.strip():
        return True

    # muitos cid?
    if "(cid:" in texto:
        return True

    # poucos caracteres alfanuméricos?
    letras = re.findall(r"[A-Za-z0-9]", texto)
    if len(letras) < 20:
        return True

    return False


def extrair_texto_pdf(arquivo_pdf: BytesIO) -> str:
    """
    Extrai texto de PDF.
    Tenta primeiro via pdfplumber.
    Se texto for insuficiente, faz OCR.
    """
    logger.debug(f"Iniciando extração de texto do PDF")

    texto = ""

    try:
        logger.debug("Tentando extrair texto com pdfplumber")
        with pdfplumber.open(arquivo_pdf) as pdf:
            for pagina in pdf.pages:
                conteudo = pagina.extract_text()
                if conteudo:
                    texto += conteudo + "\n"

        if texto_eh_ruim(texto):            
            logger.warning("Texto inválido ou corrompido. Iniciando OCR.")
            arquivo_pdf.seek(0)
            return _extrair_texto_pdf_ocr(arquivo_pdf)     

        logger.debug(f"texto extraído {texto}")
        return texto

    except Exception as e:
        logger.warning(f"Falha ao extrair texto com pdfplumber: {e}. Iniciando OCR.")
        return _extrair_texto_pdf_ocr(arquivo_pdf)

def _extrair_texto_pdf_ocr(arquivo_pdf: BytesIO) -> str:

    from PIL import Image, ImageEnhance, ImageFilter
    import pytesseract
    import fitz

    logger.debug("Iniciando OCR")

    arquivo_pdf.seek(0)  # 🔥 ESSENCIAL

    doc = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")

    texto_total = ""

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img = img.convert("L")
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageEnhance.Contrast(img).enhance(2)

        texto = pytesseract.image_to_string(
            img,
            lang="por",
            config="--oem 3 --psm 6"
        )

        texto_total += texto + "\n"

    logger.debug(f"Texto extraído via OCR: {texto_total}")
    logger.debug(f"OCR finalizado")
    arquivo_pdf.seek(0)

    return texto_total

def normalizar_referencia(ref):
    ref = ref.strip().upper()

    meses = {
        "JAN": "01", "JANEIRO": "01",
        "FEV": "02", "FEVEREIRO": "02",
        "MAR": "03", "MARÇO": "03", "MARCO": "03",
        "ABR": "04", "ABRIL": "04",
        "MAI": "05", "MAIO": "05",
        "JUN": "06", "JUNHO": "06",
        "JUL": "07", "JULHO": "07",
        "AGO": "08", "AGOSTO": "08",
        "SET": "09", "SETEMBRO": "09",
        "OUT": "10", "OUTUBRO": "10",
        "NOV": "11", "NOVEMBRO": "11",
        "DEZ": "12", "DEZEMBRO": "12"
    }

    # 🔹 Remove espaços tipo "Janeiro / 2026"
    ref = re.sub(r"\s*/\s*", "/", ref)

    # 🔹 Caso número: 02/2026
    if re.match(r"\d{2}/\d{4}", ref):
        mes, ano = ref.split("/")
        return f"{mes}/{ano}"

    # 🔹 Caso texto: JAN/2026 ou JANEIRO/2026
    match = re.match(r"([A-ZÇ]+)\/(\d{4})", ref)

    if match:
        mes_texto = match.group(1)
        ano = match.group(2)

        mes = meses.get(mes_texto)

        if mes:
            return f"{mes}/{ano}"

    return None


def identificar_favorecido(texto):
    if "CONSUMO KWh" in texto:
        return "neoenergia"
    elif "COMPANHIA DE SANEAMENTO AMBIENTAL DO DISTRITO FEDERAL" in texto:
        return "caesb"
    elif "SIMPLES NACIONAL" in texto.upper():
        return "simplesnacional"
    else:
        return "desconhecido"
    
def carregar_residencias():

    caminho = os.path.join(settings.RESIDENCIAS_FILE)
    
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")    

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def extrair_texto_txt(arquivo_bytes):

    arquivo_bytes.seek(0)
    conteudo = arquivo_bytes.read()

    try:
        return conteudo.decode("utf-8")
    except UnicodeDecodeError:
        # fallback comum
        return conteudo.decode("latin-1")
    
def encontrar_residencia_por_codigo(codigo, mapa):
    
    for chave, dados in mapa.items():
    
        for tipo, valor in dados.items():
            
            if tipo != "nome" and valor == codigo:
                return dados["nome"]

    return "Desconhecida"

def salvar_qrcode_imagem(imagem, path):
    imagem.save(path)

def extrair_qrcode_pdf(arquivo_pdf_bytes):
    """
    Extrai QRCode de PDF em memória (BytesIO).
    """

    try:
        # ⚠️ se for BytesIO, precisamos pegar os bytes reais
        if hasattr(arquivo_pdf_bytes, "getvalue"):
            pdf_bytes = arquivo_pdf_bytes.getvalue()
        else:
            pdf_bytes = arquivo_pdf_bytes

        imagens = convert_from_bytes(pdf_bytes, dpi=300)

        for imagem in imagens:

            img_cv = cv2.cvtColor(
                np.array(imagem),
                cv2.COLOR_RGB2BGR
            )

            qrcodes = decode(img_cv)

            for qr in qrcodes:
                dados = qr.data.decode("utf-8")
                logger.info("QRCode encontrado no PDF")
                return dados

        logger.info("Nenhum QRCode encontrado")
        return None

    except Exception as e:
        logger.error(f"Erro ao extrair QRCode: {e}")
        return None

def log(msg):
    print(f"[APP] {msg}", flush=True)

def precisa_ocr(caminho):
    import fitz  # pymupdf
    
    doc = fitz.open(caminho)

    texto_total = ""

    for page in doc[:3]:  # amostra
        texto = page.get_text()
        texto_total += texto

    texto_limpo = texto_total.strip()

    # 🔹 1. Sem texto relevante
    if len(texto_limpo) < 50:
        return True

    # 🔹 2. Poucos espaços → texto colado/quebrado
    if texto_limpo.count(" ") < 5:
        return True

    # 🔹 3. Poucas palavras reais
    palavras = re.findall(r"\b[a-zA-Z]{3,}\b", texto_limpo)
    if len(palavras) < 5:
        return True

    # 🔹 4. Muito caractere estranho
    proporcao_estranha = sum(1 for c in texto_limpo if not c.isalnum() and c not in " .,:\n") / len(texto_limpo)
    if proporcao_estranha > 0.3:
        return True

    return False
