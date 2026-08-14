# Data Flow Architecture

## SMART AI FORECASTING

**Team:** HACKINMOTION-RICR-HIM-1105  
**Architecture Owner:** Lokesh Yadav

---

## 1. Purpose

This document describes how information moves through SMART AI FORECASTING from user interaction to storage, AI processing, alerts, and inventory decisions.

---

## 2. High-Level Data Flow

```text
                USER
                  │
                  ▼
             WEB FRONTEND
                  │
             REST / JSON
                  │
                  ▼
            FASTAPI BACKEND
             │          │
             │          │
             ▼          ▼
        SUPABASE      AI LAYER
        DATABASE      / GEMINI
             │          │
             └────┬─────┘
                  ▼
             APPLICATION
                OUTPUT
                  │
          ┌───────┼────────┐
          ▼       ▼        ▼
       Dashboard Alerts   Orders
```

---

## 3. Authentication Data Flow

```text
User
 ↓
Auth Form
 ↓
Supabase Auth
 ↓
Session / Token
 ↓
Frontend Session State
 ↓
Protected Application
```

Unauthenticated users are redirected to the authentication page.

---

## 4. Product Data Flow

```text
Product Form
 ↓
Frontend Validation
 ↓
API / Database Request
 ↓
Supabase PostgreSQL
 ↓
Product Record
 ↓
Dashboard / Inventory UI
```

---

## 5. Sales CSV Flow

```text
CSV File
 ↓
Upload Interface
 ↓
Backend Upload Handler
 ↓
CSV Parsing
 ↓
Validation
 ↓
Sales Data
 ↓
Supabase PostgreSQL
 ↓
Forecasting Input
```

---

## 6. Forecasting Data Flow

```text
Historical Sales
       ↓
Data Cleaning
       ↓
Feature Preparation
       ↓
AI / Forecasting Engine
       ↓
Predicted Demand
       ↓
Confidence / Insight
       ↓
Forecast Storage
       ↓
Frontend Visualization
```

---

## 7. Alert Flow

```text
Current Stock
      +
Minimum Stock
      +
Forecasted Demand
      ↓
Risk Evaluation
      ↓
Inventory Risk
      ↓
Alert Generation
      ↓
Alerts Table
      ↓
Dashboard / Alerts Page
```

---

## 8. Reorder Flow

```text
Forecast
   ↓
Inventory Risk
   ↓
Reorder Requirement
   ↓
Recommended / Requested Quantity
   ↓
Order Record
   ↓
Order Status
```

---

## 9. Real-Time Flow

Where Supabase Realtime is enabled:

```text
Database Change
      ↓
Supabase Realtime
      ↓
Frontend Subscription
      ↓
UI State Update
      ↓
Updated Dashboard
```

---

## 10. Data Ownership

The system follows user-level data isolation.

```text
User A
 ├── Products
 ├── Sales
 ├── Forecasts
 ├── Alerts
 └── Orders

User B
 ├── Products
 ├── Sales
 ├── Forecasts
 ├── Alerts
 └── Orders
```

Row Level Security is used to enforce appropriate access.

---

## 11. Architecture Principle

Data should flow through controlled application boundaries rather than exposing database credentials or sensitive service keys to the browser.
