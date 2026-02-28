from pathlib import Path
import os

class Settings:

    API_KEY: str | None = os.getenv("API_KEY")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")

    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "/data"))

    ENTRADA_DIR: Path = DATA_DIR / "entrada"
    PROCESSADOS_DIR: Path = DATA_DIR / "processados"
    ERRO_DIR: Path = DATA_DIR / "erro"
    FILES_DIR: Path = DATA_DIR / "dados"

    RESIDENCIAS_FILE: Path = FILES_DIR / "residencias.json"
    DB_FILE: Path = FILES_DIR / "contas.db"

    DIR_ORIGEM: Path = Path(os.getenv("DIR_ORIGEM", "/data/entrada"))
    DIR_DESTINO: Path = Path(os.getenv("DIR_DESTINO", "/data/entrada"))
    DIR_LOG: Path = Path(os.getenv("DIR_LOG", "/data/sync.log"))


settings = Settings()