from fastapi import APIRouter, Depends
from app.services.processador import service_processar_uploads, service_reprocessar_erros
from sqlalchemy.orm import Session
from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/processar", tags=["Processar"])

# Este endpoint processa os uploads pendentes (status "enviado")
@router.post("/")
def router_processar_files(db: Session = Depends(get_db)):

    logger.debug(f"Processando uploads pendentes")
    return service_processar_uploads(db)

# Este endpoint reprocessa uploads com erro, ou um específico se id for fornecido
@router.post("/reprocessar/")
def router_reprocessar_allfiles(db: Session = Depends(get_db)):

    logger.info(f"Reprocessando todos files com erro")
    return service_reprocessar_erros(db)

# Este endpoint reprocessa um upload específico por ID
@router.post("/{id}")
def router_reprocessar_file(
    id: str,
    db: Session = Depends(get_db)
):
    logger.info(f"Reprocessando file com id {id}")
    return service_reprocessar_erros(db, id)
    