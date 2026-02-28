from datetime import timezone, datetime
from app.modules.upload import Upload
from app.services.s3_service import download_file
from app.services.parser import orchestrator
from app.core.database import inserir_conta
import logging

logger = logging.getLogger(__name__)

def service_reprocessar_erros(db, id=None):
    
    if id is not None:
        uploads = [db.query(Upload).filter(Upload.id == id).first()]
    else:
        uploads = db.query(Upload).filter(Upload.status == "erro").all()

    if not uploads:
        return {"detail": "Nenhum upload com erro encontrado"}

    reprocessados = []

    for upload in uploads:
        upload.status = "enviado"
        upload.erro = None

    db.commit()

    # Agora reaproveita sua lógica normal
    return service_processar_uploads(db)

def service_processar_uploads(db):   

    processados = []
    erros = []

    # 🔒 trava simples de concorrência via banco
    if db.query(Upload).filter(Upload.status == "processando").first():
        return {"detail": "Já existe processamento em andamento"}
    
    #uploads = db.query(Upload).filter(Upload.status == "enviado").all()
    uploads = (
        db.query(Upload)
        .filter(Upload.status != "processado")
        .all()
    )
    logger.debug(f"Uploads encontrados para processamento: {[u.nome_original for u in uploads]}")

    if not uploads:
        return {"detail": "Nenhum upload pendente"}

    for upload in uploads:
        try:

            logger.info(f"Iniciando processamento {upload.nome_original})")
            logger.debug(f"Iniciando processamento {upload.id}")

            upload.status = "processando"
            db.commit()
            
            logger.debug(f"download - nome S3: {upload.nome_s3}")
            logger.debug(f"iniciando download do arquivo: {upload.nome_original}")
            arquivo = download_file(upload.nome_s3)
            
            dados = orchestrator.processar_files(
                nome_original=upload.nome_original,
                arquivo_bytes=arquivo
            )
            
            if not dados:
                logger.debug(f"Parser não retornou dados  {upload.nome_original}")
                logger.debug(f"-----------------------------------------")                
                raise ValueError("Parser não retornou dados")                
            else:
                logger.debug(f"Parser finalizado e extraído para o file {upload.nome_original}")
                logger.debug(f"-----------------------------------------")
            
            logger.debug(f"Iniciando inserção da conta no banco para o upload {upload.nome_original}")
            inserir_conta(dados)

            upload.status = "processado"
            upload.processado_em = datetime.now(timezone.utc)

            processados.append(upload.id)

        except Exception as e:
            upload.status = "erro"
            upload.erro = str(e)            
    

        db.commit()

    return {
        "processados": processados,
        "erros": erros
    }