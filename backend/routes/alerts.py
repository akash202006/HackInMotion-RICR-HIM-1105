from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth import get_current_user
from app.database import get_supabase_admin
from app.schemas import AlertCreate, AlertUpdate

router = APIRouter()


@router.get("/alerts")
async def list_alerts(
    status: str = Query(None),
    priority: str = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get all alerts for current user"""
    supabase = get_supabase_admin()
    
    query = supabase.table("alerts").select("*").eq("user_id", current_user["user_id"])
    
    if status:
        query = query.eq("status", status)
    if priority:
        query = query.eq("priority", priority)
    
    result = query.order("created_at", desc=True).execute()
    return {"items": result.data or []}


@router.post("/alerts")
async def create_alert(payload: AlertCreate, current_user: dict = Depends(get_current_user)):
    """Create a new alert"""
    supabase = get_supabase_admin()
    
    # Verify product belongs to user
    product = supabase.table("products").select("id").eq("id", payload.product_id).eq("user_id", current_user["user_id"]).execute()
    if not product.data:
        raise HTTPException(status_code=404, detail="Product not found")
    
    alert_data = {
        "user_id": current_user["user_id"],
        "product_id": payload.product_id,
        "alert_type": payload.alert_type,
        "message": payload.message,
        "priority": payload.priority or "medium",
        "status": "active"
    }
    
    result = supabase.table("alerts").insert(alert_data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Could not create alert")
    
    return {"message": "Alert created", "alert": result.data[0]}


@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: str, current_user: dict = Depends(get_current_user)):
    """Get alert by ID"""
    supabase = get_supabase_admin()
    
    result = supabase.table("alerts").select("*").eq("id", alert_id).eq("user_id", current_user["user_id"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return result.data[0]


@router.put("/alerts/{alert_id}")
async def update_alert(alert_id: str, payload: AlertUpdate, current_user: dict = Depends(get_current_user)):
    """Update an alert"""
    supabase = get_supabase_admin()
    
    update_data = payload.model_dump(exclude_unset=True)
    result = supabase.table("alerts").update(update_data).eq("id", alert_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert updated", "alert": result.data[0]}


@router.patch("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str, current_user: dict = Depends(get_current_user)):
    """Mark alert as resolved"""
    supabase = get_supabase_admin()
    
    from datetime import datetime
    result = supabase.table("alerts").update({
        "status": "resolved",
        "resolved_at": datetime.utcnow().isoformat()
    }).eq("id", alert_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert resolved", "alert": result.data[0]}


@router.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an alert"""
    supabase = get_supabase_admin()
    
    result = supabase.table("alerts").delete().eq("id", alert_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert deleted"}


@router.get("/alerts/stats/summary")
async def alert_stats(current_user: dict = Depends(get_current_user)):
    """Get alert statistics"""
    supabase = get_supabase_admin()
    
    alerts = supabase.table("alerts").select("*").eq("user_id", current_user["user_id"]).execute()
    items = alerts.data or []
    
    active = sum(1 for a in items if a.get("status") == "active")
    resolved = sum(1 for a in items if a.get("status") == "resolved")
    critical = sum(1 for a in items if a.get("priority") == "critical")
    
    return {
        "total_alerts": len(items),
        "active_alerts": active,
        "resolved_alerts": resolved,
        "critical_alerts": critical,
        "by_type": {}
    }
