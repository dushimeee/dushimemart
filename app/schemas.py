"""
DushimeMart - Pydantic Schemas (Request/Response Validation)
Author: Cleonide Dushime (ID: 70871)

These schemas enforce input validation (returns HTTP 422 on bad data)
and shape the JSON responses.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- User ----------

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72, description="Plain password, 6-72 chars")
    full_name: str = Field(min_length=2, max_length=120)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Product ----------

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    price: float = Field(gt=0, description="Price must be greater than 0")
    stock: int = Field(ge=0, description="Stock cannot be negative")
    category: str = Field(default="general", min_length=2, max_length=60)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = Field(default=None, min_length=2, max_length=60)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Order ----------

class OrderCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=1000, description="Quantity must be between 1 and 1000")


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
