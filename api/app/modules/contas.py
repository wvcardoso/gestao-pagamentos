from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base


class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    residencia = Column(String)
    tipo = Column(String)
    favorecido = Column(String)
    referencia = Column(String)
    valor = Column(Float)
    vencimento = Column(String)
    codigo_barras = Column(String)
    pix_payload = Column(String)
    descricao = Column(String)
    status = Column(String, default="pendente")
    criado_em = Column(DateTime, default=datetime.utcnow)