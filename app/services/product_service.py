from app.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, db):
        self.repo = ProductRepository(db)

    def list(self, filters, offset, limit):
        return self.repo.list(filters, offset, limit)

    def create(self, data):
        return self.repo.create(data)

    def update(self, id, data):
        return self.repo.update(id, data)

    def delete(self, id):
        return self.repo.delete(id)

    def delete_all(self):
        return self.repo.delete_all()
