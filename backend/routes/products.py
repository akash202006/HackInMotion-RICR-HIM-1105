from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import get_current_user
from app.database import get_supabase_admin
from app.schemas import ProductCreate, ProductUpdate

router = APIRouter()


@router.get("/products")
async def list_products(current_user: dict = Depends(get_current_user)):
    supabase = get_supabase_admin()
    result = supabase.table("products").select("*").eq("user_id", current_user["user_id"]).execute()
    return {"items": result.data}


@router.post("/products")
async def create_product(payload: ProductCreate, current_user: dict = Depends(get_current_user)):
    supabase = get_supabase_admin()
    item = {
        "user_id": current_user["user_id"],
        "name": payload.name,
        "sku": payload.sku,
        "category": payload.category,
        "stock": payload.stock,
        "price": payload.price,
        "supplier": payload.supplier,
        "lead_time": payload.lead_time,
        "min_stock": payload.min_stock,
    }
    result = supabase.table("products").insert(item).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Could not create product")
    return {"message": "Product created", "product": result.data[0]}


@router.get("/products/{product_id}")
async def get_product(product_id: str, current_user: dict = Depends(get_current_user)):
    supabase = get_supabase_admin()
    result = supabase.table("products").select("*").eq("id", product_id).eq("user_id", current_user["user_id"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return result.data[0]


@router.put("/products/{product_id}")
async def update_product(product_id: str, payload: ProductUpdate, current_user: dict = Depends(get_current_user)):
    supabase = get_supabase_admin()
    update_data = payload.model_dump(exclude_unset=True)
    result = supabase.table("products").update(update_data).eq("id", product_id).eq("user_id", current_user["user_id"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated", "product": result.data[0]}


@router.delete("/products/{product_id}")
async def delete_product(product_id: str, current_user: dict = Depends(get_current_user)):
    supabase = get_supabase_admin()
    result = supabase.table("products").delete().eq("id", product_id).eq("user_id", current_user["user_id"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
