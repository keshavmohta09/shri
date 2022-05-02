"""
Celery configurations file.
"""

import os

from celery.schedules import crontab

CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_ACCEPT_CONTENT = ["json", "pickle"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_retries": os.environ.get("CELERY_PUBLISH_MAX_RETRIES", 1)
}
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_IGNORE_RESULT = False
CELERY_SEND_EVENTS = True
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 100
CELERY_BEAT_SCHEDULE = {
    "update_products_price_every_12_hours": {
        "task": "products.tasks.send_email_on_update_product_task",
        # "schedule": crontab(hour="*/12"),
        "schedule": crontab(minute="*/1"),
    },
}
