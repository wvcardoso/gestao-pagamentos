import os

# 📍 Diretório base do projeto (raiz)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📁 Pasta de dados
DATA_DIR = os.path.join(BASE_DIR, "data")

# 📄 Arquivos específicos
RESIDENCIAS_FILE = os.path.join(DATA_DIR, "residencias.json")
DB_FILE = os.path.join(DATA_DIR, "contas.db")

# 📂 Pastas de arquivos
ENTRADA_DIR = os.path.join(DATA_DIR, "entrada")
PROCESSADOS_DIR = os.path.join(DATA_DIR, "processados")
ERRO_DIR = os.path.join(DATA_DIR, "erro")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
USUARIO = os.getenv("APP_USER", "admin")
SENHA_HASH = os.getenv("APP_PASSWORD_HASH", "")