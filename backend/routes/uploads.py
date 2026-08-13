import csv
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.auth import get_current_user
from app.database import get_supabase_admin

router = APIRouter()


@router.post("/upload/products-csv")
async def upload_products_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload products from CSV file
    Expected CSV columns: name, sku, category, stock, price, supplier, lead_time, min_stock
    """
    supabase = get_supabase_admin()
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")
    
    try:
        contents = await file.read()
        csv_data = contents.decode('utf-8')
        reader = csv.DictReader(io.StringIO(csv_data))
        
        products = []
        errors = []
        
        for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
            try:
                product = {
                    "user_id": current_user["user_id"],
                    "name": row.get("name", "").strip(),
                    "sku": row.get("sku", "").strip(),
                    "category": row.get("category", "").strip(),
                    "stock": int(row.get("stock", 0)),
                    "price": float(row.get("price", 0)),
                    "supplier": row.get("supplier", "").strip(),
                    "lead_time": int(row.get("lead_time", 3)),
                    "min_stock": int(row.get("min_stock", 0))
                }
                
                # Validate required fields
                if not product["name"] or not product["sku"]:
                    errors.append(f"Row {row_num}: Name and SKU are required")
                    continue
                
                products.append(product)
            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid data format - {str(e)}")
                continue
        
        if not products:
            raise HTTPException(status_code=400, detail=f"No valid products found. Errors: {errors}")
        
        # Insert products in batches
        batch_size = 100
        inserted = 0
        
        for i in range(0, len(products), batch_size):
            batch = products[i:i+batch_size]
            result = supabase.table("products").insert(batch).execute()
            if result.data:
                inserted += len(result.data)
        
        return {
            "message": "CSV upload completed",
            "products_inserted": inserted,
            "total_products": len(products),
            "errors": errors if errors else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


@router.post("/upload/sales-csv")
async def upload_sales_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload sales data from CSV file
    Expected CSV columns: product_sku, quantity_sold, revenue, sale_date (YYYY-MM-DD)
    """
    supabase = get_supabase_admin()
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")
    
    try:
        contents = await file.read()
        csv_data = contents.decode('utf-8')
        reader = csv.DictReader(io.StringIO(csv_data))
        
        sales_records = []
        errors = []
        
        # First, get all products for the user
        products_result = supabase.table("products").select("id, sku").eq("user_id", current_user["user_id"]).execute()
        sku_to_id = {p["sku"]: p["id"] for p in products_result.data or []}
        
        for row_num, row in enumerate(reader, start=2):
            try:
                sku = row.get("product_sku", "").strip()
                
                if sku not in sku_to_id:
                    errors.append(f"Row {row_num}: Product SKU '{sku}' not found")
                    continue
                
                record = {
                    "user_id": current_user["user_id"],
                    "product_id": sku_to_id[sku],
                    "quantity_sold": int(row.get("quantity_sold", 0)),
                    "revenue": float(row.get("revenue", 0)),
                    "sale_date": row.get("sale_date", "").strip()
                }
                
                sales_records.append(record)
            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid data format - {str(e)}")
                continue
        
        if not sales_records:
            raise HTTPException(status_code=400, detail=f"No valid sales records found. Errors: {errors}")
        
        # Insert sales records in batches
        batch_size = 500
        inserted = 0
        
        for i in range(0, len(sales_records), batch_size):
            batch = sales_records[i:i+batch_size]
            result = supabase.table("sales_data").insert(batch).execute()
            if result.data:
                inserted += len(result.data)
        
        return {
            "message": "Sales CSV upload completed",
            "records_inserted": inserted,
            "total_records": len(sales_records),
            "errors": errors if errors else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


@router.get("/export/products-csv")
async def export_products_csv(current_user: dict = Depends(get_current_user)):
    """Export all products as CSV"""
    supabase = get_supabase_admin()
    
    result = supabase.table("products").select("*").eq("user_id", current_user["user_id"]).execute()
    products = result.data or []
    
    if not products:
        return {"message": "No products to export"}
    
    # Create CSV
    output = io.StringIO()
    fieldnames = ["name", "sku", "category", "stock", "price", "supplier", "lead_time", "min_stock", "created_at"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for product in products:
        writer.writerow({
            "name": product.get("name"),
            "sku": product.get("sku"),
            "category": product.get("category"),
            "stock": product.get("stock"),
            "price": product.get("price"),
            "supplier": product.get("supplier"),
            "lead_time": product.get("lead_time"),
            "min_stock": product.get("min_stock"),
            "created_at": product.get("created_at")
        })
    
    return {
        "message": "Export ready",
        "total_products": len(products),
        "csv_content": output.getvalue()
    }


@router.get("/export/sales-csv")
async def export_sales_csv(current_user: dict = Depends(get_current_user)):
    """Export sales data as CSV"""
    supabase = get_supabase_admin()
    
    result = supabase.table("sales_data").select("*").eq("user_id", current_user["user_id"]).execute()
    sales = result.data or []
    
    if not sales:
        return {"message": "No sales data to export"}
    
    # Create CSV
    output = io.StringIO()
    fieldnames = ["product_id", "quantity_sold", "revenue", "sale_date", "created_at"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for record in sales:
        writer.writerow({
            "product_id": record.get("product_id"),
            "quantity_sold": record.get("quantity_sold"),
            "revenue": record.get("revenue"),
            "sale_date": record.get("sale_date"),
            "created_at": record.get("created_at")
        })
    
    return {
        "message": "Export ready",
        "total_records": len(sales),
        "csv_content": output.getvalue()
    }
