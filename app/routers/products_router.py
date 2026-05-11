"""
DushimeMart - Products Router (controller layer for /products endpoints)
Author: Cleonide Dushime (ID: 70871)

GET endpoints are public (anyone can browse the catalogue).
POST / PUT / DELETE endpoints require authentication (admin-style protection).
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse], summary="List all products (public)")
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProductService.list_all(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponse, summary="Get a single product (public)")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return product


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product (PROTECTED — requires login)",
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProductService.create(db, payload)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a product (PROTECTED — requires login)",
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = ProductService.update(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product (PROTECTED — requires login)",
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = ProductService.delete(db, product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
