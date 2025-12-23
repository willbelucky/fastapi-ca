import sys

from celery import Celery

from config import get_settings
from user.application.send_welcome_email_task import SendWelcomeEmailTask

settings = get_settings()

celery = Celery(
    "fastapi-ca",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
    broker_connection_retry_on_startup=True,
    include=["user.application"],
)

# Windows에서는 prefork 풀이 작동하지 않으므로 solo 풀 사용
if sys.platform == "win32":
    celery.conf.task_always_eager = False
    celery.conf.worker_pool = "solo"

celery.register_task(SendWelcomeEmailTask())
