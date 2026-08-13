from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# ============================================================
# USER SCHEMAS
# ============================================================

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "store_manager"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    created_at: Optional[datetime] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============================================================
# PRODUCT SCHEMAS
# ============================================================

class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str
    stock: int
    price: float
    supplier: str
    lead_time: int
    min_stock: int
    max_stock: Optional[int] = 1000


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    lead_time: Optional[int] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None


class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    category: str
    stock: int
    price: float
    supplier: str
    lead_time: int
    min_stock: int
    created_at: datetime


# ============================================================
# FORECAST SCHEMAS
# ============================================================

class ForecastCreate(BaseModel):
    product_id: str
    predicted_demand: int
    confidence_score: Optional[float] = 0.0
    forecast_date: Optional[datetime] = None
    forecast_period: Optional[str] = "weekly"


class ForecastUpdate(BaseModel):
    predicted_demand: Optional[int] = None
    confidence_score: Optional[float] = None
    forecast_date: Optional[datetime] = None
    forecast_period: Optional[str] = None


class ForecastResponse(BaseModel):
    id: str
    product_id: str
    predicted_demand: int
    confidence_score: float
    forecast_date: datetime
    forecast_period: str
    created_at: datetime


class ForecastSummary(BaseModel):
    total_products: int
    low_stock_count: int
    overstock_count: int
    healthy_stock_count: int
    forecast_accuracy: float
    stockout_rate: float


# ============================================================
# ALERT SCHEMAS
# ============================================================

class AlertCreate(BaseModel):
    product_id: str
    alert_type: str  # low_stock, overstock, critical, reorder_recommended
    message: str
    priority: Optional[str] = "medium"  # low, medium, high, critical


class AlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class AlertResponse(BaseModel):
    id: str
    product_id: str
    alert_type: str
    message: str
    status: str
    priority: str
    created_at: datetime
    resolved_at: Optional[datetime] = None


# ============================================================
# ORDER SCHEMAS
# ============================================================

class OrderCreate(BaseModel):
    product_id: str
    quantity: int
    supplier: Optional[str] = None
    expected_delivery: Optional[datetime] = None


class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    supplier: Optional[str] = None
    expected_delivery: Optional[datetime] = None
    status: Optional[str] = None


class OrderResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    supplier: str
    status: str
    expected_delivery: Optional[datetime]
    created_at: datetime


# ============================================================
# SALES DATA SCHEMAS
# ============================================================

class SalesDataCreate(BaseModel):
    product_id: str
    quantity_sold: int
    revenue: float
    sale_date: str  # YYYY-MM-DD format


class SalesDataResponse(BaseModel):
    id: str
    product_id: str
    quantity_sold: int
    revenue: float
    sale_date: str
    created_at: datetime
