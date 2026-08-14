# 🏗️ SMART AI FORECASTING — Technical Architecture

> **AI-Powered Retail Inventory Management & Demand Forecasting Platform**

**Team:** HACKINMOTION-RICR-HIM-1105  
**Project Status:** MVP Completed — Further Development in Progress

---

# 1. Architecture Overview

SMART AI FORECASTING follows a modular **Full-Stack + AI/ML architecture** designed for scalability, security, and maintainability.

The application consists of the following major layers:

```text
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                           │
│                  Store Manager / Admin                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│                  HTML5 + CSS3 + JavaScript                 │
│                                                             │
│ Dashboard │ Inventory │ Forecast │ Alerts │ Authentication │
└───────────────────────────┬─────────────────────────────────┘
                            │
                       REST API / HTTP
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                      │
│                         FastAPI                             │
│                                                             │
│ Auth │ Products │ Dashboard │ Forecast │ Alerts │ Orders   │
│                     CSV Import / Export                    │
└───────────────┬───────────────────────┬─────────────────────┘
                │                       │
                ▼                       ▼
┌──────────────────────────┐   ┌──────────────────────────────┐
│       AI/ML LAYER        │   │       DATA LAYER             │
│                          │   │                              │
│ Demand Forecasting       │   │ Supabase PostgreSQL          │
│ Prediction               │   │ Users                        │
│ Analytics                │   │ Products                     │
│ Confidence Score         │   │ Sales Data                   │
│ Recommendations          │   │ Forecasts                    │
│                          │   │ Alerts / Orders / Audit Logs │
└──────────────────────────┘   └──────────────────────────────┘
```

---

# 2. Technology Stack

## 2.1 Frontend

| Technology | Purpose |
|---|---|
| **HTML5** | Application structure |
| **CSS3** | UI styling and responsive design |
| **Vanilla JavaScript** | Frontend logic and API communication |
| **Fetch API** | REST API requests |
| **LocalStorage** | JWT token storage and session handling |
| **SVG** | Brand/logo assets |

### Frontend Pages

```text
index.html
    │
    ├── auth.html
    │
    ├── dashboard.html
    │
    ├── inventory.html
    │
    ├── forecast.html
    │
    └── alerts.html
```

---

# 2.2 Backend

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Backend programming language |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **Pydantic** | Request/response validation |
| **JWT** | Authentication and authorization |
| **Python-dotenv / Environment Variables** | Secret configuration |

FastAPI acts as the central application layer between the frontend, AI/ML services, and database.

---

# 2.3 Database

| Technology | Purpose |
|---|---|
| **Supabase** | Backend-as-a-Service platform |
| **PostgreSQL** | Relational database |
| **Row Level Security (RLS)** | User-level data isolation |
| **Supabase Realtime** | Real-time data subscriptions |

### Main Database Tables

```text
users
products
sales_data
forecasts
alerts
orders
audit_logs
```

---

# 2.4 AI/ML

The AI/ML layer is responsible for analyzing historical sales data and generating demand forecasts.

### Current/Planned AI Components

```text
Historical Sales
       ↓
Data Processing
       ↓
Feature Preparation
       ↓
Demand Forecasting
       ↓
Predicted Demand
       ↓
Confidence Score
       ↓
Inventory Recommendation
```

Potential models and algorithms for further development:

- Time-Series Forecasting
- XGBoost
- Random Forest
- ARIMA
- Prophet
- LSTM
- Anomaly Detection

---

# 2.5 Data Processing

CSV data enters the platform through dedicated upload APIs.

```text
CSV File
   ↓
Upload API
   ↓
Validation
   ↓
Data Cleaning
   ↓
Data Transformation
   ↓
Database
   ↓
AI/ML Processing
```

The system supports:

- Product CSV import
- Historical sales CSV import
- Product CSV export
- Sales CSV export

---

# 3. Complete System Architecture

```text
                              ┌───────────────────┐
                              │       USER        │
                              │   Store Manager   │
                              └─────────┬─────────┘
                                        │
                                        ▼
                         ┌──────────────────────────┐
                         │       FRONTEND           │
                         │                          │
                         │ HTML5                    │
                         │ CSS3                     │
                         │ Vanilla JavaScript       │
                         │                          │
                         │ ┌──────────────────────┐ │
                         │ │ Dashboard            │ │
                         │ │ Inventory            │ │
                         │ │ Forecast             │ │
                         │ │ Alerts               │ │
                         │ │ Authentication       │ │
                         │ └──────────────────────┘ │
                         └────────────┬─────────────┘
                                      │
                                      │ HTTPS / REST
                                      ▼
                     ┌────────────────────────────────┐
                     │            FASTAPI             │
                     │            BACKEND             │
                     │                                │
                     │ ┌──────────┐ ┌──────────────┐ │
                     │ │   Auth   │ │  Products    │ │
                     │ ├──────────┤ ├──────────────┤ │
                     │ │Dashboard │ │  Forecasts   │ │
                     │ ├──────────┤ ├──────────────┤ │
                     │ │ Alerts   │ │    Orders    │ │
                     │ ├──────────┤ ├──────────────┤ │
                     │ │ CSV APIs │ │ Authorization │ │
                     │ └──────────┘ └──────────────┘ │
                     └──────────────┬─────────────────┘
                                    │
                    ┌───────────────┴────────────────┐
                    │                                │
                    ▼                                ▼
          ┌────────────────────┐          ┌─────────────────────┐
          │      AI/ML         │          │      SUPABASE       │
          │                    │          │     PostgreSQL      │
          │ Demand Forecasting │          │                     │
          │ Prediction         │          │ Users               │
          │ Analytics          │          │ Products            │
          │ Confidence Score   │          │ Sales Data          │
          │ Recommendations    │          │ Forecasts           │
          └──────────┬─────────┘          │ Alerts              │
                     │                    │ Orders              │
                     ▼                    │ Audit Logs          │
          ┌────────────────────┐          └─────────────────────┘
          │ Inventory Insights │
          │ & Recommendations  │
          └────────────────────┘
```

---

# 4. Application Layer Architecture

The backend follows a modular route-based architecture.

```text
backend/
│
├── main.py
│
└── app/
    │
    ├── config.py
    │
    ├── database.py
    │
    ├── auth.py
    │
    ├── schemas.py
    │
    └── routes/
        │
        ├── auth.py
        ├── products.py
        ├── dashboard.py
        ├── forecasts.py
        ├── alerts.py
        ├── orders.py
        └── uploads.py
```

### Responsibilities

**`main.py`**

Application entry point and FastAPI initialization.

**`config.py`**

Application configuration and environment variables.

**`database.py`**

Supabase/PostgreSQL client initialization and database connectivity.

**`auth.py`**

JWT authentication and password-related utilities.

**`schemas.py`**

Pydantic request and response models.

**`routes/auth.py`**

User signup and login.

**`routes/products.py`**

Inventory CRUD operations.

**`routes/dashboard.py`**

Dashboard KPIs and analytics.

**`routes/forecasts.py`**

Demand forecasting and forecast analytics.

**`routes/alerts.py`**

Stock alert creation, retrieval, filtering, and resolution.

**`routes/orders.py`**

Reorder request management.

**`routes/uploads.py`**

CSV import/export functionality.

---

# 5. API Architecture

The frontend communicates with FastAPI through REST APIs.

```text
Frontend
    │
    │ HTTP Request
    ▼
FastAPI Router
    │
    ▼
Authentication / Validation
    │
    ▼
Business Logic
    │
    ├───────────────┐
    ▼               ▼
Database          AI/ML
    │               │
    └───────┬───────┘
            ▼
       API Response
            │
            ▼
         Frontend
```

---

# 6. API Endpoints

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

## CSV

```text
POST /api/upload/products-csv
POST /api/upload/sales-csv

GET /api/export/products-csv
GET /api/export/sales-csv
```

## Health

```text
GET /health
GET /
```

---

# 7. Authentication Architecture

SMART AI FORECASTING uses JWT-based authentication.

```text
                 USER
                   │
                   ▼
            Login / Signup
                   │
                   ▼
            FastAPI Auth API
                   │
                   ▼
          Credential Validation
                   │
                   ▼
             JWT Token
                   │
                   ▼
              Frontend
                   │
                   ▼
             localStorage
                   │
                   ▼
      Authorization: Bearer <JWT>
                   │
                   ▼
          Protected API Route
                   │
                   ▼
           Token Validation
                   │
             ┌─────┴─────┐
             │           │
           Valid       Invalid
             │           │
             ▼           ▼
         Continue     Reject /
         Request      Redirect
```

---

# 8. Database Architecture

Supabase provides PostgreSQL as the primary database.

```text
                         SUPABASE
                            │
                    PostgreSQL Database
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
       ▼                    ▼                    ▼
     users              products            sales_data
       │                    │                    │
       │                    │                    │
       └────────────┬───────┴────────────┬───────┘
                    │                    │
                    ▼                    ▼
                forecasts              alerts
                    │                    │
                    └─────────┬──────────┘
                              ▼
                            orders
                              │
                              ▼
                         audit_logs
```

---

# 9. Row Level Security Architecture

Database access is isolated using Supabase Row Level Security.

```text
User A
   │
   ├── Product A
   ├── Sales A
   ├── Forecast A
   └── Alerts A

User B
   │
   ├── Product B
   ├── Sales B
   ├── Forecast B
   └── Alerts B
```

Users should only be able to access records associated with their account.

The backend service role is restricted to server-side operations.

---

# 10. AI Forecasting Architecture

The demand forecasting pipeline is designed around historical sales data.

```text
             Historical Sales
                    │
                    ▼
            Data Validation
                    │
                    ▼
             Data Cleaning
                    │
                    ▼
           Feature Engineering
                    │
                    ▼
          Forecasting Algorithm
                    │
                    ▼
            Demand Prediction
                    │
                    ▼
          Confidence Estimation
                    │
                    ▼
        Inventory Risk Analysis
                    │
             ┌──────┴──────┐
             ▼             ▼
         Low Stock      Healthy Stock
             │
             ▼
       Reorder Alert
```

---

# 11. Inventory Decision Flow

The platform converts forecasting output into inventory decisions.

```text
Historical Sales
       ↓
Demand Forecast
       ↓
Predicted Demand
       ↓
Compare With Current Stock
       ↓
Compare With Minimum Stock
       ↓
Check Supplier Lead Time
       ↓
Risk Evaluation
       ↓
┌───────────────────────────────┐
│ Stock Status                  │
├───────────────────────────────┤
│ Healthy                       │
│ Low Stock                     │
│ Critical Stock                │
└───────────────┬───────────────┘
                │
                ▼
        Alert / Recommendation
                │
                ▼
          Reorder Decision
```

---

# 12. CSV Data Architecture

```text
                 CSV FILE
                    │
                    ▼
              Upload Endpoint
                    │
                    ▼
               Validation
                    │
                    ▼
              Data Cleaning
                    │
                    ▼
             Data Processing
                    │
                    ▼
              PostgreSQL
                    │
           ┌────────┴────────┐
           ▼                 ▼
     Dashboard          AI Forecasting
                             │
                             ▼
                       Demand Prediction
```

---

# 13. Real-Time Architecture

Supabase Realtime can be used for live application updates.

```text
             Database Change
                    │
                    ▼
            Supabase Realtime
                    │
                    ▼
             Subscription
                    │
                    ▼
               Frontend
                    │
                    ▼
          UI Updates Automatically
```

Potential real-time use cases:

- Stock level updates
- New alerts
- Alert resolution
- Order status updates
- Inventory changes

---

# 14. Security Architecture

The security model uses multiple layers.

```text
┌───────────────────────────────┐
│          USER REQUEST         │
└───────────────┬───────────────┘
                ▼
        HTTPS / Secure Transport
                │
                ▼
        JWT Authentication
                │
                ▼
       FastAPI Authorization
                │
                ▼
        Pydantic Validation
                │
                ▼
         Business Logic
                │
                ▼
        Supabase RLS Policies
                │
                ▼
       Protected PostgreSQL
```

### Security Controls

- JWT authentication
- Protected routes
- Authorization headers
- Supabase RLS
- Environment variables
- Secret key protection
- Input validation
- CORS configuration
- Audit logging
- User data isolation

---

# 15. Deployment Architecture

The production architecture is designed to separate frontend, backend, and database services.

```text
                         INTERNET
                            │
                            ▼
                   ┌─────────────────┐
                   │     USERS       │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ VERCEL / CDN    │
                   │                 │
                   │ Static Frontend │
                   └────────┬────────┘
                            │
                     HTTPS / REST API
                            │
                            ▼
                   ┌─────────────────┐
                   │ BACKEND HOSTING │
                   │                 │
                   │ FastAPI         │
                   │ Python          │
                   │ Uvicorn         │
                   └────────┬────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
       ┌─────────────────┐     ┌─────────────────┐
       │ AI/ML Services  │     │    SUPABASE     │
       │                 │     │                 │
       │ Forecasting     │     │ PostgreSQL      │
       │ Analytics       │     │ Authentication  │
       │ Predictions     │     │ Realtime        │
       └─────────────────┘     └─────────────────┘
```

---

# 16. Environment & Configuration

Sensitive configuration values are managed using environment variables.

```text
backend/
│
├── .env
│
├── config.py
├── database.py
└── main.py
```

Example:

```env
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE=your-service-role-key
```

### Important

`.env` must never be committed to GitHub.

---

# 17. Scalability Strategy

The architecture can be scaled in multiple stages.

### Stage 1 — MVP

```text
Single Frontend
      +
Single FastAPI Backend
      +
Supabase PostgreSQL
```

### Stage 2 — Growing Application

```text
Frontend
   │
Load Balancer
   │
┌──┴─────────┐
│            │
API Server  API Server
│            │
└─────┬──────┘
      │
 Supabase
```

### Stage 3 — Enterprise

```text
                    API Gateway
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Auth API   Inventory API  Forecast API
              │          │          │
              └──────────┼──────────┘
                         │
                    Data Layer
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        PostgreSQL    Cache       AI Services
```

Future scalability options include:

- Containerization with Docker
- Kubernetes
- Redis caching
- Background task processing
- Message queues
- Dedicated ML inference services
- CDN-based frontend delivery
- Horizontal API scaling

---

# 18. Project Data Flow

The complete platform data flow:

```text
                    USER
                     │
                     ▼
                 FRONTEND
                     │
                     ▼
                 FASTAPI
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   AUTHENTICATION  PRODUCTS     CSV DATA
        │            │            │
        │            │            ▼
        │            │       DATA PROCESSING
        │            │            │
        │            └────────────┤
        │                         ▼
        │                    PostgreSQL
        │                         │
        │                         ▼
        │                   Historical Data
        │                         │
        │                         ▼
        │                    AI/ML MODEL
        │                         │
        │                         ▼
        │                  Demand Forecast
        │                         │
        │                         ▼
        │                  Inventory Analysis
        │                         │
        │                 ┌───────┴────────┐
        │                 ▼                ▼
        │              Alerts           Orders
        │                 │                │
        └─────────────────┴────────────────┘
                          │
                          ▼
                     DASHBOARD
```

---

# 19. Technology-to-Feature Mapping

| Feature | Frontend | Backend | Database | AI/ML |
|---|---|---|---|---|
| Authentication | JavaScript | FastAPI + JWT | Users | — |
| Dashboard | HTML/CSS/JS | Dashboard API | PostgreSQL | Analytics |
| Inventory | HTML/CSS/JS | Products API | Products | — |
| Forecasting | Forecast UI | Forecast API | Sales + Forecasts | Demand Model |
| Alerts | Alert UI | Alerts API | Alerts | Risk Analysis |
| Reordering | Order UI | Orders API | Orders | Recommendations |
| CSV Import | Upload UI | Upload API | PostgreSQL | Data Processing |
| CSV Export | Download UI | Export API | PostgreSQL | — |
| Real-Time Updates | JavaScript | API / Supabase | Supabase Realtime | — |

---

# 20. Folder-Level Architecture

```text
HACKINMOTION-RICR-HIM-1105/
│
├── frontend/                     # Presentation Layer
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
├── backend/                      # Application Layer
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
├── database/                     # Data Layer
│   ├── 01_schema.sql
│   └── README.md
│
└── README.md
```

---

# 21. Development Status

SMART AI FORECASTING is currently in the **MVP stage**.

### Completed

- [x] Frontend foundation
- [x] Authentication flow
- [x] Dashboard
- [x] Inventory management
- [x] Forecasting module
- [x] Stock alerts
- [x] Order management
- [x] CSV import/export
- [x] FastAPI backend structure
- [x] Supabase database architecture
- [x] JWT authentication
- [x] RLS-based database security
- [x] API architecture

### In Progress

- [ ] Advanced AI/ML forecasting
- [ ] Forecast accuracy optimization
- [ ] Advanced analytics
- [ ] Automated recommendations
- [ ] Production optimization
- [ ] Additional security hardening
- [ ] Advanced real-time functionality
- [ ] Final production release

---

# 22. Future Architecture

The long-term architecture is planned to evolve toward an intelligent, scalable retail platform.

```text
                         SMART AI FORECASTING
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
   AI Forecasting          Inventory Intelligence      Real-Time Data
        │                         │                         │
        ▼                         ▼                         ▼
 Advanced ML Models       Smart Recommendations       Live Monitoring
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                                  ▼
                         Multi-Store Platform
                                  │
                                  ▼
                         Enterprise Ecosystem
```

Potential future additions:

- Advanced time-series forecasting
- Automated reorder optimization
- Multi-store inventory
- Multi-tenant architecture
- Mobile application
- POS integration
- ERP integration
- Supplier API integration
- Email/WhatsApp/SMS notifications
- Advanced anomaly detection
- Business intelligence dashboards

---

# 👥 Team

## HACKINMOTION-RICR-HIM-1105

| Member | Responsibility |
|---|---|
| **Akash Choudhary** | Team Leader — Full Stack Development |
| **Alok Pratap Gupta** | Backend & Database |
| **Ali Ahmad Sadat** | Frontend Development |
| **Lokesh Yadav** | System Architecture Designing |

---

# 📌 Architecture Summary

SMART AI FORECASTING uses a modular architecture where:

```text
Frontend
   ↓
FastAPI Backend
   ↓
Authentication + Business Logic
   ↓
AI/ML + Database
   ↓
Forecasts + Alerts + Recommendations
   ↓
Inventory Decisions
```

The architecture is designed to provide:

- **Modularity**
- **Security**
- **Scalability**
- **Maintainability**
- **AI-driven decision making**
- **Real-time data capability**
- **Cloud deployment readiness**

---

# 🏆 Project

**SMART AI FORECASTING**

### Developed by

**HACKINMOTION-RICR-HIM-1105**

> *Turning retail data into intelligent inventory decisions.*