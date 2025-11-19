from app.repositories.webhook_repository import WebhookRepository

class WebhookService:
    def __init__(self, db):
        self.repo = WebhookRepository(db)

    def list(self):
        return self.repo.list()

    def create(self, data):
        return self.repo.create(data)

    def update(self, id, data):
        return self.repo.update(id, data)

    def delete(self, id):
        return self.repo.delete(id)
