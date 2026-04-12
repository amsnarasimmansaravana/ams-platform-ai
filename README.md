# AMS Platform AI

Enterprise **multi-agent orchestration** platform: documentation, architecture diagrams, and a **microservices** backend (Docker Compose).

## Architecture (runtime)

| Layer | Location |
|-------|----------|
| **Shared library** | `packages/ams-common` — config (`AMS_*`), structlog, request ID middleware, small service app helper |
| **API Gateway** | `services/gateway` — reverse proxy to domain services by `/api/v1/{agents\|orchestrations\|tools\|executions}` |
| **Domain services** | `services/agent-service`, `orchestration-service`, `tool-service`, `execution-service` |
| **Data plane** | Postgres + Redis (Compose); connect from services as you add persistence |

This is **not** a monolith: each service is an independent deployable with its own `Dockerfile` and virtualenv.

## Quick start (Docker — recommended)

```bash
docker compose up --build
```

- **Gateway (public):** http://localhost:8000  
- **Proxied examples:**  
  - http://localhost:8000/api/v1/agents  
  - http://localhost:8000/api/v1/orchestrations  

Postgres: `localhost:5432` (user/password/db `ams` / `ams` / `ams_ai`). Redis: `localhost:6379`.

## Local development (editable installs)

From repository root (PowerShell):

```powershell
.\scripts\install-local.ps1
```

Or manually: `pip install -e ./packages/ams-common` then `pip install -e ./services/gateway` (and other services). Run gateway with downstream URLs pointing to locally running services or use Compose.

## Engineering practices

| Practice | Where |
|----------|--------|
| **12-factor config** | `AMS_*` env vars (`ams_common.config.ServiceSettings`) |
| **Structured logs** | `structlog`, JSON in containers (`AMS_LOG_JSON=true`) |
| **Health probes** | `/health/live`, `/health/ready` on gateway and each service |
| **API versioning** | `/api/v1` prefix |
| **Isolation** | Separate images, scale replicas per service |
| **Tests / lint / types** | `pytest`, `ruff`, `mypy` per service (see `services/gateway/pyproject.toml`) |

Details: `services/README.md`, `CONTRIBUTING.md`, `docs/v1.0/04-TECHNICAL-ARCHITECTURE.md`.

## Documentation

Start at `docs/README.md` or `docs/COMPLETE-PRODUCT-CONTEXT.md`.

## Legacy note

The old monolithic app under `backend/src` was removed; see `backend/README.md`.
