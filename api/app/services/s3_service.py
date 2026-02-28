import boto3
import os
from io import BytesIO
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "admin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "senha123")
S3_BUCKET = os.getenv("S3_BUCKET", "uploads")


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name="us-east-1"
    )


def upload_file(file_obj, filename: str):
    logger.debug(f"Enviando arquivo para S3: {filename}")
    s3 = get_s3_client()

    try:
        s3.upload_fileobj(file_obj, S3_BUCKET, filename)
    except ClientError as e:
        logger.error(f"Erro ao enviar arquivo para S3: {e}")
        raise


def download_file(nome_s3: str) -> BytesIO:
    
    s3 = get_s3_client()
    file_obj = BytesIO()   

    try:
        s3.download_fileobj(
            Bucket=S3_BUCKET,
            Key=nome_s3,
            Fileobj=file_obj
        )
        logger.debug(f"Arquivo {nome_s3} baixado com sucesso do S3")
    except s3.exceptions.NoSuchKey:
        logger.error(f"Arquivo {nome_s3} não encontrado no S3")
        raise FileNotFoundError(f"Arquivo {nome_s3} não encontrado no S3")
    except ClientError as e:
        logger.error(f"Erro ao baixar arquivo do S3: {e}")
        raise

    file_obj.seek(0)
    return file_obj