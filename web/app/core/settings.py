import os

class Settings:

    # Configurações de segurança e acesso
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    USUARIO = os.getenv("APP_USER", "admin")
    SENHA_HASH = os.getenv("APP_PASSWORD_HASH", "")

    # Configurações da API
    API_URL: str = os.getenv("API_URL", "http://0.0.0.0:8000")   # url da parte do backend com fastapi
    API_KEY: str = os.getenv("API_KEY")              # Chave de API para autenticação
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")    # Prefixo para as rotas da API

settings = Settings()