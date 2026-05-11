"""
DushimeMart - Orders Router (controller layer for /orders endpoints)
Author: Cleonide Dushime (ID: 70871)

All order endpoints are PROTECTED — a user can only see/manage their own orders.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import OrderCreate, OrderResponse
from app.services.order_service import (
    ORDER_INSUFFICIENT_STOCK,
    ORDER_OK,
    ORDER_PRODUCT_NOT_FOUND,
    OrderService,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=List[OrderResponse], summary="List my orders")
def list_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OrderService.list_for_user(db, current_user.id)


@router.get("/{order_id}", response_model=OrderResponse, summary="Get one of my orders")
def get_my_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = OrderService.get_for_user(db, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    return order


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Place a new order",
)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    code, order = OrderService.create(db, current_user, payload)

    if code == ORDER_PRODUCT_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    if code == ORDER_INSUFFICIENT_STOCK:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Insufficient stock available for the requested quantity.",
        )
    if code != ORDER_OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create order.")
    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel an order",
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cancelled = OrderService.cancel(db, order_id, current_user.id)
    if not cancelled:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
