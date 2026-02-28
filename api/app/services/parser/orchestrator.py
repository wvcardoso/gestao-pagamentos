from pathlib import Path
from .registry import PARSERS
from . import manual
import logging
logger = logging.getLogger(__name__)

from app.core.utils import (
    extrair_texto_pdf,
    extrair_texto_txt,
    identificar_favorecido,
    extrair_qrcode_pdf,
    encontrar_residencia_por_codigo,
    carregar_residencias,
)

def processar_files(nome_original: str, arquivo_bytes):    

    mapa_residencias = carregar_residencias()
    ext = Path(nome_original).suffix.lower()    

    if ext == ".pdf":
        logger.debug(f"parse arquivo PDF: {nome_original}")
        return _processar_pdf(arquivo_bytes, mapa_residencias)

    elif ext == ".txt":
        logger.debug(f"parse arquivo TXT: {nome_original}")
        return _processar_txt(arquivo_bytes, mapa_residencias)

    return None

def _processar_pdf(arquivo_bytes, mapa_residencias):
    
    texto = extrair_texto_pdf(arquivo_bytes)
    
    if not texto or not texto.strip():
        logger.warning("Texto extraído do PDF está vazio")
        return None
    
    favorecido = identificar_favorecido(texto)
    if favorecido == "desconhecido":       
        logger.debug(f"Favorecido não identificado para o parse")
    else:
        logger.debug(f"Favorecido identificado: {favorecido}")
    
    parser = PARSERS.get(favorecido)
    if not parser:
        return None
    dados = parser.parse(texto)    
    dados["favorecido"] = favorecido
    
    qr = extrair_qrcode_pdf(arquivo_bytes)
    if qr:
        logger.debug(f"QR code encontrado: {qr}")
        dados["pix_payload"] = qr    
    
    unidade = dados.get("unidade_consumidora")    

    if unidade:
        residencia = encontrar_residencia_por_codigo(
            str(unidade).strip(),
            mapa_residencias
        )
    else:
        residencia = "Desconhecida"

    dados["residencia"] = residencia

    return dados

def _processar_txt(arquivo_bytes, mapa_residencias):

    # 🔎 valida arquivo recebido
    if not arquivo_bytes:
        logger.warning("Arquivo TXT não foi recebido")
        return None

    # 🔎 valida se está vazio
    if hasattr(arquivo_bytes, "getbuffer"):
        if arquivo_bytes.getbuffer().nbytes == 0:
            logger.warning("Arquivo TXT vazio (0 bytes)")
            return None

        # reset ponteiro (boa prática)
        arquivo_bytes.seek(0)

    texto = extrair_texto_txt(arquivo_bytes)

    # 🔎 valida texto extraído
    if not texto or not texto.strip():
        logger.warning("Texto extraído do TXT está vazio")
        return None

    dados = manual.parse(texto)

    if not dados:
        logger.warning("Parser manual retornou vazio")
        return None

    unidade = dados.get("unidade_consumidora")

    if unidade:
        residencia = encontrar_residencia_por_codigo(
            str(unidade).strip(),
            mapa_residencias
        )
    else:
        residencia = "desconhecida"

    dados["residencia"] = residencia

    if dados.get("pix"):
        dados["pix_payload"] = dados["pix"]

    return dados