# Scalability Architecture

## SMART AI FORECASTING

**Team:** HACKINMOTION-RICR-HIM-1105  
**Architecture Owner:** Lokesh Yadav

---

## 1. Objective

The scalability architecture defines how SMART AI FORECASTING can evolve from a small MVP into a production-ready platform supporting larger datasets, more users, and multiple stores.

---

## 2. Current MVP Architecture

```text
Browser
   ↓
Static Frontend
   ↓
FastAPI
   ↓
Supabase PostgreSQL
   +
AI Services
```

This architecture is intentionally lightweight for MVP development.

---

## 3. Scalability Challenges

As adoption grows, the system may need to handle:

- More concurrent users
- Larger sales datasets
- More products
- More stores
- More forecasting requests
- More CSV uploads
- More realtime events

---

## 4. Horizontal Backend Scaling

Multiple backend instances can be introduced.

```text
                 Load Balancer
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       FastAPI     FastAPI     FastAPI
       Instance    Instance    Instance
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Supabase DB
```

---

## 5. Caching Layer

Redis can be introduced for frequently requested information.

Potential cached data:

- Dashboard KPIs
- Forecast summaries
- Product analytics
- Frequently accessed configuration

```text
Frontend
   ↓
FastAPI
   ↓
Redis Cache
   ↓
Database
```

---

## 6. Background Processing

Long-running jobs should not block normal API requests.

Potential background tasks:

- Large CSV processing
- Model training
- Forecast generation
- Batch analytics
- Scheduled alerts

Future architecture:

```text
API
 ↓
Job Queue
 ↓
Background Worker
 ↓
AI / Database
```

Potential technologies:

- Celery
- Redis
- Task queues

---

## 7. AI/ML Scaling

Forecasting can eventually be moved into a dedicated service.

```text
FastAPI
   ↓
ML Service
   ↓
Forecast Model
   ↓
Prediction
   ↓
FastAPI
```

This allows AI models to scale independently.

---

## 8. Multi-Store Expansion

Future architecture can support multiple stores.

```text
Organization
     │
     ├── Store A
     │     ├── Products
     │     └── Sales
     │
     ├── Store B
     │     ├── Products
     │     └── Sales
     │
     └── Store C
           ├── Products
           └── Sales
```

A tenant/store identifier can be introduced into relevant database records.

---

## 9. Storage Scaling

Large datasets may require:

- Database indexing
- Pagination
- Archiving
- Data partitioning
- Object storage for large files

CSV uploads should be processed in controlled batches as data volume increases.

---

## 10. Observability

Production architecture should include:

```text
Application
   ↓
Logs
Metrics
Traces
Alerts
```

Monitoring should help detect:

- API failures
- Slow requests
- Database errors
- AI service failures
- Authentication issues

---

## 11. Future Production Architecture

```text
                    USERS
                      │
                      ▼
                CDN / Frontend
                      │
                      ▼
                Load Balancer
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       API-1       API-2       API-3
          │           │           │
          └───────────┼───────────┘
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
         Redis              Job Queue
            │                   │
            │                   ▼
            │              AI Workers
            │                   │
            └─────────┬─────────┘
                      ▼
                Supabase DB
```

---

## 12. Scalability Principle

The MVP should remain simple while keeping boundaries clear enough to allow future services to be introduced without rewriting the entire application.

---

## 13. Status

**Current:** Lightweight MVP architecture.

**Future:** Horizontally scalable, multi-store, production-oriented architecture.
