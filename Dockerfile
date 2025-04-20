FROM python:3.11-slim

# Instala libs mínimas para Playwright headless
RUN apt-get update && apt-get install -y \
    wget curl gnupg \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libpangocairo-1.0-0 libpango-1.0-0 libx11-xcb1 libxshmfence1 \
    libxext6 libxfixes3 libxkbcommon0 \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instala navegadores do Playwright
RUN python -m playwright install chromium

# Define diretório de trabalho
WORKDIR /app
COPY . .

# Porta padrão do Flask
EXPOSE 5000

# Comando default (ajuste se tiver um app.py por exemplo)
CMD ["python", "wsgi.py"]