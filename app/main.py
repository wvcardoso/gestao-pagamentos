import os
import shutil

from parser import base
from database import criar_tabela, inserir_conta
from config import ENTRADA_DIR, PROCESSADOS_DIR, ERRO_DIR



def main():

    os.makedirs(ENTRADA_DIR, exist_ok=True)
    os.makedirs(PROCESSADOS_DIR, exist_ok=True)
    os.makedirs(ERRO_DIR, exist_ok=True)

    # 🔹 garante que a tabela existe
    criar_tabela()
    
    for arquivo in os.listdir(ENTRADA_DIR):

        caminho = os.path.join(ENTRADA_DIR, arquivo)

        print(f"\n📄 Arquivo: {arquivo}")

        try:
            dados = base.processar(caminho)

            if not dados:
                raise ValueError("Parser retornou None")

            inserir_conta(dados)

            # ✅ sucesso → move para processados
            destino = os.path.join(PROCESSADOS_DIR, arquivo)
            shutil.move(caminho, destino)
            print(f"✅ Movido para: {destino}")
            print(f"✅ Processado com sucesso → {destino}")

            # 🔹 output
            print("🏷 Tipo:", dados.get("tipo"))
            print("🏢 Favorecido:", dados.get("favorecido"))
            print("🏠 Residência:", dados.get("residencia"))
            print("🔢 UC:", dados.get("unidade_consumidora"))
            print("💰 Valor:", dados.get("valor"))
            print("📅 Vencimento:", dados.get("vencimento"))
            print("📆 Referência:", dados.get("referencia"))
            #print("🔢 Código:", dados.get("codigo_pagamento") || dados.get("pix"))
            print("🔢 Código:", dados.get("codigo_pagamento") or dados.get("pix"))

            if dados.get("pix_payload"):
                print("🔳 QRCode PIX encontrado")

        except Exception as e:

            print(f"❌ Erro ao processar: {e}")

            # ❌ erro → move para erro/
            destino = os.path.join(ERRO_DIR, arquivo)
            shutil.move(caminho, destino)

            print(f"🚨 Movido para erro → {destino}")

if __name__ == "__main__":
    main()
