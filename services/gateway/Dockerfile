# Build from repository root: docker build -f services/gateway/Dockerfile .
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY packages/ams-common /app/packages/ams-common
COPY services/gateway /app/services/gateway
RUN pip install --upgrade pip \
 && pip install --no-cache-dir /app/packages/ams-common \
 && pip install --no-cache-dir /app/services/gateway \
 && chown -R nobody:nogroup /app
EXPOSE 8000
USER nobody
WORKDIR /app/services/gateway
CMD ["python", "-m", "uvicorn", "gateway_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
