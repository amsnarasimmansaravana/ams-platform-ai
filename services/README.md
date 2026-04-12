# AMS-AI microservices

Enterprise-style **service-per-bounded-context** layout (not a monolith):

| Service | Role | Default path (via gateway) |
|---------|------|-----------------------------|
| **gateway** | API Gateway — HTTP proxy, CORS, public port | `http://localhost:8000` |
| **agent-service** | Agent registry & A2A | `/api/v1/agents` |
| **orchestration-service** | Workflows / DAGs | `/api/v1/orchestrations` |
| **tool-service** | Tool & API registry | `/api/v1/tools` |
| **execution-service** | Runs / execution engine | `/api/v1/executions` |

Shared library: **`packages/ams-common`** (logging, config, middleware, small app factory).

## Local install (editable)

From repository root:

```bash
pip install -e ./packages/ams-common
pip install -e "./services/gateway[dev]"
pip install -e "./services/agent-service[dev]"
# …other services as needed
```

Run gateway (expects upstream URLs — use Docker Compose or set `AMS_*_SERVICE_URL`):

```bash
# Terminal 1–4: run each domain service on 8001–8004 (see each main.py)
# Terminal 5:
cd services/gateway
python -m uvicorn gateway_service.main:app --reload --port 8000
```

Easiest path: **`docker compose up --build`** from repo root (see `../docker-compose.yml`).

## Adding a new microservice

1. Copy `services/agent-service/` as a template (pyproject, `src/<pkg>/main.py`, `Dockerfile`).
2. Register routes under a **unique** `/api/v1/<resource>` prefix.
3. Add the service to `docker-compose.yml` and extend `gateway_service/settings.py` + `gateway_service/main.py` proxy branches (or refactor proxy to a registry map).

## Practices

- **One process per service** in production; scale replicas independently.
- **Gateway** is the only service that typically needs a public load balancer.
- **Postgres/Redis** are shared infrastructure; use **schemas or DB-per-service** as you add persistence (see ADRs).
