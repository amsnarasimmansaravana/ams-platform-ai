"""Structured logging (structlog)."""

import logging
import sys
from typing import Any

import structlog

from ams_common.config import ServiceSettings

_configured = False


def configure_logging(settings: ServiceSettings) -> None:
    global _configured
    if _configured:
        return
    _configured = True

    timestamper = structlog.processors.TimeStamper(fmt="iso")
    shared: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        timestamper,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if settings.log_json:
        shared.append(structlog.processors.JSONRenderer())
    else:
        shared.append(
            structlog.dev.ConsoleRenderer(colors=settings.environment == "development"),
        )

    level = (
        logging.DEBUG
        if settings.debug
        else getattr(logging, settings.log_level.upper(), logging.INFO)
    )

    structlog.configure(
        processors=shared,
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=level, format="%(message)s", stream=sys.stdout, force=True)


def get_logger(name: str | None = None) -> Any:
    return structlog.get_logger(name)
