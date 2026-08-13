create extension if not exists "pgcrypto";

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  name text not null,
  password_hash text,
  role text default 'store_manager',
  created_at timestamptz default now()
);

create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  name text not null,
  sku text not null,
  category text not null,
  stock integer not null default 0,
  price numeric(10,2) not null default 0,
  supplier text,
  lead_time integer default 3,
  min_stock integer default 0,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists public.orders (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  product_id uuid references public.products(id) on delete cascade,
  quantity integer not null,
  supplier text,
  expected_delivery timestamptz,
  status text default 'pending',
  created_at timestamptz default now()
);

create table if not exists public.alerts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  product_id uuid references public.products(id) on delete cascade,
  alert_type text not null,
  message text not null,
  status text default 'active',
  created_at timestamptz default now(),
  resolved_at timestamptz
);

create table if not exists public.forecasts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  product_id uuid references public.products(id) on delete cascade,
  predicted_demand integer not null,
  confidence numeric(5,2) default 0,
  forecast_date timestamptz,
  created_at timestamptz default now()
);
