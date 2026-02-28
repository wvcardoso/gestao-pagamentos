from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.core.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from app.modules.upload import Upload
from app.services.s3_service import upload_file
from app.core.utils import calcular_hash
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
}

@router.get("/all/")
def listar_uploads(
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Upload)

    if status:
        query = query.filter(Upload.status == status)

    uploads = query.order_by(Upload.id.desc()).all()

    return uploads


@router.post("/")
async def upload_files(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Tipo de arquivo não permitido"
        )

    db = SessionLocal()

    try:
        # calcular hash
        file_hash = calcular_hash(file.file)

        # verificar duplicidade
        existente = db.query(Upload).filter(Upload.hash_sha256 == file_hash).first()
        if existente:
            raise HTTPException(status_code=400, detail="Arquivo já enviado anteriormente")

        # tamanho
        file.file.seek(0, 2)
        tamanho = file.file.tell()
        file.file.seek(0)

        novo_nome = f"{uuid.uuid4()}.pdf"

        # enviar para S3
        upload_file(file.file, novo_nome)

        # criar registro no banco
        novo_upload = Upload(
            nome_original=file.filename,
            nome_s3=novo_nome,
            tamanho_bytes=tamanho,
            hash_sha256=file_hash,
            status="enviado"
        )

        db.add(novo_upload)
        db.commit()
        db.refresh(novo_upload)

        logger.info(f"Upload salvo com ID {novo_upload.id}")

        return {
            "id": novo_upload.id,
            "status": novo_upload.status
        }

    finally:
        db.close()