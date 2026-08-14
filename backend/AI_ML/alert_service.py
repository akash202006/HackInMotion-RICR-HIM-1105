"""
Automated Alert Generation Service
Automatically creates and manages alerts based on inventory analysis
"""

from app.database import get_supabase_admin
from typing import List, Dict, Any
from datetime import datetime
import uuid


class AlertService:
    """Service for managing inventory alerts"""

    @staticmethod
    def _priority_from_severity(value: str) -> str:
        severity = (value or "MEDIUM").upper()
        if severity in {"CRITICAL", "HIGH"}:
            return "high" if severity == "HIGH" else "critical"
        return "medium"

    @staticmethod
    async def create_alerts_from_analysis(user_id: str, critical_alerts: List[Dict[str, Any]], 
                                         low_stock_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Automatically create alerts in the database from AI analysis.

        The database schema uses alert_type/status/priority, not the legacy
        type/severity/is_resolved fields from older code paths.
        """

        supabase = get_supabase_admin()
        created_alerts = []

        def _insert_if_missing(payload: Dict[str, Any], dedupe_key: str) -> None:
            product_id = payload.get("product_id")
            if not product_id:
                return

            try:
                existing = supabase.table("alerts").select("id").eq(
                    "user_id", user_id
                ).eq("product_id", product_id).eq(
                    "alert_type", payload["alert_type"]
                ).eq("status", "active").execute()
                if existing.data:
                    return
            except Exception:
                pass

            try:
                response = supabase.table("alerts").insert([payload]).execute()
                if response.data:
                    created_alerts.append(response.data[0])
            except Exception as e:
                print(f"Error creating alert {dedupe_key}: {e}")

        # Create alerts for critical issues
        for alert in critical_alerts:
            product_id = alert.get("product_id")
            if not product_id:
                continue

            alert_data = {
                "user_id": user_id,
                "product_id": str(product_id),
                "alert_type": str(alert.get("type", "LOW_STOCK")).lower(),
                "message": alert.get("message", "Inventory issue detected"),
                "status": "active",
                "priority": AlertService._priority_from_severity(alert.get("severity", "HIGH")),
                "created_at": datetime.utcnow().isoformat(),
            }
            _insert_if_missing(alert_data, f"critical:{product_id}")

        # Create alerts for low stock items
        for item in low_stock_items:
            product_id = item.get("product_id")
            if not product_id:
                continue

            current_stock = item.get("current_stock", 0)
            minimum_stock = item.get("minimum_stock", 0)
            recommended_order = item.get("recommended_order", 0)
            alert_data = {
                "user_id": user_id,
                "product_id": str(product_id),
                "alert_type": "low_stock",
                "message": f"Low Stock: {item.get('product_name', 'Unknown')} - Current: {current_stock}, Minimum: {minimum_stock}",
                "status": "active",
                "priority": "critical" if item.get("urgency") == "CRITICAL" else "high",
                "created_at": datetime.utcnow().isoformat(),
            }
            _insert_if_missing(alert_data, f"low_stock:{product_id}")

        return created_alerts

    @staticmethod
    async def get_active_alerts(user_id: str) -> List[Dict[str, Any]]:
        """Get all active alerts for a user"""

        supabase = get_supabase_admin()

        try:
            response = supabase.table("alerts").select("*").eq(
                "user_id", user_id
            ).eq("status", "active").order("created_at", desc=True).execute()

            return response.data or []
        except Exception as e:
            print(f"Error fetching alerts: {e}")
            return []

    @staticmethod
    async def mark_alert_resolved(alert_id: str, user_id: str) -> bool:
        """Mark an alert as resolved"""

        supabase = get_supabase_admin()

        try:
            response = supabase.table("alerts").update({
                "status": "resolved",
                "resolved_at": datetime.utcnow().isoformat()
            }).eq("id", alert_id).eq("user_id", user_id).execute()

            return len(response.data) > 0
        except Exception as e:
            print(f"Error resolving alert: {e}")
            return False
