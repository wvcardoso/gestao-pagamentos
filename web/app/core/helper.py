import requests
from app.core.settings import settings

def api_post(endpoint):
    return requests.post(
        f"{settings.API_URL}{settings.API_PREFIX}/{endpoint}",
        headers={"X-API-KEY": settings.API_KEY},
        timeout=5
    )

def api_get(endpoint):
    return requests.get(
        f"{settings.API_URL}{settings.API_PREFIX}/{endpoint}",
        headers={"X-API-KEY": settings.API_KEY},
        timeout=5
    )