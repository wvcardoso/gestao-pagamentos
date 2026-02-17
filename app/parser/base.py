from utils import (
    extrair_texto_pdf,
    extrair_texto_txt,
    identificar_favorecido,
    extrair_qrcode_pdf,
    encontrar_residencia_por_codigo,
    carregar_residencias,
)

from parser import neoenergia, caesb, manual

PARSERS = {
    "neoenergia": neoenergia,
    "caesb": caesb,
}


def processar(caminho):

    mapa_residencias = carregar_residencias()

    # =========================
    # 📄 PDF
    # =========================
    if caminho.endswith(".pdf"):

        texto = extrair_texto_pdf(caminho)
        favorecido = identificar_favorecido(texto)

        parser = PARSERS.get(favorecido)

        if not parser:
            print("❌ Parser não encontrado")
            return None

        dados = parser.parse(texto)

        # QR Code
        qr = extrair_qrcode_pdf(caminho)
        if qr:
            dados["pix_payload"] = qr

        # favorecido
        dados["favorecido"] = favorecido

        # residência
        unidade = dados.get("unidade_consumidora")

        if unidade:
            unidade = str(unidade).strip()
            residencia = encontrar_residencia_por_codigo(unidade, mapa_residencias)
        else:
            residencia = "Desconhecida"

        dados["residencia"] = residencia

        return dados

    # =========================
    # 📝 TXT
    # =========================
    elif caminho.endswith(".txt"):

        texto = extrair_texto_txt(caminho)
        dados = manual.parse(texto)

        # favorecido
        #dados["favorecido"] = favorecido

        # residência
        unidade = dados.get("unidade_consumidora")

        if unidade:
            unidade = str(unidade).strip()
            residencia = encontrar_residencia_por_codigo(unidade, mapa_residencias)
        else:
            residencia = "Desconhecida"

        dados["residencia"] = residencia
        
        pix = dados.get("pix")
        if pix:
            dados["pix_payload"] = pix

        return dados

    else:
        print("⚠️ Tipo de arquivo não suportado")
        return None
