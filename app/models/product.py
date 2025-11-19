from sqlalchemy import Column, Integer, String, Index, func
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(64), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)

    __table_args__ = (
        Index("ix_products_sku_lower", func.lower(sku), unique=True),
    )
