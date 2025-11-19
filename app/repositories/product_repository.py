from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, filters, offset, limit):
        q = self.db.query(Product)

        if filters.sku:
            q = q.filter(Product.sku.ilike(filters.sku))
        if filters.name:
            q = q.filter(Product.name.ilike(f"%{filters.name}%"))
        if filters.description:
            q = q.filter(Product.description.ilike(f"%{filters.description}%"))

        return q.offset(offset).limit(limit).all()

    def get_by_id(self, id):
        return self.db.query(Product).filter(Product.id == id).first()

    def create(self, data):
        p = Product(**data)
        self.db.add(p)
        self.db.commit()
        self.db.refresh(p)
        return p

    def update(self, id, data):
        p = self.get_by_id(id)
        if not p:
            return None
        for k, v in data.items():
            setattr(p, k, v)
        self.db.commit()
        self.db.refresh(p)
        return p

    def delete(self, id):
        p = self.get_by_id(id)
        if not p:
            return False
        self.db.delete(p)
        self.db.commit()
        return True

    def delete_all(self):
        self.db.query(Product).delete()
        self.db.commit()
