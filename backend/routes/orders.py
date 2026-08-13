from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth import get_current_user
from app.database import get_supabase_admin
from app.schemas import OrderCreate, OrderUpdate
from datetime import datetime

router = APIRouter()


@router.get("/orders")
async def list_orders(
    status: str = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get all orders for current user"""
    supabase = get_supabase_admin()
    
    query = supabase.table("orders").select("*").eq("user_id", current_user["user_id"])
    
    if status:
        query = query.eq("status", status)
    
    result = query.order("created_at", desc=True).execute()
    return {"items": result.data or []}


@router.post("/orders")
async def create_order(payload: OrderCreate, current_user: dict = Depends(get_current_user)):
    """Create a new order (reorder request)"""
    supabase = get_supabase_admin()
    
    # Verify product belongs to user
    product = supabase.table("products").select("*").eq("id", payload.product_id).eq("user_id", current_user["user_id"]).execute()
    if not product.data:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_data = product.data[0]
    
    order_data = {
        "user_id": current_user["user_id"],
        "product_id": payload.product_id,
        "quantity": payload.quantity,
        "supplier": payload.supplier or product_data.get("supplier"),
        "expected_delivery": payload.expected_delivery,
        "status": "pending"
    }
    
    result = supabase.table("orders").insert(order_data).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Could not create order")
    
    return {"message": "Order created", "order": result.data[0]}


@router.get("/orders/{order_id}")
async def get_order(order_id: str, current_user: dict = Depends(get_current_user)):
    """Get order by ID"""
    supabase = get_supabase_admin()
    
    result = supabase.table("orders").select("*").eq("id", order_id).eq("user_id", current_user["user_id"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return result.data[0]


@router.put("/orders/{order_id}")
async def update_order(order_id: str, payload: OrderUpdate, current_user: dict = Depends(get_current_user)):
    """Update an order"""
    supabase = get_supabase_admin()
    
    update_data = payload.model_dump(exclude_unset=True)
    result = supabase.table("orders").update(update_data).eq("id", order_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order updated", "order": result.data[0]}


@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str, current_user: dict = Depends(get_current_user)):
    """Update order status"""
    allowed_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    
    if status not in allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {allowed_statuses}")
    
    supabase = get_supabase_admin()
    
    result = supabase.table("orders").update({
        "status": status,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", order_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": f"Order status updated to {status}", "order": result.data[0]}


@router.delete("/orders/{order_id}")
async def delete_order(order_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an order"""
    supabase = get_supabase_admin()
    
    result = supabase.table("orders").delete().eq("id", order_id).eq("user_id", current_user["user_id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order deleted"}


@router.get("/orders/product/{product_id}")
async def get_product_orders(product_id: str, current_user: dict = Depends(get_current_user)):
    """Get all orders for a specific product"""
    supabase = get_supabase_admin()
    
    # Verify product belongs to user
    product = supabase.table("products").select("id").eq("id", product_id).eq("user_id", current_user["user_id"]).execute()
    if not product.data:
        raise HTTPException(status_code=404, detail="Product not found")
    
    result = supabase.table("orders").select("*").eq("product_id", product_id).eq("user_id", current_user["user_id"]).order("created_at", desc=True).execute()
    return {"items": result.data or []}


@router.get("/orders/stats/summary")
async def order_stats(current_user: dict = Depends(get_current_user)):
    """Get order statistics"""
    supabase = get_supabase_admin()
    
    orders = supabase.table("orders").select("*").eq("user_id", current_user["user_id"]).execute()
    items = orders.data or []
    
    pending = sum(1 for o in items if o.get("status") == "pending")
    confirmed = sum(1 for o in items if o.get("status") == "confirmed")
    shipped = sum(1 for o in items if o.get("status") == "shipped")
    delivered = sum(1 for o in items if o.get("status") == "delivered")
    
    total_quantity = sum(o.get("quantity", 0) for o in items)
    
    return {
        "total_orders": len(items),
        "pending": pending,
        "confirmed": confirmed,
        "shipped": shipped,
        "delivered": delivered,
        "total_quantity_ordered": total_quantity
    }
