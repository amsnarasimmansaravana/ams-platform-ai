"""Pytest fixtures."""

import pytest

from gateway_service.settings import get_gateway_settings


@pytest.fixture(autouse=True)
def _clear_gateway_settings() -> None:
    get_gateway_settings.cache_clear()
    yield
    get_gateway_settings.cache_clear()
