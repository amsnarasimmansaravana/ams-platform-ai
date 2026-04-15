"""Inter-service HTTP client for service-to-service communication."""

from typing import Any, Optional

import httpx

from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class ServiceClient:
    """HTTP client for inter-service communication."""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = httpx.Timeout(timeout)
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(timeout=self.timeout, headers=headers)
        return self._client

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get(self, path: str, **kwargs) -> dict[str, Any]:
        """GET request."""
        client = await self._get_client()
        url = f"{self.base_url}{path}"
        try:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            _LOG.error("service_call_failed", url=url, status=e.response.status_code)
            raise
        except Exception as e:
            _LOG.error("service_call_error", url=url, error=str(e))
            raise

    async def post(self, path: str, json: dict[str, Any] | None = None, **kwargs) -> dict[str, Any]:
        """POST request."""
        client = await self._get_client()
        url = f"{self.base_url}{path}"
        try:
            response = await client.post(url, json=json, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            _LOG.error("service_call_failed", url=url, status=e.response.status_code)
            raise
        except Exception as e:
            _LOG.error("service_call_error", url=url, error=str(e))
            raise

    async def put(self, path: str, json: dict[str, Any] | None = None, **kwargs) -> dict[str, Any]:
        """PUT request."""
        client = await self._get_client()
        url = f"{self.base_url}{path}"
        try:
            response = await client.put(url, json=json, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            _LOG.error("service_call_failed", url=url, status=e.response.status_code)
            raise
        except Exception as e:
            _LOG.error("service_call_error", url=url, error=str(e))
            raise

    async def delete(self, path: str, **kwargs) -> Optional[dict[str, Any]]:
        """DELETE request."""
        client = await self._get_client()
        url = f"{self.base_url}{path}"
        try:
            response = await client.delete(url, **kwargs)
            response.raise_for_status()
            if response.content:
                return response.json()
            return None
        except httpx.HTTPStatusError as e:
            _LOG.error("service_call_failed", url=url, status=e.response.status_code)
            raise
        except Exception as e:
            _LOG.error("service_call_error", url=url, error=str(e))
            raise


# Service client factories for each domain
class AgentServiceClient(ServiceClient):
    """Agent service HTTP client."""
    pass


class ToolServiceClient(ServiceClient):
    """Tool service HTTP client."""
    pass


class OrchestrationServiceClient(ServiceClient):
    """Orchestration service HTTP client."""
    pass


class ExecutionServiceClient(ServiceClient):
    """Execution service HTTP client."""
    pass
