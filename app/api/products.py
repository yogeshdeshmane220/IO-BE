from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.models.product import Product
from app.schemas.products import (
    ProductCreate, ProductUpdate, ProductOut, ProductFilter
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products")

# ----------------------- LIST -----------------------
@router.get("/", response_model=list[ProductOut])
def list_products(
    filters: ProductFilter = Depends(),
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_session)
):
    offset = (page - 1) * limit
    svc = ProductService(db)
    return svc.list(filters, offset, limit)

# ----------------------- CREATE -----------------------
@router.post("/", response_model=ProductOut)
def create_product(data: ProductCreate, db: Session = Depends(get_session)):
    svc = ProductService(db)
    return svc.create(data.dict())

# ----------------------- BULK DELETE (MOVE ABOVE {id}) -----------------------
@router.delete("/clear_all")
def clear_all(db: Session = Depends(get_session)):
    db.query(Product).delete()
    db.commit()
    return {"status": "ok"}

@router.delete("/")
def delete_all_products(db: Session = Depends(get_session)):
    svc = ProductService(db)
    svc.delete_all()
    return {"success": True}

# ----------------------- SINGLE DELETE -----------------------
@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_session)):
    svc = ProductService(db)
    return {"success": svc.delete(id)}

# ----------------------- UPDATE -----------------------
@router.put("/{id}", response_model=ProductOut)
def update_product(id: int, data: ProductUpdate, db: Session = Depends(get_session)):
    svc = ProductService(db)
    return svc.update(id, data.dict(exclude_none=True))
