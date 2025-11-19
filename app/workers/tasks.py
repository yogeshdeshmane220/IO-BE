# from app.workers.celery_app import celery_app
# from sqlalchemy.orm import Session
# from app.db.db import SessionLocal
# from app.models.product_staging import ProductStaging
# from app.models.product import Product
# from app.models.job import Job
# import csv
# import requests
# from sqlalchemy import text
# from app.models.webhook import Webhook
#
# @celery_app.task(name="app.workers.tasks.process_csv")
# def process_csv(job_id: int, path: str):
#     db: Session = SessionLocal()
#
#     try:
#         job = db.query(Job).filter(Job.id == job_id).first()
#         job.status = "parsing"
#         job.phase = "reading_csv"
#         db.commit()
#
#         with open(path, "r", encoding="utf-8") as f:
#             reader = csv.DictReader(f)
#             rows = list(reader)
#
#         total = len(rows)
#         processed = 0
#
#         db.query(ProductStaging).delete()
#         db.commit()
#
#         for r in rows:
#             db.add(ProductStaging(
#                 sku=r["sku"],
#                 name=r["name"],
#                 description=r.get("description"),
#             ))
#             processed += 1
#             if processed % 1000 == 0:
#                 job.percent = processed / total * 100
#                 db.commit()
#
#         db.commit()
#
#         job.status = "merging"
#         job.phase = "dedupe_and_insert"
#         db.commit()
#
#         db.execute(text("""
#             INSERT INTO products (sku, name, description)
#             SELECT sku, name, description
#             FROM product_staging
#             ON CONFLICT ((lower(sku)))
#             DO UPDATE SET
#                 name = EXCLUDED.name,
#                 description = EXCLUDED.description;
#         """))
#         db.commit()
#
#         job.status = "complete"
#         job.phase = "done"
#         job.percent = 100
#         db.commit()
#
#     except Exception as e:
#         job = db.query(Job).filter(Job.id == job_id).first()
#         job.status = "failed"
#         job.error_message = str(e)
#         db.commit()
#
#     finally:
#         db.close()
#
#
# @celery_app.task
# def send_test_webhook(webhook_id: int):
#     db = SessionLocal()
#     try:
#         w = db.query(Webhook).filter(Webhook.id == webhook_id).first()
#         if not w or not w.enabled:
#             return
#         payload = {"message": "webhook test", "id": webhook_id}
#         requests.post(w.url, json=payload, timeout=5)
#     finally:
#         db.close()


from app.workers.celery_app import celery_app
from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.models.product import Product
from app.models.job import Job
from app.models.webhook import Webhook
from sqlalchemy.dialects.postgresql import insert
import csv
from sqlalchemy import text
import os
import requests


@celery_app.task(name="app.workers.tasks.process_csv")
def process_csv(job_id: int, path: str):
    db: Session = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        job.status = "parsing"
        job.phase = "reading_csv"
        db.commit()

        # read file
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        total = len(rows)
        processed = 0

        # dedupe by case-insensitive SKU
        dedupe = {}
        for r in rows:
            key = r["sku"].lower()
            dedupe[key] = {
                "sku": r["sku"],
                "name": r["name"],
                "description": r.get("description"),
            }

            processed += 1
            if processed % 1000 == 0:
                job.percent = processed / total * 100
                db.commit()

        final_rows = list(dedupe.values())

        job.status = "merging"
        job.phase = "bulk_upsert"
        db.commit()

        # bulk UPSERT
        stmt = insert(Product.__table__).values(final_rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=[text("lower(sku)")],
            set_={
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
            }
        )

        db.execute(stmt)
        db.commit()

        job.status = "complete"
        job.phase = "done"
        job.percent = 100
        db.commit()

    except Exception as e:
        if job := db.query(Job).filter(Job.id == job_id).first():
            job.status = "failed"
            job.error_message = str(e)
            db.commit()

    finally:
        db.close()


@celery_app.task
def send_test_webhook(webhook_id: int):
    db = SessionLocal()
    try:
        w = db.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not w or not w.enabled:
            return
        payload = {"message": "webhook test", "id": webhook_id}
        requests.post(w.url, json=payload, timeout=5)
    finally:
        db.close()
