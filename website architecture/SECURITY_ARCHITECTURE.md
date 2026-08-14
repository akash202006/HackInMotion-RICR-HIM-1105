# Security Architecture

## SMART AI FORECASTING

**Team:** HACKINMOTION-RICR-HIM-1105  
**Architecture Owner:** Lokesh Yadav

---

## 1. Security Objective

The security architecture is designed to protect:

- User accounts
- Inventory information
- Historical sales data
- Forecast data
- Orders
- API credentials
- Database records

---

## 2. Security Layers

```text
User
 ↓
Frontend
 ↓
Authentication
 ↓
API Authorization
 ↓
Backend Validation
 ↓
Database RLS
 ↓
PostgreSQL Data
```

Each layer provides a separate security boundary.

---

## 3. Authentication

Supabase Auth is used for user authentication.

The architecture supports:

- User signup
- User login
- Session management
- Logout
- Protected application access

---

## 4. Authorization

Protected application requests should contain a valid authentication context.

```text
Request
  ↓
Authentication Check
  ↓
Authorization
  ↓
Resource Access
```

Invalid or unauthenticated requests should be rejected.

---

## 5. Row Level Security

Supabase PostgreSQL Row Level Security is used to restrict data access.

Concept:

```text
User A → User A data
User B → User B data
```

This prevents users from directly accessing another user's private inventory information when the corresponding policies are correctly configured.

---

## 6. Secret Management

Sensitive credentials must remain outside the source code.

Examples:

```text
SUPABASE_URL
SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE
GEMINI_API_KEY
```

Secrets should be stored in environment variables.

```text
.env
  ↓
.gitignore
  ↓
Never commit secrets to repository
```

---

## 7. Service Role Key

The Supabase Service Role Key has elevated privileges and must never be exposed to frontend JavaScript.

It should only be available to trusted server-side processes when required.

---

## 8. Gemini API Security

The Gemini API key must not be placed directly in public frontend files.

Recommended architecture:

```text
Frontend
   ↓
FastAPI Backend
   ↓
Gemini API
```

This keeps sensitive AI credentials on the server side.

---

## 9. Input Validation

Backend request data should be validated before processing.

Validation should cover:

- Required fields
- Data types
- Numeric ranges
- IDs
- CSV fields
- API request structure

Pydantic schemas are used for structured request validation.

---

## 10. CORS

CORS should be configured to allow only trusted frontend origins in production.

Development:

```text
Frontend → localhost:8000
Backend  → localhost:8001
```

Production should use the actual deployed frontend domain.

---

## 11. Transport Security

Production deployment should use HTTPS.

```text
Browser
   │
 HTTPS
   ▼
Frontend / API
```

Sensitive data should never be transmitted through unencrypted production connections.

---

## 12. Security Roadmap

Future security improvements:

- Rate limiting
- Security headers
- Better audit logging
- Automated dependency scanning
- Secret rotation
- API abuse protection
- Centralized monitoring
- Stronger role-based access control

---

## 13. Security Status

**Current:** MVP-level security architecture implemented.

**Future:** Production security hardening is planned before a full production release.
