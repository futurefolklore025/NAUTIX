FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PYTHONPATH="/app"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     gcc     libpq-dev     curl     && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create keys directory
RUN mkdir -p /app/keys &&     if [ ! -f /app/keys/qr_es256_private.pem ]; then         openssl ecparam -genkey -name prime256v1 -noout -out /app/keys/qr_es256_private.pem &&         openssl ec -in /app/keys/qr_es256_private.pem -pubout -out /app/keys/qr_es256_public.pem;     fi

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Create non-root user
RUN groupadd -r nautix && useradd -r -g nautix nautix

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/keys /app/logs &&     chown -R nautix:nautix /app

# Switch to non-root user
USER nautix

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3     CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
