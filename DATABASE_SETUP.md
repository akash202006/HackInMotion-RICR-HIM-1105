# Database Deployment Checklist

## ✅ Quick Supabase Setup

### Step 1: Create Supabase Project
- [ ] Go to https://supabase.com
- [ ] Sign up / Log in
- [ ] Click "New Project"
- [ ] Select Organization
- [ ] Project Name: `SMART AI FORECASTING`
- [ ] Password: (save safely)
- [ ] Region: Choose closest to your location
- [ ] Wait for project to initialize (2-3 minutes)

### Step 2: Get API Credentials
- [ ] Go to **Project Settings** (gear icon)
- [ ] Click **API** tab
- [ ] Copy these and save to `backend/.env`:
  - `Project URL` → `SUPABASE_URL=`
  - `Anon Key` → `SUPABASE_ANON_KEY=`
  - `Service Role Key` → `SUPABASE_SERVICE_ROLE=`

### Step 3: Create Database Tables
- [ ] In Supabase dashboard, go to **SQL Editor**
- [ ] Click **New Query**
- [ ] Open file: `database/01_schema.sql`
- [ ] Copy entire content
- [ ] Paste into query editor
- [ ] Click **Run** (Ctrl+Enter)
- [ ] Wait for success message
- [ ] Verify tables in **Table Editor** on left sidebar

### Step 4: Verify Tables Created
- [ ] Click **Table Editor**
- [ ] Verify these tables exist:
  - [ ] `users`
  - [ ] `products`
  - [ ] `orders`
  - [ ] `alerts`
  - [ ] `forecasts`
  - [ ] `sales_data`
  - [ ] `audit_logs`

### Step 5: Enable Real-time (Optional)
- [ ] Go to **Database** → **Replication**
- [ ] Enable for tables:
  - [ ] `products`
  - [ ] `alerts`
  - [ ] `orders`
  - [ ] `forecasts`

### Step 6: Test Connection
- [ ] Go to backend folder
- [ ] Run: `python -m uvicorn main:app --reload --port 8001`
- [ ] Visit: `http://localhost:8001/health`
- [ ] Should see:
  ```json
  {
    "status": "ok",
    "service": "smart-ai-forecasting-api",
    "project": "HACKINMOTION-RICR-HIM-1105"
  }
  ```

### Step 7: Test API Endpoints
- [ ] Visit: `http://localhost:8001/docs`
- [ ] Try **POST /api/auth/signup**:
  ```json
  {
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User",
    "role": "store_manager"
  }
  ```
- [ ] Should get back JWT token and user data

### Step 8: Test Frontend Connection
- [ ] Start frontend: `python -m http.server 8000` (from frontend/ folder)
- [ ] Visit: `http://localhost:8000/auth.html`
- [ ] Try signing up with test account
- [ ] Should redirect to dashboard
- [ ] Check browser console for any errors

---

## 🔍 Database Verification Commands

### Check Tables Exist
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' ORDER BY table_name;
```

### Check Indexes
```sql
SELECT indexname FROM pg_indexes 
WHERE schemaname = 'public' ORDER BY indexname;
```

### Check RLS Policies
```sql
SELECT schemaname, tablename, policyname, permissive, roles, qual, with_check 
FROM pg_policies 
WHERE schemaname = 'public' ORDER BY tablename, policyname;
```

### Check Row Counts
```sql
SELECT 
  (SELECT COUNT(*) FROM public.users) as users,
  (SELECT COUNT(*) FROM public.products) as products,
  (SELECT COUNT(*) FROM public.orders) as orders,
  (SELECT COUNT(*) FROM public.alerts) as alerts,
  (SELECT COUNT(*) FROM public.forecasts) as forecasts,
  (SELECT COUNT(*) FROM public.sales_data) as sales_data,
  (SELECT COUNT(*) FROM public.audit_logs) as audit_logs;
```

---

## 🆘 Common Issues

### "Connection refused" from backend
- **Issue**: Backend can't reach Supabase
- **Fix**: 
  1. Verify SUPABASE_URL in `.env` is correct
  2. Check internet connection
  3. Verify Supabase project is active (check dashboard)

### "Relation 'public.users' does not exist"
- **Issue**: Tables weren't created
- **Fix**: Re-run `database/01_schema.sql` in SQL Editor

### "Permission denied" for insert/update
- **Issue**: RLS policies are too restrictive
- **Fix**: 
  1. Make sure using Service Role key for backend
  2. Check RLS policies allow Service Role

### Auth fails but no error message
- **Issue**: Usually password hash mismatch
- **Fix**:
  1. Check bcrypt is installed: `pip show bcrypt`
  2. Check password is long enough (6+ chars)

---

## 📊 Database Backup

### Manual Backup
- [ ] Supabase Dashboard → **Database** → **Backups**
- [ ] Click **Create Backup**
- [ ] Wait for completion
- [ ] Download backup file

### Restore Backup
- [ ] **Database** → **Backups**
- [ ] Click **Restore** on backup
- [ ] Confirm (this will replace current data!)

---

## 🧹 Clean Up (Reset Database)

**WARNING: This deletes all data!**

```sql
-- Drop all tables
DROP TABLE IF EXISTS public.audit_logs CASCADE;
DROP TABLE IF EXISTS public.sales_data CASCADE;
DROP TABLE IF EXISTS public.forecasts CASCADE;
DROP TABLE IF EXISTS public.alerts CASCADE;
DROP TABLE IF EXISTS public.orders CASCADE;
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;

-- Drop function
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Re-run 01_schema.sql to recreate everything fresh
```

---

**Last Updated**: 2026-08-13
**Status**: ✅ Ready for Production
