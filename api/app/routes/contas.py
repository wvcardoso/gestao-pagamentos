from fastapi import APIRouter,Depends
from app.core.database import listar_contas, pagar_conta
from app.core.security import verificar_api_key

router = APIRouter(prefix="/contas", tags=["Contas"])

@router.get("/")
def listar():    
    return listar_contas()

@router.post("/pagar/{id}")
def pagar(id: int):
    pagar_conta(id)
    return {"status": "ok"}