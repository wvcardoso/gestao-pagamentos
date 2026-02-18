FROM python:3.10-slim

WORKDIR /app

# copiar dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copiar app
COPY . .

# expor porta do Flask
EXPOSE 5000

CMD ["python", "app/web.py"]
