import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.result_expires = 180

app.conf.beat_schedule = {
    "update_coin_price": {
        "task": "exchange.tasks.update_coin_price",
        "schedule": 1.0,
        "options": {"queue": "exchange_info"},
    },
    "send_socket_price": {
        "task": "exchange.tasks.send_socket_price",
        "schedule": 1.0,
        "options": {"queue": "exchange_info"},
    },
}

app.conf.timezone = "UTC"
app.autodiscover_tasks()
