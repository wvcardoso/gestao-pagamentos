from app.core.settings import settings
import json

# Criar diretórios se não existirem
def ensure_directories():
    
    for directory in [
        settings.DATA_DIR,
        settings.ENTRADA_DIR,
        settings.PROCESSADOS_DIR,
        settings.ERRO_DIR,
        settings.FILES_DIR,
    ]:
        print(f"Ensuring directory exists: {directory}")
        directory.mkdir(parents=True, exist_ok=True)

# Criar arquivos se não existirem
def ensure_files():
    # Criar residencias.json vazio se não existir
    if not settings.RESIDENCIAS_FILE.exists():
        with settings.RESIDENCIAS_FILE.open("w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

# Files e Folders se não existir
def create_infra():
    ensure_directories()
    ensure_files()