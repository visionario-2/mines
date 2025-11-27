FROM python:3.11-slim

# Não criar .pyc e mandar tudo pro stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Primeiro só o requirements, pra aproveitar cache
COPY requirements.txt .

# Atualiza pip e instala dependências
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install supervisor

# Agora copia o restante do projeto
COPY . .

# Arquivos de log do supervisor vão pro stdout/stderr
ENV SUPERVISOR_LOGLEVEL=info

# Comando que vai rodar os 2 processos: bot + uvicorn
CMD ["supervisord", "-c", "/app/supervisord.conf"]
