# Contributing

## Workflow

1. Branch from the default branch (`feature/…`, `fix/…`).
2. Keep changes focused; match existing style (`ruff format` + `ruff check`).
3. Run tests before opening a PR: `cd backend && pytest`.
4. For API changes, update OpenAPI by maintaining route docstrings and Pydantic models.

## Backend checks (microservices)

Install shared library and a service (example: gateway):

```bash
pip install -e ./packages/ams-common
pip install -e "./services/gateway[dev]"
cd services/gateway
ruff format src tests
ruff check src tests
mypy src
pytest
```

Full local install: `./scripts/install-local.ps1` (Windows) or see `Makefile` on Unix.

```bash
docker compose up --build
```

## ADRs & requirements

Significant architectural decisions should use `docs/templates/ARCHITECTURE-DECISION-RECORD.md`. Functional changes should trace to `docs/v1.0/03-FUNCTIONAL-REQUIREMENTS.md` where applicable.

## Commits

Use clear, imperative subjects; body explains *why* when the change is non-obvious.
