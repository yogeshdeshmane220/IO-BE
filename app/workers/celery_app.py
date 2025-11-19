from celery import Celery

# Use docker service hostnames (redis service = "redis")
celery_app = Celery(
    "acme",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.workers.tasks"]
)

# also allow autodiscovery (redundant but harmless)
celery_app.autodiscover_tasks(["app.workers"])