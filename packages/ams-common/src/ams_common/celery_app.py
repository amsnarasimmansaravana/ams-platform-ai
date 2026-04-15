"""Celery app setup for distributed task processing."""

from celery import Celery

from ams_common.config import ServiceSettings
from ams_common.logging import get_logger

_LOG = get_logger(__name__)


def get_celery_app(settings: ServiceSettings) -> Celery:
    """Initialize and configure Celery app."""
    app = Celery(
        "ams_ai",
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
    )

    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes max
        task_soft_time_limit=25 * 60,  # 25 minutes soft limit
        worker_prefetch_multiplier=4,
    )

    _LOG.info("celery_configured", broker=settings.celery_broker_url)
    return app
