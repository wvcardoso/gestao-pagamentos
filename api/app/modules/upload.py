from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime, timezone
import uuid
from app.core.database import Base

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome_original = Column(String, nullable=False)
    nome_s3 = Column(String, nullable=False)
    tamanho_bytes = Column(Integer)
    hash_sha256 = Column(String)
    data_upload = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="enviado")    
    processado_em = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    erro = Column(String, nullable=True)