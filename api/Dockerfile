FROM python:3.10-slim

# Criar usuário não-root
#RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libzbar0 \
    tesseract-ocr \
    tesseract-ocr-por \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Mudar para usuário não-root
#USER appuser

CMD ["sh", "-c", "uvicorn app.main:api --host 0.0.0.0 --port 8000 --log-level ${LOG_LEVEL:-info}"]