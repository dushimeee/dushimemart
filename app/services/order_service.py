"""
DushimeMart - Order Service (business logic for placing & managing orders)
Author: Cleonide Dushime (ID: 70871)
"""
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models import Order, Product, User
from app.schemas import OrderCreate


# Result codes returned by create() to keep business logic decoupled from HTTP errors
ORDER_OK = "ok"
ORDER_PRODUCT_NOT_FOUND = "product_not_found"
ORDER_INSUFFICIENT_STOCK = "insufficient_stock"


class OrderService:
    """Encapsulates business logic for orders."""

    @staticmethod
    def list_for_user(db: Session, user_id: int) -> List[Order]:
        return db.query(Order).filter(Order.user_id == user_id).all()

    @staticmethod
    def get_for_user(db: Session, order_id: int, user_id: int) -> Optional[Order]:
        return (
            db.query(Order)
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )

    @staticmethod
    def create(db: Session, user: User, payload: OrderCreate) -> Tuple[str, Optional[Order]]:
        """
        Create an order. Returns (status_code, order_or_None).
        Status codes are defined as module-level constants above.
        """
        product = db.query(Product).filter(Product.id == payload.product_id).first()
        if not product:
            return ORDER_PRODUCT_NOT_FOUND, None
        if product.stock < payload.quantity:
            return ORDER_INSUFFICIENT_STOCK, None

        # Deduct stock and create the order in one transaction
        product.stock -= payload.quantity
        total = round(product.price * payload.quantity, 2)
        order = Order(
            user_id=user.id,
            product_id=product.id,
            quantity=payload.quantity,
            total_price=total,
            status="confirmed",
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return ORDER_OK, order

    @staticmethod
    def cancel(db: Session, order_id: int, user_id: int) -> bool:
        order = OrderService.get_for_user(db, order_id, user_id)
        if not order:
            return False
        # Restock the product before deleting the order
        product = db.query(Product).filter(Product.id == order.product_id).first()
        if product:
            product.stock += order.quantity
        db.delete(order)
        db.commit()
        return True
