FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY packages/ams-common /app/packages/ams-common
COPY services/orchestration-service /app/services/orchestration-service
RUN pip install --upgrade pip \
 && pip install --no-cache-dir /app/packages/ams-common \
 && pip install --no-cache-dir /app/services/orchestration-service \
 && chown -R nobody:nogroup /app
EXPOSE 8000
USER nobody
WORKDIR /app/services/orchestration-service
CMD ["python", "-m", "uvicorn", "orchestration_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
