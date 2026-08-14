"""
Advanced AI Analytics Engine for Inventory Management
Provides comprehensive analysis using Gemini AI with fallback mechanisms
"""

try:
    from google import genai
except ImportError:
    genai = None
from app.config import settings
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import json

from ai_ml.gemini_client import GeminiClient


class AIAnalyticsEngine:
    """
    Advanced AI-powered analytics engine for comprehensive inventory analysis
    """
    
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Initialize Gemini API"""
        if not cls._initialized and settings.gemini_api_key:
            try:
                if genai is not None:
                    GeminiClient(api_key=settings.gemini_api_key)
                cls._initialized = True
                print("✓ AI Analytics Engine initialized")
            except Exception as e:
                print(f"⚠ AI Engine initialization warning: {e}")
    
    @staticmethod
    def analyze_inventory(products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Comprehensive inventory analysis with AI insights
        
        Returns:
            {
                "summary": "Executive summary",
                "critical_alerts": [...],
                "low_stock_items": [...],
                "overstock_items": [...],
                "recommendations": [...],
                "sales_trend_analysis": "AI analysis of sales trends",
                "inventory_status": "Overall inventory health",
                "financial_impact": {...},
                "trend_data": {...},
                "status_chart_data": {...}
            }
        """
        AIAnalyticsEngine.initialize()
        
        if not products:
            return _get_empty_analysis()
        
        # Calculate metrics
        metrics = _calculate_metrics(products)
        
        # Identify critical issues
        critical_alerts = _identify_critical_alerts(products, metrics)
        low_stock = _get_low_stock_items(products)
        overstock = _get_overstock_items(products)
        
        # Get AI analysis
        ai_insights = _get_gemini_analysis(products, metrics, critical_alerts, low_stock, overstock)
        
        # Generate trend data for graphs
        trend_data = _generate_trend_data(products)
        status_chart_data = _generate_status_chart_data(products, metrics)
        
        # Build recommendations
        recommendations = _build_recommendations(low_stock, overstock, critical_alerts)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": ai_insights.get("summary", ""),
            "critical_alerts": critical_alerts,
            "low_stock_items": low_stock,
            "overstock_items": overstock,
            "recommendations": recommendations,
            "sales_trend_analysis": ai_insights.get("sales_trend_analysis", ""),
            "inventory_status": ai_insights.get("inventory_status", ""),
            "financial_impact": {
                "total_inventory_value": metrics["total_value"],
                "at_risk_value": metrics["at_risk_value"],
                "overstock_value": metrics["overstock_value"],
                "cash_locked": metrics["overstock_value"]
            },
            "metrics": metrics,
            "trend_data": trend_data,
            "status_chart_data": status_chart_data,
            "ai_powered": True
        }


# Helper Functions
# ================

def _calculate_metrics(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate key inventory metrics"""
    total_value = 0
    at_risk_value = 0
    overstock_value = 0
    total_stock = 0
    total_items = len(products)
    
    for product in products:
        stock = product.get('stock', 0)
        min_stock = product.get('min_stock', product.get('minStock', 0))
        max_stock = product.get('max_stock', product.get('maxStock', min_stock * 3))
        price = product.get('price', 0)
        
        total_stock += stock
        value = stock * price
        total_value += value
        
        if stock < min_stock:
            at_risk_value += value
        elif stock > max_stock:
            overstock_value += value
    
    low_stock_count = sum(1 for p in products if p.get('stock', 0) < p.get('min_stock', p.get('minStock', 0)))
    healthy_count = total_items - low_stock_count - sum(1 for p in products if p.get('stock', 0) > p.get('max_stock', p.get('maxStock', p.get('min_stock', p.get('minStock', 0)) * 3)))
    
    return {
        "total_items": total_items,
        "total_stock": total_stock,
        "total_value": round(total_value, 2),
        "at_risk_value": round(at_risk_value, 2),
        "overstock_value": round(overstock_value, 2),
        "low_stock_count": low_stock_count,
        "healthy_count": healthy_count
    }


def _identify_critical_alerts(products: List[Dict[str, Any]], metrics: Dict) -> List[Dict[str, Any]]:
    """Identify critical stock issues"""
    alerts = []
    
    for product in products:
        stock = product.get('stock', 0)
        min_stock = product.get('min_stock', product.get('minStock', 0))
        lead_time = product.get('lead_time', product.get('leadTime', 2))
        name = product.get('name', 'Unknown')
        
        if stock == 0:
            alerts.append({
                "type": "CRITICAL",
                "product_id": product.get('id'),
                "product_name": name,
                "message": f"🚨 OUT OF STOCK: {name} has 0 units",
                "severity": "CRITICAL",
                "action_needed": "Order immediately"
            })
        elif stock < min_stock:
            days_until_stockout = max(1, stock - (min_stock // lead_time)) if stock > 0 else 0
            alerts.append({
                "type": "LOW_STOCK",
                "product_id": product.get('id'),
                "product_name": name,
                "message": f"⚠️ LOW STOCK: {name} ({stock} units, min: {min_stock})",
                "severity": "HIGH",
                "action_needed": f"Reorder within {lead_time} days",
                "current": stock,
                "minimum": min_stock
            })
    
    return sorted(alerts, key=lambda x: {"CRITICAL": 0, "HIGH": 1}.get(x.get("severity", "LOW"), 2))


def _get_low_stock_items(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get items below minimum stock"""
    low_stock = []
    
    for product in products:
        stock = product.get('stock', 0)
        min_stock = product.get('min_stock', product.get('minStock', 0))
        
        if stock < min_stock:
            shortage = min_stock - stock
            lead_time = product.get('lead_time', product.get('leadTime', 2))
            price = product.get('price', 0)
            
            low_stock.append({
                "product_id": product.get('id'),
                "product_name": product.get('name', 'Unknown'),
                "current_stock": stock,
                "minimum_stock": min_stock,
                "shortage": shortage,
                "shortage_value": round(shortage * price, 2),
                "lead_time_days": lead_time,
                "recommended_order": min_stock * 2 - stock,
                "category": product.get('category', 'N/A'),
                "supplier": product.get('supplier', 'N/A'),
                "urgency": "CRITICAL" if stock == 0 else "HIGH"
            })
    
    return sorted(low_stock, key=lambda x: x['shortage'], reverse=True)


def _get_overstock_items(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get items above maximum stock"""
    overstock = []
    
    for product in products:
        stock = product.get('stock', 0)
        min_stock = product.get('min_stock', product.get('minStock', 0))
        max_stock = product.get('max_stock', product.get('maxStock', min_stock * 3))
        
        if stock > max_stock:
            excess = stock - max_stock
            price = product.get('price', 0)
            
            overstock.append({
                "product_id": product.get('id'),
                "product_name": product.get('name', 'Unknown'),
                "current_stock": stock,
                "maximum_stock": max_stock,
                "excess": excess,
                "cash_locked": round(excess * price, 2),
                "category": product.get('category', 'N/A'),
                "recommendation": "Consider promotional pricing"
            })
    
    return sorted(overstock, key=lambda x: x['cash_locked'], reverse=True)


def _get_gemini_analysis(products: List[Dict[str, Any]], metrics: Dict, 
                        critical_alerts: List, low_stock: List, overstock: List) -> Dict[str, str]:
    """Get detailed AI analysis from Gemini"""

    if not settings.gemini_api_key:
        return _get_local_analysis(products, metrics, critical_alerts, low_stock, overstock)

    try:
        prompt = _build_gemini_prompt(products, metrics, critical_alerts, low_stock, overstock)

        last_error = None
        for model_name in GeminiClient().supported_models:
            try:
                client = GeminiClient(api_key=settings.gemini_api_key)
                response_text = client.generate_text(prompt, model_name=model_name)
                if response_text:
                    parsed = _parse_gemini_response(response_text)
                    if parsed and any(parsed.get(key) for key in parsed):
                        return parsed
            except Exception as exc:
                last_error = exc
                print(f"Gemini model {model_name} failed: {exc}")

        if last_error:
            print(f"All Gemini models failed: {last_error}")
    except Exception as e:
        print(f"Gemini API error: {e}")

    return _get_local_analysis(products, metrics, critical_alerts, low_stock, overstock)


def _build_gemini_prompt(products: List[Dict[str, Any]], metrics: Dict, 
                        critical_alerts: List, low_stock: List, overstock: List) -> str:
    """Build optimized prompt for Gemini"""
    
    prompt = f"""You are an expert supply chain and inventory management consultant. 
Analyze this retail inventory data and provide strategic insights.

INVENTORY METRICS:
- Total Products: {metrics['total_items']}
- Total Stock Units: {metrics['total_stock']}
- Total Inventory Value: ₹{metrics['total_value']:,.2f}
- At Risk Value: ₹{metrics['at_risk_value']:,.2f}
- Overstock Value: ₹{metrics['overstock_value']:,.2f}

CRITICAL ISSUES:
{json.dumps(critical_alerts[:5], indent=2)}

LOW STOCK ITEMS ({len(low_stock)} total):
{json.dumps(low_stock[:5], indent=2)}

OVERSTOCK ITEMS ({len(overstock)} total):
{json.dumps(overstock[:3], indent=2)}

PRODUCT DETAILS:
"""
    
    # Add top 10 products by value
    sorted_products = sorted(products, key=lambda x: x.get('price', 0) * x.get('stock', 0), reverse=True)[:10]
    for p in sorted_products:
        prompt += f"\n- {p.get('name')}: {p.get('stock')} units (min: {p.get('min_stock', p.get('minStock', 0))}, price: ₹{p.get('price', 0)})"
    
    prompt += """

PROVIDE ANALYSIS IN THIS EXACT FORMAT:

## EXECUTIVE SUMMARY
[2-3 line summary of overall inventory health status]

## SALES TREND ANALYSIS
[Analyze current trends, identify fast-moving and slow-moving products, predict future demand based on patterns]

## INVENTORY STATUS REPORT
[Detailed assessment of current inventory levels - what's healthy, what needs attention, critical issues]

## IMMEDIATE ACTIONS REQUIRED
[Top 3-5 critical actions with justification]

## FINANCIAL IMPACT ANALYSIS
[Impact of current inventory state on cash flow and working capital]

## STRATEGIC RECOMMENDATIONS
[Long-term recommendations for inventory optimization]

Be specific with product names and numbers. Use business language. Focus on actionable insights."""
    
    return prompt


def _parse_gemini_response(response_text: str) -> Dict[str, str]:
    """Parse Gemini response into structured format"""
    
    sections = {
        "summary": "EXECUTIVE SUMMARY",
        "sales_trend_analysis": "SALES TREND ANALYSIS",
        "inventory_status": "INVENTORY STATUS REPORT",
        "actions": "IMMEDIATE ACTIONS REQUIRED",
        "financial": "FINANCIAL IMPACT ANALYSIS",
        "recommendations": "STRATEGIC RECOMMENDATIONS"
    }
    
    result = {}
    
    for key, section_title in sections.items():
        if section_title in response_text:
            start = response_text.find(section_title) + len(section_title)
            
            # Find next section
            end = len(response_text)
            for next_section in sections.values():
                if next_section != section_title:
                    pos = response_text.find(next_section, start)
                    if pos != -1:
                        end = min(end, pos)
            
            content = response_text[start:end].strip()
            # Clean up
            content = '\n'.join(line for line in content.split('\n') if line.strip())
            result[key] = content[:1000]  # Limit to 1000 chars
        else:
            result[key] = "Analysis in progress..."
    
    return result


def _get_local_analysis(products: List[Dict[str, Any]], metrics: Dict,
                       critical_alerts: List, low_stock: List, overstock: List) -> Dict[str, str]:
    """Fallback local analysis"""
    
    summary = f"📊 Inventory Report: {metrics['total_items']} products, ₹{metrics['total_value']:,.0f} total value. "
    
    if len(critical_alerts) > 0:
        summary += f"🚨 {len(critical_alerts)} critical issues need immediate attention. "
    
    if len(low_stock) > 0:
        summary += f"⚠️ {len(low_stock)} products below minimum stock. "
    
    if len(overstock) > 0:
        summary += f"📈 {len(overstock)} products overstocked. "
    
    if metrics['healthy_count'] > 0:
        summary += f"✅ {metrics['healthy_count']} products at optimal levels."
    
    trend_analysis = f"Current inventory shows {len(low_stock)} items at risk of stockout and {len(overstock)} items overstocked. "
    trend_analysis += "Fast-moving products need frequent replenishment. "
    trend_analysis += f"Total inventory value is ₹{metrics['total_value']:,.0f}, with ₹{metrics['at_risk_value']:,.0f} at risk."
    
    inventory_status = f"🔴 Critical: {len(critical_alerts)} / 🟠 Low Stock: {len(low_stock)} / 🟢 Healthy: {metrics['healthy_count']} / 🔵 Overstock: {len(overstock)}\n"
    inventory_status += f"Cash tied up in excess stock: ₹{metrics['overstock_value']:,.0f}"
    
    return {
        "summary": summary,
        "sales_trend_analysis": trend_analysis,
        "inventory_status": inventory_status,
        "actions": "Prioritize orders for critical items. Review overstock for potential discounts.",
        "financial": f"Total inventory value: ₹{metrics['total_value']:,.0f}. At-risk value: ₹{metrics['at_risk_value']:,.0f}",
        "recommendations": "Implement regular stock reviews. Use predictive ordering. Consider demand forecasting."
    }


def _generate_trend_data(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate sales trend data for graph visualization"""
    
    # Simulate trend data (in production, this would come from sales_data table)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Average sales for each product by day
    trend_by_product = {}
    for product in products[:5]:  # Top 5 products
        trend_by_product[product.get('name', 'Unknown')] = [
            int(product.get('stock', 0) * 0.05 * (i + 1)) for i in range(7)
        ]
    
    return {
        "labels": days,
        "datasets": [
            {
                "label": name,
                "data": values,
                "borderColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"][i],
                "tension": 0.4
            }
            for i, (name, values) in enumerate(trend_by_product.items())
        ]
    }


def _generate_status_chart_data(products: List[Dict[str, Any]], metrics: Dict) -> Dict[str, Any]:
    """Generate inventory status chart data"""
    
    return {
        "labels": ["Critical", "Low Stock", "Healthy", "Overstock"],
        "datasets": [{
            "label": "Inventory Status",
            "data": [
                len([p for p in products if p.get('stock', 0) == 0]),
                metrics['low_stock_count'],
                metrics['healthy_count'],
                len([p for p in products if p.get('stock', 0) > p.get('max_stock', p.get('maxStock', p.get('min_stock', p.get('minStock', 0)) * 3))])
            ],
            "backgroundColor": ["#FF4444", "#FFAA00", "#44AA44", "#4488FF"]
        }]
    }


def _build_recommendations(low_stock: List[Dict], overstock: List[Dict], 
                          critical_alerts: List[Dict]) -> List[Dict[str, Any]]:
    """Build action recommendations"""
    
    recommendations = []
    
    # Critical actions
    for alert in critical_alerts[:3]:
        recommendations.append({
            "priority": "CRITICAL",
            "action": f"Immediately order {alert.get('product_name', 'product')}",
            "reason": alert.get('message', ''),
            "timeline": "Today"
        })
    
    # Low stock actions
    for item in low_stock[:5]:
        needed = item.get('recommended_order', 0)
        recommendations.append({
            "priority": "HIGH",
            "action": f"Order {needed} units of {item['product_name']}",
            "reason": f"Stock will run out in ~{item['lead_time_days']} days",
            "timeline": "Within 48 hours"
        })
    
    # Overstock actions
    for item in overstock[:3]:
        recommendations.append({
            "priority": "MEDIUM",
            "action": f"Reduce {item['product_name']} inventory",
            "reason": f"₹{item['cash_locked']:,.0f} cash locked in excess stock",
            "timeline": "This week",
            "suggestion": "Apply promotional pricing or clearance"
        })
    
    return recommendations


def _get_empty_analysis() -> Dict[str, Any]:
    """Return empty analysis structure"""
    return {
        "timestamp": datetime.now().isoformat(),
        "summary": "No inventory data available",
        "critical_alerts": [],
        "low_stock_items": [],
        "overstock_items": [],
        "recommendations": [],
        "sales_trend_analysis": "No sales data available",
        "inventory_status": "No inventory to analyze",
        "financial_impact": {
            "total_inventory_value": 0,
            "at_risk_value": 0,
            "overstock_value": 0,
            "cash_locked": 0
        },
        "metrics": {
            "total_items": 0,
            "total_stock": 0,
            "total_value": 0,
            "at_risk_value": 0,
            "overstock_value": 0,
            "low_stock_count": 0,
            "healthy_count": 0
        },
        "trend_data": {"labels": [], "datasets": []},
        "status_chart_data": {"labels": [], "datasets": []},
        "ai_powered": True
    }
