from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.database import get_supabase_admin

router = APIRouter()


@router.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    supabase = get_supabase_admin()
    products = supabase.table("products").select("*").eq("user_id", current_user["user_id"]).execute()

    items = products.data or []
    total = len(items)
    low_stock_count = sum(1 for item in items if item.get("stock", 0) <= item.get("min_stock", 0))
    overstock_count = sum(1 for item in items if item.get("stock", 0) > item.get("min_stock", 0) * 3)
    healthy_stock_count = total - low_stock_count - overstock_count
    forecast_accuracy = 92.0
    stockout_rate = -35.0

    return {
        "total_products": total,
        "low_stock_count": low_stock_count,
        "overstock_count": overstock_count,
        "healthy_stock_count": healthy_stock_count,
        "forecast_accuracy": forecast_accuracy,
        "stockout_rate": stockout_rate,
        "products": items,
    }
