"""
DushimeMart - Seed Script (populates the database with sample grocery products)
Author: Cleonide Dushime (ID: 70871)

Run with:
    python seed.py

This is optional but useful for screenshots / demos.
"""
from app.database import Base, SessionLocal, engine
from app.models import Product


SAMPLE_PRODUCTS = [
    {"name": "Brown Bread Loaf", "description": "Freshly baked whole-grain loaf", "price": 2.50, "stock": 40, "category": "bakery"},
    {"name": "Free-Range Eggs (12 pack)", "description": "Locally sourced free-range eggs", "price": 4.20, "stock": 60, "category": "dairy"},
    {"name": "Whole Milk 1L", "description": "Pasteurized whole cow milk", "price": 1.30, "stock": 80, "category": "dairy"},
    {"name": "Bananas (1 kg)", "description": "Ripe yellow bananas", "price": 1.80, "stock": 100, "category": "produce"},
    {"name": "Basmati Rice 5 kg", "description": "Premium long-grain basmati rice", "price": 12.50, "stock": 25, "category": "pantry"},
    {"name": "Olive Oil 500 ml", "description": "Extra-virgin Mediterranean olive oil", "price": 7.90, "stock": 30, "category": "pantry"},
    {"name": "Chicken Breast (1 kg)", "description": "Skinless chicken breast fillets", "price": 8.50, "stock": 20, "category": "meat"},
    {"name": "Tomato Pasta Sauce", "description": "Classic Italian tomato sauce, 400g jar", "price": 2.10, "stock": 50, "category": "pantry"},
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Product).count()
        if existing > 0:
            print(f"Database already has {existing} products — skipping seed.")
            return
        for item in SAMPLE_PRODUCTS:
            db.add(Product(**item))
        db.commit()
        print(f"Inserted {len(SAMPLE_PRODUCTS)} sample products.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
