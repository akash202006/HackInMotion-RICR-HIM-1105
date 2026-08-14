# API_DOCUMENTATION.md

# SMART AI FORECASTING — API & External Services Documentation

**Team:** HACKINMOTION-RICR-HIM-1105  
**Project:** SMART AI FORECASTING  
**Status:** MVP Completed — Further Development in Progress

---

## 1. Overview

SMART AI FORECASTING uses external APIs/services for two major purposes:

1. **Supabase APIs** — Authentication and database operations
2. **Google Gemini API** — AI-powered forecasting, analysis, and intelligent responses

The application uses Supabase Auth for user authentication and Supabase PostgreSQL for application data storage.

---

## 2. API Services Used

| Service | Purpose | Main Usage |
|---|---|---|
| **Supabase** | Authentication + Database | Users, products, sales, forecasts, alerts, orders |
| **Google Gemini** | AI Intelligence | Demand analysis, forecasting assistance, AI-generated insights |

---

# 3. Supabase API

Supabase provides the backend services used by SMART AI FORECASTING for authentication and PostgreSQL database access.

### Supabase services used

- Supabase Authentication
- Supabase PostgreSQL Database
- Supabase REST/Data API
- Supabase Realtime, where enabled
- Supabase Row Level Security (RLS)

---

# 4. Supabase Authentication API

Authentication is handled using **Supabase Auth**.

### Authentication operations

```text
Sign Up
Sign In
Session Management
Current User
Sign Out
```

### Authentication flow

```text
User
  |
  v
Login / Signup Form
  |
  v
Supabase Auth
  |
  +---- Invalid ---> Authentication Error
  |
  +---- Valid -----> Session / Access Token
                         |
                         v
                    Application
```

## 4.1 Sign Up

Creates a new user account.

```javascript
const { data, error } = await supabase.auth.signUp({
    email,
    password
});
```

**Input**

```text
email
password
```

---

## 4.2 Sign In

Authenticates an existing user.

```javascript
const { data, error } =
    await supabase.auth.signInWithPassword({
        email,
        password
    });
```

**Input**

```text
email
password
```

**Output**

```text
Authenticated User
Session
Access Token
```

---

## 4.3 Current Session

Retrieves the currently authenticated session.

```javascript
const {
    data: { session }
} = await supabase.auth.getSession();
```

---

## 4.4 Current User

Retrieves the currently authenticated user.

```javascript
const {
    data: { user }
} = await supabase.auth.getUser();
```

---

## 4.5 Sign Out

Logs the user out.

```javascript
await supabase.auth.signOut();
```

After logout, the application returns the user to the authentication/landing page.

---

# 5. Supabase Database API

The application database is PostgreSQL and is accessed through the Supabase client/Data API.

### Main tables

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

# 6. Database CRUD Operations

The application uses standard CRUD operations:

```text
CREATE  → INSERT
READ    → SELECT
UPDATE  → UPDATE
DELETE  → DELETE
```

---

## 6.1 Products API

### Read Products

```javascript
const { data, error } = await supabase
    .from("products")
    .select("*");
```

### Create Product

```javascript
const { data, error } = await supabase
    .from("products")
    .insert({
        name: "Pepsi 750ml",
        sku: "SKU-123",
        category: "Beverages",
        stock: 100,
        price: 45,
        supplier: "XYZ Dist.",
        lead_time: 3,
        min_stock: 20
    });
```

### Update Product

```javascript
const { data, error } = await supabase
    .from("products")
    .update({
        stock: 85
    })
    .eq("id", productId);
```

### Delete Product

```javascript
const { data, error } = await supabase
    .from("products")
    .delete()
    .eq("id", productId);
```

---

# 7. Sales Data API

Historical sales data is stored in the `sales_data` table.

### Read Sales Data

```javascript
const { data, error } = await supabase
    .from("sales_data")
    .select("*");
```

### Typical fields

```text
product_id
quantity_sold
revenue
sale_date
```

Sales data is used as input for demand forecasting and analytics.

---

# 8. Forecast Data API

Forecast results can be stored in the `forecasts` table.

### Create Forecast

```javascript
const { data, error } = await supabase
    .from("forecasts")
    .insert({
        product_id: productId,
        predicted_demand: 150,
        confidence_score: 92
    });
```

### Forecast information

```text
product_id
predicted_demand
confidence_score
forecast_date
created_at
```

---

# 9. Alerts API

Inventory alerts are stored in the `alerts` table.

### Create Alert

```javascript
const { data, error } = await supabase
    .from("alerts")
    .insert({
        product_id: productId,
        alert_type: "LOW_STOCK",
        message: "Stock is below minimum level",
        priority: "HIGH"
    });
```

### Resolve Alert

```javascript
const { data, error } = await supabase
    .from("alerts")
    .update({
        resolved: true
    })
    .eq("id", alertId);
```

---

# 10. Orders API

Reorder requests are stored in the `orders` table.

### Create Order

```javascript
const { data, error } = await supabase
    .from("orders")
    .insert({
        product_id: productId,
        quantity: 100,
        status: "Pending"
    });
```

### Update Order Status

```javascript
const { data, error } = await supabase
    .from("orders")
    .update({
        status: "Ordered"
    })
    .eq("id", orderId);
```

---

# 11. Supabase Realtime

Where enabled, Supabase Realtime can be used to receive database changes without manually refreshing the page.

### Possible use cases

```text
Inventory Updates
Alert Creation
Order Status Changes
Forecast Updates
```

### Example

```javascript
const channel = supabase
    .channel("inventory-changes")
    .on(
        "postgres_changes",
        {
            event: "*",
            schema: "public",
            table: "products"
        },
        (payload) => {
            console.log("Inventory updated:", payload);
        }
    )
    .subscribe();
```

### Realtime flow

```text
Supabase PostgreSQL
        |
        v
Database Change
        |
        v
Supabase Realtime
        |
        v
Frontend Subscription
        |
        v
UI Update
```

---

# 12. Row Level Security (RLS)

Supabase Row Level Security is used to protect user-specific application data.

The intended access model is:

```text
User A
  |
  +--> User A Products
  +--> User A Sales
  +--> User A Forecasts
  +--> User A Alerts
  +--> User A Orders

User B
  |
  +--> User B Products
  +--> User B Sales
  +--> User B Forecasts
  +--> User B Alerts
  +--> User B Orders
```

A user should not be able to access another user's private inventory records.

RLS policies should be based on the authenticated Supabase user identity.

---

# 13. Google Gemini API

Google Gemini is used as the AI layer of SMART AI FORECASTING.

It can process relevant sales/inventory context and generate intelligent analysis, forecasting assistance, and business insights.

### AI flow

```text
Historical Sales Data
        |
        v
Data Preparation
        |
        v
Gemini API
        |
        v
AI Analysis
        |
        v
Demand / Inventory Insight
        |
        v
Application UI
```

---

# 14. Gemini API Key

The Gemini API key must be stored securely as an environment variable.

Example:

```env
GEMINI_API_KEY=your-gemini-api-key
```

### Security rules

- Never hard-code the Gemini API key in frontend source code.
- Never commit the API key to GitHub.
- Keep secret values inside environment variables.
- Rotate the key if it is accidentally exposed.

---

# 15. Gemini Request

The application can send structured inventory and sales context to Gemini for analysis.

### Example request context

```text
System:
You are an inventory forecasting assistant.

Input:
Product: Pepsi 750ml
Historical Sales:
100, 115, 108, 130, 142
Current Stock: 90
Minimum Stock: 30
Lead Time: 3 days

Task:
Analyze the demand trend and provide:
1. Expected demand
2. Inventory risk
3. Reorder recommendation
4. Short explanation
```

The application should process the model response before presenting it as a final business recommendation.

---

# 16. Gemini Response Handling

AI-generated output should be validated before it is stored or used for business decisions.

### Recommended flow

```text
Gemini Response
      |
      v
Validate Response
      |
      v
Extract Relevant Values
      |
      v
Apply Business Rules
      |
      v
Store / Display Result
```

### Example output

```text
Predicted Demand: 150 units
Inventory Risk: HIGH
Recommended Action: Reorder
Reason: Forecasted demand is higher than current available stock.
```

---

# 17. AI + Database Integration

Gemini and Supabase work together in the forecasting pipeline.

```text
                    SUPABASE
                       |
                       v
                Historical Sales
                       |
                       v
                 Data Preparation
                       |
                       v
                  GEMINI API
                       |
                       v
                AI Analysis
                       |
                       v
              Forecast / Insight
                       |
                       v
                    SUPABASE
                       |
                       v
                  Frontend
```

### Responsibility separation

| Service | Responsibility |
|---|---|
| **Supabase Auth** | User authentication and sessions |
| **Supabase PostgreSQL** | Application data storage |
| **Supabase RLS** | Data access control |
| **Supabase Realtime** | Live database updates, where enabled |
| **Gemini API** | AI analysis and forecasting assistance |
| **Frontend** | Visualization and user interaction |

---

# 18. API Security

## Supabase Security

Security mechanisms include:

- Supabase Auth
- Access tokens
- Row Level Security
- Database policies
- Environment variables

## Gemini Security

Security requirements include:

- API key stored in environment variables
- API key not exposed in frontend code
- API key not committed to GitHub
- API usage restrictions where possible
- AI output validation before critical actions

---

# 19. Environment Variables

Example environment configuration:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE=your-service-role-key
GEMINI_API_KEY=your-gemini-api-key
```

> **Important:** Never upload `.env` files containing secrets to GitHub.

Recommended `.gitignore` entries:

```gitignore
.env
.env.*
__pycache__/
*.pyc
```

### Important production note

`SUPABASE_SERVICE_ROLE` is a highly privileged secret and must only be used in a trusted server/backend environment. It must never be exposed to browser/client-side code.

---

# 20. API Error Handling

External API failures should be handled gracefully.

### Possible errors

```text
Authentication Failure
Database Connection Failure
Database Validation Error
RLS Permission Error
Gemini API Failure
Invalid Gemini Response
Rate Limit
Network Error
Timeout
```

### Recommended flow

```text
API Request
    |
    v
Try Request
    |
    +---- Success ----> Process Response
    |
    +---- Failure ----> Handle Error
                          |
                          v
                    User-Friendly Message
```

The application should avoid exposing raw database errors, API keys, tokens, or internal stack traces to end users.

---

# 21. API Usage Summary

| API / Service | Authentication | Database | AI |
|---|---:|---:|---:|
| Supabase Auth | ✅ | — | — |
| Supabase PostgreSQL | Via Supabase session/RLS | ✅ | — |
| Supabase Realtime | Via Supabase access control | ✅ | — |
| Google Gemini API | API Key | — | ✅ |

---

# 22. Complete Application Data Flow

```text
USER
 |
 v
Frontend
 |
 +----------------------+
 |                      |
 v                      v
SUPABASE AUTH        APPLICATION DATA
 |                      |
 v                      v
Session              Supabase DB
                         |
                         v
                  Historical Sales
                         |
                         v
                    Gemini API
                         |
                         v
                  AI Forecast/Insight
                         |
                         v
                 Inventory Analysis
                    /          \
                   v            v
                Alerts        Orders
                   \            /
                    v          v
                     Dashboard
```

---

# 23. CSV / Data Import Integration

SMART AI FORECASTING can process uploaded CSV data as part of the inventory/sales workflow.

### Intended flow

```text
CSV Upload
    |
    v
File Validation
    |
    v
Data Type Detection
    |
    +---- Products ----> Product Validation
    |
    +---- Sales -------> Sales Validation
    |
    v
AI/Data Processing
    |
    v
Valid Records
    |
    v
Supabase Database
```

### Data validation

The import process should validate:

- Required columns
- Product identifiers
- Quantity values
- Revenue values
- Dates
- Duplicate records
- Missing values
- Invalid numeric values

Only validated records should be inserted into the database.

---

# 24. Forecasting Pipeline

The forecasting system follows this general pipeline:

```text
Historical Sales
       |
       v
Data Cleaning
       |
       v
Feature / Context Preparation
       |
       v
AI Forecasting / Analysis
       |
       v
Predicted Demand
       |
       v
Inventory Risk Evaluation
       |
       +------------------+
       |                  |
       v                  v
   Low Risk           High Risk
       |                  |
       v                  v
   Monitor            Alert / Reorder
```

---

# 25. API Documentation Status

This document currently covers the external APIs/services used by the SMART AI FORECASTING MVP:

- Supabase Authentication
- Supabase PostgreSQL Database
- Supabase Realtime, where enabled
- Google Gemini API

As the project evolves, update this document whenever new external APIs, integrations, endpoints, or services are introduced.

---

# 26. Future Integrations

The following integrations may be considered in future versions:

- Supplier APIs
- POS systems
- ERP systems
- Payment services
- Email notification services
- SMS notification services
- WhatsApp notification services
- Advanced AI/ML services

These should only be introduced when required by the final product architecture.

---

# 27. Important Development Note

> **The current project is an MVP and is not the final production product.**

The API architecture is expected to evolve as development continues.

---

# 28. Team

| Member | Responsibility |
|---|---|
| **Akash Choudhary (Leader)** | Full Stack Development |
| **Alok Pratap Gupta** | Backend and Database |
| **Ali Ahmad Sadat** | Frontend Development |
| **Lokesh Yadav** | System Architecture Designing |

---

**SMART AI FORECASTING**  
*AI-powered inventory intelligence for smarter retail decisions.*

**MVP Completed ✅ | Further Development in Progress 🚧**
