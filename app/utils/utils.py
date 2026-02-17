import pdfplumber
import re
import json
from datetime import datetime
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import os
from config import RESIDENCIAS_FILE
import qrcode


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

def extrair_texto_pdf(caminho_pdf):
    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            conteudo = pagina.extract_text()

            #print(conteudo)

            if conteudo:
                texto += conteudo + "\n"

    return texto

def normalizar_referencia(ref):
    meses = {
        "JAN": "01", "FEV": "02", "MAR": "03", "ABR": "04",
        "MAI": "05", "JUN": "06", "JUL": "07", "AGO": "08",
        "SET": "09", "OUT": "10", "NOV": "11", "DEZ": "12"
    }

    # Caso: JAN/2026
    if ref[:3].isalpha():
        mes = meses.get(ref[:3].upper())
        ano = ref[4:]
        return f"{ano}-{mes}"

    # Caso: 02/2026
    else:
        mes, ano = ref.split("/")
        return f"{ano}-{mes}"

def identificar_favorecido(texto):
    if "CONSUMO KWh" in texto:
        return "neoenergia"
    elif "COMPANHIA DE SANEAMENTO AMBIENTAL DO DISTRITO FEDERAL" in texto:
        return "caesb"
    else:
        return "desconhecido"
    
def carregar_residencias():
    caminho = os.path.join(RESIDENCIAS_FILE)

    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def extrair_texto_txt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()
    
def encontrar_residencia_por_codigo(codigo, mapa):
    
    for chave, dados in mapa.items():
    
        for tipo, valor in dados.items():
            
            if tipo != "nome" and valor == codigo:
                return dados["nome"]

    return "Desconhecida"

def salvar_qrcode_imagem(imagem, path):
    imagem.save(path)


def extrair_qrcode_pdf(caminho_pdf):
    imagens = convert_from_path(caminho_pdf, dpi=300)

    for i, imagem in enumerate(imagens):
        img_cv = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)

        qrcodes = decode(img_cv)

        for qr in qrcodes:
            dados = qr.data.decode("utf-8")
            return dados  # conteúdo do QR

    return None