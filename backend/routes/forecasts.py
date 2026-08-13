from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.database import get_supabase_admin
from app.schemas import ForecastCreate, ForecastUpdate
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/forecasts")
async def list_forecasts(current_user: dict = Depends(get_current_user)):
    """Get all forecasts for current user's products"""
    supabase = get_supabase_admin()
    result = supabase.table("forecasts").select("*").eq("user_id", current_user["user_id"]).order("forecast_date", desc=True).execute()
    return {"items": result.data or []}


@router.post("/forecasts")
async def create_forecast(payload: ForecastCreate, current_user: dict = Depends(get_current_user)):
    """Create a new forecast for a product"""
    supabase = get_supabase_admin()
    
    # Verify product belongs to user
    product = supabase.table("products").select("id").eq("id", payload.product_id).eq("user_id", current_user["user_id"]).execute()
    if not product.data:
        raise HTTPException(status_code=404, detail="Product not found")
    
    forecast_data = {
        "user_id": current_user["user_id"],
        "product_id": payload.product_id,
        "predicted_demand": payload.predicted_demand,
        "confidence_score": payload.confidence_score,
        "forecast_date": payload.forecast_date or datetime.utcnow().isoformat(),
        "forecast_period": payload.forecast_period or "weekly"
    }
    
    result = supabase.table("forecasts").insert(forecast_data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Could not create forecast")
    
    return {"message": "Forecast created", "forecast": result.data[0]}


@router.get("/forecasts/{product_id}")
async def get_product_forecasts(product_id: str, current_user: dict = Depends(get_current_user)):
    """Get forecasts for a specific product"""
    supabase = get_supabase_admin()
    
    # Verify product belongs to user
    product = supabase.table("products").select("id").eq("id", product_id).eq("user_id", current_user["user_id"]).execute()
    if not product.data:
        raise HTTPException(status_code=404, detail="Product not found")
    
    result = supabase.table("forecasts").select("*").eq("product_id", product_id).eq("user_id", current_user["user_id"]).order("forecast_date", desc=True).execute()
    return {"items": result.data or []}


@router.put("/forecasts/{forecast_id}")
async def update_forecast(forecast_id: str, payload: ForecastUpdate, current_user: dict = Depends(get_current_user)):
    """Update a forecast"""
    supabase = get_supabase_admin()
    
    update_data = payload.model_dump(exclude_unset=True)
    result = supabase.table("forecasts").update(update_data).eq("id", forecast_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Forecast not found")
    
    return {"message": "Forecast updated", "forecast": result.data[0]}


@router.delete("/forecasts/{forecast_id}")
async def delete_forecast(forecast_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a forecast"""
    supabase = get_supabase_admin()
    
    result = supabase.table("forecasts").delete().eq("id", forecast_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Forecast not found")
    
    return {"message": "Forecast deleted"}


@router.get("/forecasts/analytics/summary")
async def forecast_analytics(current_user: dict = Depends(get_current_user)):
    """Get forecast analytics summary"""
    supabase = get_supabase_admin()
    
    forecasts = supabase.table("forecasts").select("predicted_demand,confidence_score").eq("user_id", current_user["user_id"]).execute()
    items = forecasts.data or []
    
    if not items:
        return {
            "total_forecasts": 0,
            "avg_confidence": 0,
            "total_predicted_demand": 0,
            "confidence_range": {"min": 0, "max": 0}
        }
    
    confidences = [item.get("confidence_score", 0) for item in items]
    demands = [item.get("predicted_demand", 0) for item in items]
    
    return {
        "total_forecasts": len(items),
        "avg_confidence": sum(confidences) / len(confidences) if confidences else 0,
        "total_predicted_demand": sum(demands),
        "confidence_range": {
            "min": min(confidences) if confidences else 0,
            "max": max(confidences) if confidences else 0
        }
    }
