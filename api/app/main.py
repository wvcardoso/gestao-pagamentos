from fastapi import FastAPI, Depends
from app.core.logging import setup_logging

# importa routers
from app.routes.processamento import router as processamento_router
from app.routes.contas import router as contas_router
from app.routes.upload import router as upload_router
from app.core.settings import settings
from app.core.security import verificar_api_key

from app.core.database import init_db
from app.core.bootstrap.folders import create_infra

# criação da aplicação FastAPI
api = FastAPI(
    title="Gestão de Pagamentos API",
    version="1.0.0",
    docs_url=f"{settings.API_PREFIX}/docs",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",    
    redoc_url=None
)




# evento de startup para inicialização do ambiente
@api.on_event("startup")
def startup_event():
    print("🚀 Iniciando aplicação...")

    # Configurar logging
    setup_logging()

    # Garantir que os diretórios e arquivos necessários existam
    print("🔧 Criando infra necessaria...")
    create_infra()

    # Criar tabela no banco de dados
    print("📂 Criando tabela no banco de dados...")
    init_db()

    print("✅ Ambiente pronto")

# Definir rotas para contas e processamento
## /api/v1/processar - executa processamento
## /api/v1/processar/status - consulta status do processamento
api.include_router(processamento_router,prefix=settings.API_PREFIX, dependencies=[Depends(verificar_api_key)])
api.include_router(upload_router       ,prefix=settings.API_PREFIX, dependencies=[Depends(verificar_api_key)])
api.include_router(contas_router       ,prefix=settings.API_PREFIX, dependencies=[Depends(verificar_api_key)])