"""
DushimeMart - Product Service (business logic for product catalogue)
Author: Cleonide Dushime (ID: 70871)
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


class ProductService:
    """Encapsulates business logic for grocery products."""

    @staticmethod
    def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def get(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def create(db: Session, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update(db: Session, product_id: int, payload: ProductUpdate) -> Optional[Product]:
        product = ProductService.get(db, product_id)
        if not product:
            return None
        # Only apply fields that were actually provided (partial update)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product_id: int) -> bool:
        product = ProductService.get(db, product_id)
        if not product:
            return False
        db.delete(product)
        db.commit()
        return True
