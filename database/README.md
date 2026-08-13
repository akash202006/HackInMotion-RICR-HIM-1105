# Database Setup Guide

## Supabase Configuration

### 1. Create Supabase Project
- Go to https://supabase.com
- Create new project
- Copy the following from project settings:
  - Project URL
  - Anon Key
  - Service Role Key

### 2. Run Schema Setup
1. Go to Supabase Dashboard → SQL Editor
2. Create new query
3. Copy entire content from `01_schema.sql`
4. Execute query
5. Verify all tables are created

### 3. Enable Real-time (Optional)
- Go to Database → Replication
- Enable real-time for tables:
  - products
  - alerts
  - orders
  - forecasts

### 4. Set up Authentication (Optional)
- Go to Authentication → Providers
- Enable Email/Password auth
- Configure email templates

### 5. Backup and Restore
```bash
# Backup (from Supabase Dashboard)
- Database → Backups → Download backup

# Restore
- Database → Backups → Restore from backup
```

## Tables Overview

| Table | Purpose | Records |
|-------|---------|---------|
| `users` | Store managers | One per user |
| `products` | Inventory items | Variable per user |
| `orders` | Reorder requests | Variable |
| `alerts` | Stock alerts | Variable |
| `forecasts` | AI predictions | Variable |
| `sales_data` | Historical sales | Bulk import |
| `audit_logs` | Activity logs | System generated |

## Environment Variables

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE=your-service-role-key
```

## Real-time Subscriptions

```python
# Listen to product changes
supabase.table('products').on('*', callback).subscribe()

# Listen to alerts
supabase.table('alerts').on('INSERT', handle_new_alert).subscribe()
```

## Performance Tips

1. Use indexes for frequently queried columns
2. Enable caching for dashboard data
3. Use batch operations for bulk imports
4. Monitor query performance in Dashboard

## Disaster Recovery

- Enable automatic backups
- Test restore procedures
- Keep SQL schema files versioned
- Document all changes to schema
