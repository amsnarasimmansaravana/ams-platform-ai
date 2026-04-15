"""Celery worker startup script for AMS-AI."""

import sys

from ams_common.celery_app import get_celery_app
from ams_common.config import ServiceSettings
from ams_common.logging import configure_logging, get_logger

_LOG = get_logger(__name__)


def main():
    """Start Celery worker."""
    settings = ServiceSettings()
    configure_logging(settings)

    celery_app = get_celery_app(settings)

    _LOG.info(
        "celery_worker_starting",
        broker=settings.celery_broker_url,
        concurrency=4,
    )

    celery_app.worker_main([
        "worker",
        "--loglevel=info",
        "--concurrency=4",
        "--prefetch-multiplier=4",
    ])


if __name__ == "__main__":
    main()
