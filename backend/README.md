# Legacy `backend/` folder

The **monolithic** FastAPI app previously lived under `backend/src/ams_ai/`. The codebase has moved to a **microservices** layout:

- **`packages/ams-common`** — shared library  
- **`services/gateway`** — API Gateway  
- **`services/*-service`** — domain services  
- **`docker-compose.yml`** (repo root) — run the full stack  

See **`services/README.md`** and the root **`README.md`**.

This directory is kept only as a pointer; new code should go under `packages/` and `services/`.
