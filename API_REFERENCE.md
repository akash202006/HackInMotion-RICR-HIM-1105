# API Quick Reference Card

## 🔑 Supabase Credentials (Already Configured)

**Supabase URL**: `https://fdeilubldzcjzerbpkdgss.supabase.co`

**Keys Location**: `backend/.env`

---

## 🚀 API Base URL

```
http://localhost:8001/api
```

---

## 📝 Authentication

### Signup
```bash
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe",
  "role": "store_manager"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "store_manager",
    "created_at": "2026-08-13T..."
  }
}
```

### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

---

## 🏪 Products

### List Products
```bash
GET /products
Authorization: Bearer <token>
```

### Create Product
```bash
POST /products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Pepsi 750ml",
  "sku": "SKU-003",
  "category": "Beverages",
  "stock": 150,
  "price": 35.00,
  "supplier": "PQR Ltd.",
  "lead_time": 2,
  "min_stock": 30,
  "max_stock": 500
}
```

### Get Product
```bash
GET /products/{product-uuid}
Authorization: Bearer <token>
```

### Update Product
```bash
PUT /products/{product-uuid}
Authorization: Bearer <token>
Content-Type: application/json

{
  "stock": 120,
  "price": 36.00
}
```

### Delete Product
```bash
DELETE /products/{product-uuid}
Authorization: Bearer <token>
```

---

## 📊 Dashboard

### Get KPIs
```bash
GET /dashboard
Authorization: Bearer <token>

Response:
{
  "total_products": 24,
  "low_stock_count": 3,
  "overstock_count": 2,
  "healthy_stock_count": 19,
  "forecast_accuracy": 92.0,
  "stockout_rate": -35.0,
  "products": [...]
}
```

---

## 🔮 Forecasts

### List Forecasts
```bash
GET /forecasts
Authorization: Bearer <token>
```

### Create Forecast
```bash
POST /forecasts
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": "product-uuid",
  "predicted_demand": 150,
  "confidence_score": 92.5,
  "forecast_date": "2026-08-20T00:00:00",
  "forecast_period": "weekly"
}
```

### Get Forecast Analytics
```bash
GET /forecasts/analytics/summary
Authorization: Bearer <token>
```

---

## 🚨 Alerts

### List Alerts
```bash
GET /alerts
GET /alerts?status=active
GET /alerts?priority=critical
GET /alerts?status=active&priority=high
Authorization: Bearer <token>
```

### Create Alert
```bash
POST /alerts
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": "product-uuid",
  "alert_type": "low_stock",
  "message": "Stock level below minimum threshold",
  "priority": "high"
}
```

### Resolve Alert
```bash
PATCH /alerts/{alert-uuid}/resolve
Authorization: Bearer <token>
```

### Alert Stats
```bash
GET /alerts/stats/summary
Authorization: Bearer <token>
```

---

## 📦 Orders

### List Orders
```bash
GET /orders
GET /orders?status=pending
Authorization: Bearer <token>
```

### Create Order
```bash
POST /orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": "product-uuid",
  "quantity": 50,
  "supplier": "ABC Distributor",
  "expected_delivery": "2026-08-20T00:00:00"
}
```

### Update Order Status
```bash
PATCH /orders/{order-uuid}/status
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "confirmed"
}

Valid statuses: pending, confirmed, shipped, delivered, cancelled
```

### Order Stats
```bash
GET /orders/stats/summary
Authorization: Bearer <token>
```

---

## 📁 Upload & Export

### Upload Products CSV
```bash
POST /upload/products-csv
Authorization: Bearer <token>
Content-Type: multipart/form-data

Expected CSV columns:
name, sku, category, stock, price, supplier, lead_time, min_stock

Example:
Pepsi 750ml,SKU-003,Beverages,150,35.00,PQR Ltd.,2,30
Coca-Cola 500ml,SKU-005,Beverages,80,30.00,PQR Ltd.,2,25
```

### Export Products CSV
```bash
GET /export/products-csv
Authorization: Bearer <token>

Returns CSV file with all products
```

### Upload Sales Data CSV
```bash
POST /upload/sales-csv
Authorization: Bearer <token>
Content-Type: multipart/form-data

Expected CSV columns:
product_sku, quantity_sold, revenue, sale_date (YYYY-MM-DD)

Example:
SKU-003,50,1750.00,2026-08-13
SKU-005,30,900.00,2026-08-13
```

### Export Sales CSV
```bash
GET /export/sales-csv
Authorization: Bearer <token>

Returns CSV file with all sales records
```

---

## ✅ Health Check

```bash
GET /health
GET /

No authorization needed
```

---

## 🧪 Testing with cURL

### Login
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

### List Products
```bash
curl -X GET http://localhost:8001/api/products \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Product
```bash
curl -X POST http://localhost:8001/api/products \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "sku": "TEST-001",
    "category": "Test",
    "stock": 100,
    "price": 50.00,
    "supplier": "Test Supplier",
    "lead_time": 3,
    "min_stock": 10
  }'
```

---

## 🌐 Testing with Postman

1. Download Postman: https://www.postman.com/downloads/
2. Create new collection
3. Add requests following examples above
4. Set Authorization header: `Bearer {token}`
5. Use http://localhost:8001/api as base URL

---

## 📚 Interactive API Docs

Visit: **http://localhost:8001/docs**

(Swagger UI with live testing)

---

## ⚠️ Error Responses

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad request
- `401` - Unauthorized (missing/invalid token)
- `404` - Not found
- `500` - Server error

---

**Last Updated**: 2026-08-13
