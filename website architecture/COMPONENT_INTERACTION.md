# Component Interaction & Module Map

## SMART AI FORECASTING

**Team:** HACKINMOTION-RICR-HIM-1105  
**Architecture Owner:** Lokesh Yadav

---

## 1. Purpose

This document defines how the major components of SMART AI FORECASTING interact with each other.

---

## 2. Major Components

```text
Frontend
Backend
Authentication
Database
AI/ML
Alerts
Orders
CSV Processing
Realtime
```

---

## 3. Component Map

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │    FRONTEND     │
                  │ HTML/CSS/JS     │
                  └────────┬────────┘
                           │
                    REST / JSON
                           │
                           ▼
                  ┌─────────────────┐
                  │     FASTAPI     │
                  │   API LAYER     │
                  └───┬─────┬───────┘
                      │     │
             ┌────────┘     └─────────┐
             ▼                        ▼
       ┌─────────────┐         ┌─────────────┐
       │  SUPABASE   │         │  AI / ML     │
       │ PostgreSQL  │         │  GEMINI      │
       └──────┬──────┘         └──────┬──────┘
              │                       │
              └───────────┬───────────┘
                          ▼
                    Application
                     Intelligence
                          │
                  ┌───────┼────────┐
                  ▼       ▼        ▼
              Dashboard Alerts   Orders
```

---

## 4. Frontend Components

### Landing

```text
index.html
```

Provides the public introduction and navigation.

### Authentication

```text
auth.html
```

Handles login/signup UI.

### Dashboard

```text
dashboard.html
```

Displays high-level inventory and forecasting information.

### Inventory

```text
inventory.html
```

Handles product management.

### Forecast

```text
forecast.html
```

Displays demand predictions and forecasting information.

### Alerts

```text
alerts.html
```

Displays inventory warnings and critical conditions.

---

## 5. Backend Modules

```text
app/routes/
├── auth.py
├── products.py
├── dashboard.py
├── forecasts.py
├── alerts.py
├── orders.py
└── uploads.py
```

Each route module has a specific domain responsibility.

---

## 6. Module Interaction

### Authentication

```text
auth.html
   ↓
auth.py
   ↓
Supabase Auth
```

### Products

```text
inventory.html
   ↓
products.py
   ↓
Supabase products table
```

### Forecasts

```text
forecast.html
   ↓
forecasts.py
   ↓
AI/ML
   ↓
forecasts table
```

### Alerts

```text
alerts.html
   ↓
alerts.py
   ↓
Inventory / Forecast Logic
   ↓
alerts table
```

### Orders

```text
Inventory Risk
   ↓
orders.py
   ↓
orders table
```

### CSV

```text
CSV Upload
   ↓
uploads.py
   ↓
Validation / Parsing
   ↓
Supabase
```

---

## 7. Dependency Direction

The architecture follows a controlled dependency direction:

```text
UI
 ↓
API
 ↓
Business Logic
 ↓
External Services / Database
```

Lower-level services should not directly control frontend UI behavior.

---

## 8. Failure Boundaries

The system should handle failures independently.

```text
Frontend Failure
    ≠
Database Failure
    ≠
Gemini Failure
    ≠
Authentication Failure
```

For example, if the AI service becomes temporarily unavailable, inventory CRUD operations should remain independently manageable wherever possible.

---

## 9. Extensibility

New modules can be added without restructuring the entire platform.

Potential modules:

```text
Supplier Management
Notifications
Multi-Store
Reports
Analytics
User Roles
Mobile API
```

---

## 10. Architecture Status

**Current:** Core component interaction designed for MVP.

**Future:** Additional modules and integrations can be introduced through dedicated services and API routes.
