try:
    from google import genai
except ImportError:
    genai = None
from app.config import settings
from datetime import datetime, timedelta
from typing import List, Dict, Any

from ai_ml.gemini_client import GeminiClient

# Configure Gemini API
if settings.gemini_api_key and genai is not None:
    GeminiClient(api_key=settings.gemini_api_key)

class GeminiAnalyzer:
    """Gemini AI analyzer for inventory insights"""
    
    @staticmethod
    def generate_insights(products: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate AI insights from inventory data using Gemini
        
        Args:
            products: List of product dictionaries with stock data
            
        Returns:
            Dictionary with AI insights about inventory
        """
        if not products:
            return {
                "stockout_risk": "⚠️ No products to analyze.",
                "reorder_recommendation": "📋 Add products to your inventory first.",
                "overstock_analysis": "📊 No overstock analysis available."
            }
        
        try:
            # Prepare inventory summary
            inventory_summary = _prepare_inventory_summary(products)
            
            # Try to call Gemini API
            if settings.gemini_api_key:
                try:
                    # Build prompt for Gemini
                    prompt = _build_analysis_prompt(inventory_summary)
                    
                    # Try multiple model options
                    model_options = GeminiClient().supported_models
                    response = None
                    
                    for model_name in model_options:
                        try:
                            client = GeminiClient(api_key=settings.gemini_api_key)
                            response_text = client.generate_text(prompt, model_name=model_name)
                            if response_text:
                                insights = _parse_gemini_response(response_text)
                                return insights
                        except Exception as model_error:
                            print(f"Model {model_name} failed: {model_error}")
                            continue
                    
                    # If no model worked, use local analysis
                    print("All Gemini models failed, using local analysis")
                    return _generate_local_insights(products, inventory_summary)
                    
                except Exception as api_error:
                    print(f"Gemini API error: {api_error}")
                    return _generate_local_insights(products, inventory_summary)
            else:
                # No API key configured, use local analysis
                return _generate_local_insights(products, inventory_summary)
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            return {
                "stockout_risk": "⚠️ Unable to analyze inventory right now.",
                "reorder_recommendation": "📋 Please try again later.",
                "overstock_analysis": "📊 Check back soon for analysis."
            }

def _generate_local_insights(products: List[Dict[str, Any]], summary: str) -> Dict[str, str]:
    """Generate insights locally without Gemini API"""
    
    low_stock_items = []
    overstock_items = []
    total_value = 0
    
    for product in products:
        stock = product.get('stock', 0)
        min_stock = product.get('minStock', product.get('min_stock', 0))
        lead_time = product.get('leadTime', product.get('lead_time', 0))
        price = product.get('price', 0)
        name = product.get('name', 'Unknown')
        
        total_value += stock * price
        
        if stock < min_stock:
            shortage_days = max(1, lead_time - (stock / max(1, min_stock)))
            low_stock_items.append({
                'name': name,
                'stock': stock,
                'min': min_stock,
                'days': shortage_days,
                'lead_time': lead_time
            })
        elif stock > min_stock * 3:
            overstock_items.append({
                'name': name,
                'stock': stock,
                'excess': stock - (min_stock * 3),
                'value': stock * price
            })
    
    # Build insights - return clean HTML-friendly format
    if low_stock_items:
        risk_items = low_stock_items[:3]
        risk_text = f"<strong>{len(low_stock_items)} product(s) below minimum stock:</strong><br>"
        for item in risk_items:
            risk_text += f"<div style='margin-top:8px;'><strong>{item['name']}</strong><br><small>{item['stock']} units (min: {item['min']}, lead time: {item['lead_time']} days)</small></div>"
    else:
        risk_text = "<strong>✅ All Healthy</strong><br><small>No immediate stockout risks detected.</small>"
    
    if low_stock_items:
        reorder_text = "<strong>Action Required:</strong><br>"
        for item in low_stock_items[:3]:
            needed = max(item['min'] * 2 - item['stock'], 10)
            reorder_text += f"<div style='margin-top:8px;'><strong>{item['name']}</strong><br><small>Order <strong>{needed} units</strong> (Lead time: {item['lead_time']} days)</small></div>"
    else:
        reorder_text = "<strong>Optimal Levels</strong><br><small>Maintain regular stock rotation.</small>"
    
    if overstock_items:
        overstock_text = f"<strong>{len(overstock_items)} product(s) overstocked</strong><br>"
        total_overstock_value = sum(item['value'] for item in overstock_items)
        overstock_text += f"<small>Total excess value: ₹{total_overstock_value:,.0f}</small>"
        for item in overstock_items[:2]:
            overstock_text += f"<div style='margin-top:8px;'><strong>{item['name']}</strong><br><small>{item['excess']} excess units</small></div>"
    else:
        overstock_text = "<strong>Well-Balanced</strong><br><small>No significant overstock detected.</small>"
    
    return {
        "stockout_risk": risk_text,
        "reorder_recommendation": reorder_text,
        "overstock_analysis": overstock_text
    }

def _prepare_inventory_summary(products: List[Dict[str, Any]]) -> str:
    """Prepare a text summary of inventory for Gemini"""
    summary_lines = []
    
    total_stock_value = 0
    low_stock_items = []
    overstock_items = []
    
    for product in products:
        stock = product.get('stock', 0)
        min_stock = product.get('minStock', product.get('min_stock', 0))
        lead_time = product.get('leadTime', product.get('lead_time', 0))
        price = product.get('price', 0)
        name = product.get('name', 'Unknown')
        
        total_stock_value += stock * price
        
        # Categorize products
        if stock < min_stock:
            low_stock_items.append({
                'name': name,
                'current': stock,
                'minimum': min_stock,
                'shortage': min_stock - stock,
                'lead_time': lead_time
            })
        elif stock > min_stock * 3:
            overstock_items.append({
                'name': name,
                'current': stock,
                'excess': stock - (min_stock * 3)
            })
    
    # Format summary
    summary = f"""
INVENTORY ANALYSIS REPORT
========================
Total Products: {len(products)}
Total Inventory Value: ₹{total_stock_value:,.2f}

LOW STOCK ALERTS ({len(low_stock_items)} items):
{_format_low_stock(low_stock_items)}

OVERSTOCK ITEMS ({len(overstock_items)} items):
{_format_overstock(overstock_items)}

HEALTHY STOCK: {len(products) - len(low_stock_items) - len(overstock_items)} items

Current Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return summary

def _format_low_stock(items: List[Dict]) -> str:
    """Format low stock items"""
    if not items:
        return "  ✓ No low stock items"
    
    lines = []
    for item in items:
        days_left = _estimate_stock_duration(item['current'], item['lead_time'])
        lines.append(
            f"  • {item['name']}: {item['current']} units (need {item['minimum']}, "
            f"shortage: {item['shortage']} units, lead time: {item['lead_time']}d, "
            f"stock lasts: ~{days_left} days)"
        )
    return '\n'.join(lines)

def _format_overstock(items: List[Dict]) -> str:
    """Format overstock items"""
    if not items:
        return "  ✓ No overstock items"
    
    lines = []
    for item in items:
        lines.append(
            f"  • {item['name']}: {item['current']} units (excess: {item['excess']} units)"
        )
    return '\n'.join(lines)

def _estimate_stock_duration(current_stock: int, lead_time: int) -> int:
    """Estimate how many days current stock will last"""
    # Estimate daily consumption based on lead time (longer lead time = lower daily consumption)
    daily_consumption = max(1, (lead_time + 10) // 5)
    return max(1, current_stock // daily_consumption) if current_stock > 0 else 0

def _build_analysis_prompt(inventory_summary: str) -> str:
    """Build the prompt for Gemini AI"""
    return f"""You are an expert inventory and supply chain analyst. Analyze the following inventory data and provide insights:

{inventory_summary}

Please provide your analysis in the following format (use emoji bullets for clarity):

STOCKOUT RISKS:
[Analyze which products are at risk of running out. Include specific product names, current stock levels, and estimated days until stockout based on lead times. Be concise but comprehensive.]

REORDER RECOMMENDATIONS:
[Provide specific reorder recommendations including which products to order, how many units, and urgency levels. Consider lead times and safety stock. Include cost implications if possible.]

OVERSTOCK ANALYSIS:
[Identify products with excess inventory and suggest optimization strategies like promotions or clearance sales. Include cash flow impact.]

CASH FLOW IMPACT:
[Brief analysis of inventory value and cash tied up in stock. Suggest if there are opportunities to free up cash.]

Keep the response concise, actionable, and use business-friendly language. Use bullet points and emojis for clarity."""

def _parse_gemini_response(response_text: str) -> Dict[str, str]:
    """Parse Gemini response into structured insights"""
    sections = {
        "stockout_risk": "STOCKOUT RISKS:",
        "reorder_recommendation": "REORDER RECOMMENDATIONS:",
        "overstock_analysis": "OVERSTOCK ANALYSIS:"
    }
    
    insights = {}
    
    for key, section_header in sections.items():
        if section_header in response_text:
            # Extract content after this section until next section or end
            start = response_text.find(section_header) + len(section_header)
            next_sections = [s for s in sections.values() if s != section_header]
            
            end = len(response_text)
            for next_section in next_sections:
                next_pos = response_text.find(next_section, start)
                if next_pos != -1:
                    end = min(end, next_pos)
            
            content = response_text[start:end].strip()
            # Clean up the content
            content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())
            insights[key] = content[:500]  # Limit to 500 chars per insight
        else:
            insights[key] = "Analysis in progress..."
    
    return insights
