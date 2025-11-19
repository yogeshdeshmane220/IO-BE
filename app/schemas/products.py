from pydantic import BaseModel

class ProductBase(BaseModel):
    sku: str
    name: str
    description: str | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True

class ProductFilter(BaseModel):
    sku: str | None = None
    name: str | None = None
    description: str | None = None
