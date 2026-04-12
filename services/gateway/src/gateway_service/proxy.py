"""HTTP reverse proxy to domain services (same path & query preserved)."""

from collections.abc import Mapping

import httpx
from fastapi import HTTPException, Request, Response

# Hop-by-hop headers (RFC 7230) — do not forward blindly
_HOP_HEADERS = frozenset(
    {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
        "host",
    },
)


def _filter_request_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {
        k: v
        for k, v in headers.items()
        if k.lower() not in _HOP_HEADERS and k.lower() != "content-length"
    }


def _filter_response_headers(headers: httpx.Headers) -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in headers.items():
        kl = k.lower()
        if kl in _HOP_HEADERS:
            continue
        out[k] = v
    return out


async def forward_request(
    request: Request,
    service_base_url: str,
    client: httpx.AsyncClient,
) -> Response:
    """Proxy to `service_base_url` + incoming path + query."""
    base = service_base_url.rstrip("/")
    path = request.url.path
    if not path.startswith("/"):
        path = "/" + path
    url = f"{base}{path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"

    body = await request.body()
    req_headers = _filter_request_headers(request.headers)
    try:
        upstream = await client.request(
            request.method,
            url,
            content=body if body else None,
            headers=req_headers,
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Upstream unreachable: {e!s}") from e

    resp_headers = _filter_response_headers(upstream.headers)
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=resp_headers,
        media_type=upstream.headers.get("content-type"),
    )
