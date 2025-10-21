
# Imagem base leve
FROM python:3.12-slim

# Variáveis de ambiente para Python no container
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1

# Instalar dependências do sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copiar app
COPY . .

# Expor porta
EXPOSE 5000

# Executar a aplicação
CMD ["python", "app.py"]
