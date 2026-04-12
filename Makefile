# Unix/macOS/Git Bash — mirrors scripts/install-local.ps1 on Windows.

.PHONY: install lint test compose

install:
	pip install -e ./packages/ams-common
	cd services/gateway && pip install -e ".[dev]" && cd ../..
	cd services/agent-service && pip install -e ".[dev]" && cd ../..
	cd services/orchestration-service && pip install -e ".[dev]" && cd ../..
	cd services/tool-service && pip install -e ".[dev]" && cd ../..
	cd services/execution-service && pip install -e ".[dev]" && cd ../..

lint:
	cd services/gateway && ruff check src tests && ruff format --check src tests && mypy src && cd ../..
	cd packages/ams-common && ruff check src && mypy src 2>/dev/null || true

test:
	pytest services/gateway/tests -q

compose:
	docker compose up --build
