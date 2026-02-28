#!/usr/bin/env python3

import os
import glob
import argparse
import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API = "https://contas.wvcardoso.lab/api/v1"
DEFAULT_DIR = os.path.expanduser("~/Downloads/pdf")


def upload(diretorio):
    arquivos = glob.glob(f"{diretorio}/*.pdf") + glob.glob(f"{diretorio}/*.txt")

    if not arquivos:
        print("⚠️ Nenhum arquivo encontrado.")
        return

    for caminho in arquivos:
        nome = os.path.basename(caminho)

        mime = "application/pdf" if nome.endswith(".pdf") else "text/plain"

        print("📤 Enviando:", nome)

        with open(caminho, "rb") as f:
            r = requests.post(
                f"{API}/upload/",
                headers={"X-API-KEY": KEY},
                files={"file": (nome, f, mime)},
                verify=False
            )
            print_json(r)
        
        print("--------------------------------------")

def processar():
    print("🚀 Executando processamento...")
    r = requests.post(
        f"{API}/processar/",
        headers={"X-API-KEY": KEY},
        verify=False
    )
    print_json(r)


def reprocessar():
    print("🔁 Executando reprocessamento...")
    r = requests.post(
        f"{API}/reprocessar/",
        headers={"X-API-KEY": KEY},
        verify=False
    )
    print_json(r)

def erros():    
    r = requests.get(
        f"{API}/upload/all/?status=erro",
        headers={"X-API-KEY": KEY},
        verify=False
    )
    print_json(r)

def get(status):    
    r = requests.get(
        f"{API}/upload/all/?status={status}",
        headers={"X-API-KEY": KEY},
        verify=False
    )    
    print_json(r)


def print_json(response):
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception:
        print(response.text)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Uploader Contas API")
    parser.add_argument(
        "action",
        choices=["upload", "processar", "reprocessar", "erros", "get"],
        help="Ação a ser executada"
    )
    parser.add_argument(
        "--dir",
        default=DEFAULT_DIR,
        help="Diretório dos arquivos (apenas para upload)"
    )
    parser.add_argument(
        "--status",
        help="Status para filtrar (apenas para custom)"
    )

    args = parser.parse_args()
    
    if args.action == "erros":
        erros()
    
    elif args.action == "get":
        get(args.status)

    elif args.action == "upload":
        upload(args.dir)

    elif args.action == "processar":
        processar()

    elif args.action == "reprocessar":
        reprocessar()


"""
Use os comandos abaixo para interagir com a API:

python3 contasctl.py get --status processado  | jq .
python3 contasctl.py get --status enviados    | jq .
python3 contasctl.py get --status erro        | jq .

"""