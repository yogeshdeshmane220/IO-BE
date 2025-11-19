from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.schemas.webhooks import (
    WebhookCreate, WebhookUpdate, WebhookOut
)
from app.services.webhook_service import WebhookService
from app.workers.tasks import send_test_webhook

router = APIRouter(prefix="/webhooks")

@router.get("/", response_model=list[WebhookOut])
def list_webhooks(db: Session = Depends(get_session)):
    svc = WebhookService(db)
    return svc.list()

@router.post("/", response_model=WebhookOut)
def create_webhook(data: WebhookCreate, db: Session = Depends(get_session)):
    svc = WebhookService(db)
    return svc.create(data.dict())

@router.put("/{id}", response_model=WebhookOut)
def update_webhook(id: int, data: WebhookUpdate, db: Session = Depends(get_session)):
    svc = WebhookService(db)
    return svc.update(id, data.dict(exclude_none=True))

@router.delete("/{id}")
def delete_webhook(id: int, db: Session = Depends(get_session)):
    svc = WebhookService(db)
    return {"success": svc.delete(id)}

@router.post("/{id}/test")
def test_webhook(id: int, db: Session = Depends(get_session)):
    send_test_webhook.delay(id)
    return {"queued": True}
