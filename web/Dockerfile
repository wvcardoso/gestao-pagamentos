FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y \
##    libzbar0 \
#    tesseract-ocr \
#    tesseract-ocr-por \
#    libgl1 \
#    libglib2.0-0 \
#    poppler-utils \
#    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "app.main"]