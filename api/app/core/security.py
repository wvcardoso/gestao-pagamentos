from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.settings import settings

api_key_header = APIKeyHeader(
    name="X-API-KEY",
    auto_error=False
)

def verificar_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida"
        )