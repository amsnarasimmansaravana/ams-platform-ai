FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY packages/ams-common /app/packages/ams-common
COPY services/agent-service /app/services/agent-service
RUN pip install --upgrade pip \
 && pip install --no-cache-dir /app/packages/ams-common \
 && pip install --no-cache-dir /app/services/agent-service \
 && chown -R nobody:nogroup /app
EXPOSE 8000
USER nobody
WORKDIR /app/services/agent-service
CMD ["python", "-m", "uvicorn", "agent_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
