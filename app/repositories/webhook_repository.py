from sqlalchemy.orm import Session
from app.models.webhook import Webhook

class WebhookRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(Webhook).all()

    def get(self, id: int):
        return self.db.query(Webhook).filter(Webhook.id == id).first()

    def create(self, data: dict):
        w = Webhook(**data)
        self.db.add(w)
        self.db.commit()
        self.db.refresh(w)
        return w

    def update(self, id: int, data: dict):
        w = self.get(id)
        if not w:
            return None
        for k, v in data.items():
            setattr(w, k, v)
        self.db.commit()
        self.db.refresh(w)
        return w

    def delete(self, id: int):
        w = self.get(id)
        if not w:
            return False
        self.db.delete(w)
        self.db.commit()
        return True
