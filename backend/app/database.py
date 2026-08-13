from supabase import create_client

from app.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_anon_key)
supabase_admin = create_client(settings.supabase_url, settings.supabase_service_role)


def get_supabase():
    return supabase


def get_supabase_admin():
    return supabase_admin
