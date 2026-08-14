# 🚀 SMART AI FORECASTING

> **AI-Powered Retail Inventory Management & Demand Forecasting Platform**

**Team:** HACKINMOTION-RICR-HIM-1105

SMART AI FORECASTING is a full-stack AI-powered inventory management platform designed to help retailers monitor stock, analyze historical sales, forecast future demand, identify low-stock situations, and make smarter inventory decisions.

The platform combines **AI/ML-based demand forecasting, automated stock alerts, CSV data processing, inventory management, analytics, and secure user authentication** into a single web application.

---

> [!NOTE]
>
> ## 🚧 Project Status — MVP Completed
>
> **SMART AI FORECASTING is currently a work-in-progress project and is not the final production-ready product yet.**
>
> We have successfully developed the **Minimum Viable Product (MVP)** with the core functionality, including **inventory management, AI-powered demand forecasting, stock alerts, CSV data processing, authentication, analytics, and backend APIs**.
>
> The team is continuously working on improving the platform, refining the AI/ML forecasting capabilities, enhancing security, optimizing performance, improving the user experience, and adding additional features before the final release.
>
> **Current Status:** ✅ MVP Completed | 🚧 Further Development in Progress

---

# 📌 Problem

Retail businesses frequently face inventory-related challenges such as:

* Overstocking products with low demand
* Stockouts of high-demand products
* Difficulty predicting future product demand
* Manual inventory tracking
* Lack of centralized sales and inventory analytics
* Delayed identification of low-stock products
* Inefficient reorder decisions
* Large historical CSV datasets that are difficult to analyze manually

These problems can result in:

**Lost Sales + Excess Inventory + Increased Operational Cost + Poor Customer Experience**

---

# 💡 Solution

SMART AI FORECASTING provides an intelligent inventory management platform that transforms historical sales and inventory data into actionable insights.

The system allows store managers to:

1. Upload product and historical sales data through CSV.
2. Manage inventory from a centralized dashboard.
3. Monitor stock levels.
4. Analyze historical sales performance.
5. Generate AI-powered demand forecasts.
6. Detect low-stock and critical-stock conditions.
7. Receive actionable inventory alerts.
8. Create and manage reorder requests.
9. Export inventory and sales data.
10. Securely manage users and their business data.

### Core Workflow

```text
CSV / Inventory Data
        ↓
   Data Processing
        ↓
   Historical Sales
        ↓
    AI Forecasting
        ↓
 Demand Prediction
        ↓
 Stock Analysis
        ↓
 Alerts & Insights
        ↓
 Reorder Decisions
```

---

# ⭐ Key Features

## 📊 Smart Dashboard

* Total products overview
* Current inventory status
* Low-stock count
* Critical-stock count
* Sales analytics
* Forecast summaries
* Inventory KPIs

## 📦 Inventory Management

* Add products
* Edit products
* Delete products
* Search and manage inventory
* SKU management
* Stock-level tracking
* Minimum stock threshold
* Supplier information
* Lead-time tracking

## 🤖 AI Demand Forecasting

* Historical sales analysis
* Future demand prediction
* Product-level forecasting
* Predicted demand values
* Forecast confidence score
* Forecast analytics

## 🚨 Smart Stock Alerts

* Low-stock alerts
* Critical-stock alerts
* Inventory warnings
* Alert priority levels
* Alert resolution
* Alert filtering

## 🛒 Reorder Management

* Create reorder requests
* Product-wise reorder quantity
* Order status tracking
* Reorder statistics

## 📁 CSV Import & Export

* Import products through CSV
* Import historical sales through CSV
* Export product data
* Export sales data
* Bulk data processing

## 🔐 Secure Authentication

* User signup
* User login
* JWT authentication
* Protected application routes
* Token-based API authorization
* User-specific data access

## 🗄️ Database & Data Security

* PostgreSQL database through Supabase
* Row Level Security (RLS)
* User-specific records
* Audit logging
* Secure backend database access

---

# 🤖 AI/ML

SMART AI FORECASTING uses historical sales information to estimate future product demand.

### Forecasting Pipeline

```text
Historical Sales Data
        ↓
Data Cleaning
        ↓
Data Processing
        ↓
Feature Preparation
        ↓
Demand Forecasting Model
        ↓
Predicted Demand
        ↓
Confidence Score
        ↓
Inventory Recommendation
```

### AI/ML Inputs

The forecasting system can use information such as:

* Product ID
* Product category
* Historical sales quantity
* Sales date
* Revenue
* Previous demand patterns
* Current stock
* Minimum stock level
* Supplier lead time

### AI/ML Outputs

The system generates:

* Predicted future demand
* Forecast confidence score
* Product-level demand insights
* Inventory planning information

### Planned ML Improvements

The architecture can be extended with:

* XGBoost
* Random Forest
* Prophet
* ARIMA
* LSTM
* Time-series forecasting
* Seasonal demand analysis
* Anomaly detection

---

# 🧰 Technology Stack

| Layer             | Technology                      |
| ----------------- | ------------------------------- |
| Frontend          | HTML5, CSS3, Vanilla JavaScript |
| Backend           | Python, FastAPI                 |
| Database          | PostgreSQL                      |
| Database Platform | Supabase                        |
| Authentication    | JWT                             |
| API               | REST API                        |
| Data Validation   | Pydantic                        |
| AI/ML             | Python-based forecasting        |
| Real-Time         | Supabase Subscriptions          |
| Data Import       | CSV                             |
| Deployment        | Vercel + Backend Cloud Platform |
| Version Control   | Git & GitHub                    |

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │        USER         │
                    │    Store Manager    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FRONTEND       │
                    │   HTML / CSS / JS   │
                    │                     │
                    │ Dashboard           │
                    │ Inventory           │
                    │ Forecast            │
                    │ Alerts              │
                    └──────────┬──────────┘
                               │
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │       FASTAPI       │
                    │       BACKEND       │
                    ├─────────────────────┤
                    │ Authentication      │
                    │ Products API        │
                    │ Dashboard API       │
                    │ Forecast API        │
                    │ Alerts API          │
                    │ Orders API          │
                    │ CSV API             │
                    └───────┬─────┬───────┘
                            │     │
               ┌────────────┘     └────────────┐
               ▼                               ▼
     ┌──────────────────┐            ┌──────────────────┐
     │     AI/ML LAYER  │            │     SUPABASE     │
     │                  │            │    PostgreSQL     │
     │ Demand Forecast  │            │                  │
     │ Prediction       │            │ Users            │
     │ Analytics        │            │ Products         │
     │ Confidence       │            │ Sales Data       │
     └────────┬─────────┘            │ Forecasts        │
              │                      │ Alerts           │
              ▼                      │ Orders           │
     ┌──────────────────┐            │ Audit Logs       │
     │ Recommendations  │            └──────────────────┘
     │ & Alerts         │
     └──────────────────┘
```

---

# 📁 Project Structure

```text
HACKINMOTION-RICR-HIM-1105/
│
├── frontend/
│   ├── index.html
│   ├── auth.html
│   ├── dashboard.html
│   ├── inventory.html
│   ├── forecast.html
│   ├── alerts.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── main.js
│   │
│   └── logo.svg
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   │
│   └── app/
│       ├── config.py
│       ├── database.py
│       ├── auth.py
│       ├── schemas.py
│       │
│       └── routes/
│           ├── auth.py
│           ├── products.py
│           ├── dashboard.py
│           ├── forecasts.py
│           ├── alerts.py
│           ├── orders.py
│           └── uploads.py
│
├── database/
│   ├── 01_schema.sql
│   └── README.md
│
└── README.md
```

---

# ⚙️ Installation

## Prerequisites

Make sure the following are installed:

* Python 3.9+
* Git
* VS Code or another code editor
* Supabase account
* Modern web browser

Node.js is optional because the frontend is built using Vanilla JavaScript and does not require a build system.

---

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd HACKINMOTION-RICR-HIM-1105
```

---

## 2. Configure Supabase

Create a new project on Supabase.

Navigate to:

```text
Supabase Dashboard
→ Project Settings
→ API
```

Obtain:

```text
Project URL
Anon Key
Service Role Key
```

Then open:

```text
database/01_schema.sql
```

Copy the complete SQL script into:

```text
Supabase
→ SQL Editor
→ New Query
```

Execute the SQL script.

This creates the required:

* Tables
* Indexes
* RLS policies
* Database structure
* Security rules

---

## 3. Install Backend Dependencies

```bash
cd backend

pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file inside the `backend/` directory.

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE=your-service-role-key
```

### ⚠️ Important Security Rule

**Never commit `.env` to GitHub.**

Add it to `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
```

Only store environment variables in the deployment platform's secure environment-variable settings.

---

# ▶️ Running Locally

## Start Backend

From the `backend/` directory:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Backend:

```text
http://localhost:8001
```

API Documentation:

```text
http://localhost:8001/docs
```

Health Check:

```text
http://localhost:8001/health
```

---

## Start Frontend

Open another terminal:

```bash
cd frontend

python -m http.server 8000
```

Frontend:

```text
http://localhost:8000
```

---

# 📄 CSV Format

## Products CSV

Example:

```csv
name,sku,category,stock,price,supplier,lead_time,min_stock
Pepsi 750ml,SKU-001,Beverages,100,45,XYZ Dist.,3,20
Lays Classic,SKU-002,Snacks,80,20,ABC Foods,2,15
```

### Required Product Fields

| Field       | Description             |
| ----------- | ----------------------- |
| `name`      | Product name            |
| `sku`       | Unique product SKU      |
| `category`  | Product category        |
| `stock`     | Current inventory       |
| `price`     | Product price           |
| `supplier`  | Supplier name           |
| `lead_time` | Supplier lead time      |
| `min_stock` | Minimum stock threshold |

---

## Sales CSV

Example:

```csv
product_id,quantity_sold,revenue,date
PRODUCT-UUID-1,25,1125,2026-08-01
PRODUCT-UUID-1,30,1350,2026-08-02
PRODUCT-UUID-2,15,300,2026-08-02
```

### Required Sales Fields

| Field           | Description       |
| --------------- | ----------------- |
| `product_id`    | Product UUID      |
| `quantity_sold` | Quantity sold     |
| `revenue`       | Revenue generated |
| `date`          | Sales date        |

---

# 🔌 API Documentation

## Authentication

```text
POST /api/auth/login
POST /api/auth/signup
```

## Products

```text
GET    /api/products
POST   /api/products
GET    /api/products/{id}
PUT    /api/products/{id}
DELETE /api/products/{id}
```

## Dashboard

```text
GET /api/dashboard
```

## Forecasts

```text
GET /api/forecasts
POST /api/forecasts
GET /api/forecasts/{product_id}
GET /api/forecasts/analytics/summary
```

## Alerts

```text
GET    /api/alerts
POST   /api/alerts
PATCH  /api/alerts/{id}/resolve
DELETE /api/alerts/{id}
```

## Orders

```text
GET   /api/orders
POST  /api/orders
PATCH /api/orders/{id}/status
GET   /api/orders/stats/summary
```

## CSV Import / Export

```text
POST /api/upload/products-csv
POST /api/upload/sales-csv

GET /api/export/products-csv
GET /api/export/sales-csv
```

## Health

```text
GET /
GET /health
```

### Interactive API Documentation

Once the backend is running, Swagger UI is available at:

```text
http://localhost:8001/docs
```

---

# 🖼️ Screenshots

Add screenshots of the main application pages here.

### Landing Page

```markdown
![Landing Page](screenshots/landing.png)
```

### Authentication

```markdown
![Authentication](screenshots/auth.png)
```

### Dashboard

```markdown
![Dashboard](screenshots/dashboard.png)
```

### Inventory Management

```markdown
![Inventory](screenshots/inventory.png)
```

### AI Forecasting

```markdown
![Forecast](screenshots/forecast.png)
```

### Alerts

```markdown
![Alerts](screenshots/alerts.png)
```

> Create a `screenshots/` folder in the repository and place the corresponding images inside it.

---

# 🛡️ Security

Security is an important part of SMART AI FORECASTING.

### Authentication Security

* JWT-based authentication
* Protected application routes
* Authorization header for API requests
* Secure login/signup flow

### Database Security

* Supabase PostgreSQL
* Row Level Security (RLS)
* User-specific data access
* Service-role access restricted to backend

### API Security

* Protected API endpoints
* Token validation
* Pydantic request validation
* CORS configuration
* Controlled database access

### Data Security

* Environment variables for secrets
* `.env` excluded from Git
* Audit logging
* User-isolated records

### Security Architecture

```text
User
 ↓
JWT Authentication
 ↓
FastAPI Authorization
 ↓
Validated Request
 ↓
Supabase RLS
 ↓
Protected Data
```

---

# 🧪 Testing

Testing should cover the major application components.

### Frontend Testing

* Login/signup UI
* Dashboard rendering
* Inventory CRUD
* Forecast page
* Alert page
* CSV upload interface
* Responsive layout

### Backend Testing

* Authentication endpoints
* Product CRUD endpoints
* Dashboard API
* Forecast APIs
* Alert APIs
* Order APIs
* CSV import/export APIs
* Health endpoint

### Database Testing

* Table creation
* RLS policies
* User data isolation
* CRUD operations
* Foreign-key relationships

### API Testing

Swagger UI can be used to test the API:

```text
http://localhost:8001/docs
```

---

# 🚀 Deployment

## Frontend

The static frontend can be deployed using platforms such as:

* Vercel
* Netlify
* GitHub Pages

For Vercel, deploy the `frontend/` directory.

No frontend build step is required.

---

## Backend

The FastAPI backend can be deployed on:

* Render
* Railway
* Heroku
* Other Python-compatible cloud platforms

Example production command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Deployment Architecture

```text
                    USERS
                      │
                      ▼
              ┌───────────────┐
              │ Vercel / CDN  │
              │   Frontend    │
              └───────┬───────┘
                      │
                      │ HTTPS / REST API
                      ▼
              ┌───────────────┐
              │ FastAPI       │
              │ Backend       │
              └───────┬───────┘
                      │
               ┌──────┴──────┐
               ▼             ▼
        ┌────────────┐  ┌──────────────┐
        │ AI/ML      │  │ Supabase     │
        │ Forecasting│  │ PostgreSQL   │
        └────────────┘  └──────────────┘
```

---

# 👥 Team Members

## HACKINMOTION-RICR-HIM-1105

| Member                | Role                                 |
| --------------------- | ------------------------------------ |
| **Akash Choudhary**   | Team Leader — Full Stack Development |
| **Alok Pratap Gupta** | Backend & Database                   |
| **Ali Ahmad Sadat**   | Frontend Development                 |
| **Lokesh Yadav**      | System Architecture Designing        |

### Team Responsibilities

### 👨‍💻 Akash Choudhary — Team Leader / Full Stack Development

* Overall project development
* Frontend-backend integration
* API integration
* Application functionality
* Project coordination

### 🗄️ Alok Pratap Gupta — Backend & Database

* FastAPI backend
* Supabase PostgreSQL
* Database schema
* API development
* Authentication and data management

### 🎨 Ali Ahmad Sadat — Frontend Development

* UI development
* HTML/CSS implementation
* JavaScript functionality
* Dashboard and application pages
* Frontend user experience

### 🏗️ Lokesh Yadav — System Architecture Designing

* System architecture
* Application workflow
* Technical architecture planning
* Component integration design
* System-level documentation

---

# 🔮 Future Scope

SMART AI FORECASTING can be extended into a complete intelligent retail inventory ecosystem.

## 🤖 Advanced AI

* Deep learning-based forecasting
* LSTM time-series models
* XGBoost demand prediction
* Seasonal demand detection
* Product demand anomaly detection
* Automated model selection

## 📈 Advanced Analytics

* Sales trend analysis
* Customer demand patterns
* Product performance scoring
* Revenue forecasting
* Inventory turnover analysis
* Profit optimization

## 🧠 Intelligent Recommendations

The system can automatically recommend:

```text
What to order?
How much to order?
When to order?
Which products need attention?
Which products are overstocked?
Which products are likely to run out?
```

## 🔔 Advanced Alerts

* Email notifications
* WhatsApp notifications
* SMS alerts
* Automated reorder recommendations
* Predictive stockout warnings

## ☁️ Scalability

* Multi-store management
* Multi-tenant architecture
* Cloud-based AI inference
* Distributed data processing
* Enterprise-scale deployment

## 📱 Mobile Application

A future mobile application can provide:

* Mobile dashboard
* Inventory management
* Push notifications
* Forecast monitoring
* Reorder approvals

## 🔗 Future Integrations

Potential integrations include:

* POS systems
* E-commerce platforms
* ERP systems
* Supplier APIs
* Payment systems
* Business intelligence platforms

---

# 📜 License

This project is developed as an **internal hackathon project** by:

**HACKINMOTION-RICR-HIM-1105**

---

# ❤️ Built by HACKINMOTION-RICR-HIM-1105

> **SMART AI FORECASTING**
>
> *Turning retail data into intelligent inventory decisions.*
