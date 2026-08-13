from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ===================== AUTH MODELS =====================
class UserSignUp(BaseModel):
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
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ===================== PRODUCT MODELS =====================
class ProductCreate(BaseModel):
    name: str
    sku: str
    category: str
    price: float
    stock: int
    supplier: str
    lead_time: int
    min_stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    supplier: Optional[str] = None
    lead_time: Optional[int] = None
    min_stock: Optional[int] = None

class ProductResponse(BaseModel):
    id: str
    user_id: str
    name: str
    sku: str
    category: str
    price: float
    stock: int
    supplier: str
    lead_time: int
    min_stock: int
    created_at: datetime
    updated_at: datetime

# ===================== FORECAST MODELS =====================
class ForecastCreate(BaseModel):
    product_id: str
    predicted_demand: int
    confidence: float
    forecast_date: datetime

class ForecastResponse(BaseModel):
    id: str
    product_id: str
    user_id: str
    predicted_demand: int
    confidence: float
    forecast_date: datetime
    created_at: datetime

# ===================== ALERT MODELS =====================
class AlertCreate(BaseModel):
    product_id: str
    alert_type: str  # "low_stock", "overstock", "stockout_risk"
    message: str

class AlertResponse(BaseModel):
    id: str
    product_id: str
    user_id: str
    alert_type: str
    message: str
    status: str  # "active", "resolved"
    created_at: datetime
    resolved_at: Optional[datetime] = None

# ===================== INVENTORY MODELS =====================
class InventoryUpdate(BaseModel):
    product_id: str
    quantity_change: int
    reason: str  # "purchase", "sale", "adjustment"

class InventoryResponse(BaseModel):
    id: str
    product_id: str
    current_stock: int
    min_stock: int
    status: str  # "healthy", "low", "overstock"
    last_updated: datetime

# ===================== DASHBOARD MODELS =====================
class DashboardStatsResponse(BaseModel):
    total_products: int
    low_stock_count: int
    overstock_count: int
    healthy_stock_count: int
    total_forecast_accuracy: float
    stockout_rate: float

class RecentAlertResponse(BaseModel):
    id: str
    product_name: str
    alert_type: str
    message: str
    created_at: datetime
    status: str

# ===================== ORDER MODELS =====================
class OrderCreate(BaseModel):
    product_id: str
    quantity: int
    supplier: str
    expected_delivery: datetime

class OrderResponse(BaseModel):
    id: str
    product_id: str
    user_id: str
    quantity: int
    supplier: str
    status: str  # "pending", "delivered", "cancelled"
    expected_delivery: datetime
    created_at: datetime
    delivered_at: Optional[datetime] = None
