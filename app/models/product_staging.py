from sqlalchemy import Column, Integer, String
from app.models.base import Base

class ProductStaging(Base):
    __tablename__ = "product_staging"

    id = Column(Integer, primary_key=True)
    sku = Column(String(64), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
