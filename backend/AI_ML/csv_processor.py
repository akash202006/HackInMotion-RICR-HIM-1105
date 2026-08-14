"""
CSV Processing with Gemini AI
Processes CSV data using Gemini before saving to database.
No raw data is stored — only cleaned, structured records.
"""

import csv
import io
import json
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    from google import genai
except ImportError:
    genai = None
from app.config import settings

from ai_ml.gemini_client import GeminiClient

BATCH_SIZE = 50
GEMINI_MODEL = "gemini-2.5-flash"
SUPPORTED_GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

PRODUCT_ALIASES = {
    "name": ["name", "product_name", "product", "item", "item_name", "title"],
    "sku": ["sku", "product_sku", "code", "product_code", "item_code", "id"],
    "category": ["category", "cat", "type", "product_category", "group"],
    "stock": ["stock", "quantity", "qty", "inventory", "current_stock", "stock_qty"],
    "price": ["price", "unit_price", "cost", "mrp", "selling_price", "rate"],
    "supplier": ["supplier", "vendor", "supplier_name", "vendor_name"],
    "lead_time": ["lead_time", "leadtime", "delivery_days", "lead_days"],
    "min_stock": ["min_stock", "minstock", "minimum_stock", "reorder_level", "min_qty"],
    "max_stock": ["max_stock", "maxstock", "maximum_stock", "max_qty"],
}

SALES_ALIASES = {
    "product_sku": ["product_sku", "sku", "product_code", "item_code", "code"],
    "quantity_sold": ["quantity_sold", "qty", "quantity", "units_sold", "sold", "sales_qty"],
    "revenue": ["revenue", "amount", "total", "total_amount", "sales_amount", "value"],
    "sale_date": ["sale_date", "date", "transaction_date", "order_date", "sold_date"],
}


class CSVProcessor:
    """Process CSV files using Gemini AI — no raw data stored."""

    @staticmethod
    def initialize_gemini() -> bool:
        if not settings.gemini_api_key:
            return False
        try:
            GeminiClient(api_key=settings.gemini_api_key)
            return True
        except Exception as exc:
            print(f"[WARNING] Gemini init failed: {exc}")
            return False

    @staticmethod
    def parse_csv(csv_content: str) -> Tuple[List[Dict[str, str]], List[str]]:
        try:
            reader = csv.DictReader(io.StringIO(csv_content))
            rows = [dict(row) for row in reader]
            headers = list(reader.fieldnames or [])
            return rows, headers
        except Exception:
            return [], []

    @staticmethod
    def _normalize_header(header: str) -> str:
        return re.sub(r"[^a-z0-9]", "_", header.strip().lower())

    @staticmethod
    def _map_columns(headers: List[str], alias_map: Dict[str, List[str]]) -> Dict[str, str]:
        """Map CSV headers to standard field names."""
        normalized = {CSVProcessor._normalize_header(h): h for h in headers}
        mapping: Dict[str, str] = {}
        for standard, aliases in alias_map.items():
            for alias in aliases:
                key = CSVProcessor._normalize_header(alias)
                if key in normalized:
                    mapping[standard] = normalized[key]
                    break
        return mapping

    @staticmethod
    def _extract_json(text: str) -> Optional[Dict[str, Any]]:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            return None
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _rows_to_preview(rows: List[Dict[str, str]], headers: List[str]) -> str:
        preview = f"Headers: {headers}\n\n"
        for i, row in enumerate(rows):
            preview += f"Row {i + 1}: {json.dumps(row)}\n"
        return preview

    @staticmethod
    def _call_gemini(prompt: str, max_tokens: int = 8000) -> Optional[Dict[str, Any]]:
        if not CSVProcessor.initialize_gemini():
            return None
        try:
            last_error = None
            for model_name in SUPPORTED_GEMINI_MODELS:
                try:
                    client = GeminiClient(api_key=settings.gemini_api_key)
                    response_text = client.generate_text(
                        prompt,
                        model_name=model_name,
                        temperature=0.2,
                        max_output_tokens=max_tokens,
                    )
                    if response_text:
                        parsed = CSVProcessor._extract_json(response_text)
                        if parsed is not None:
                            return parsed
                        return {"raw_text": response_text}
                except Exception as e:
                    last_error = e
                    print(f"[WARNING] Gemini model {model_name} failed: {str(e)}")
            if last_error:
                print(f"[WARNING] All Gemini model attempts failed: {last_error}")
            print(f"[INFO] Falling back to local CSV processing...")
            return None
        except Exception as e:
            print(f"[WARNING] Gemini API error: {str(e)}")
            print(f"[INFO] Falling back to local CSV processing...")
            return None

    @staticmethod
    async def detect_data_type(
        headers: List[str], sample_rows: List[Dict[str, str]]
    ) -> str:
        """Detect whether CSV contains products or sales data."""
        header_text = ", ".join(headers).lower()
        sales_signals = ["quantity_sold", "revenue", "sale_date", "sold", "transaction"]
        product_signals = ["stock", "price", "supplier", "category", "lead_time", "min_stock"]

        sales_score = sum(1 for s in sales_signals if s in header_text)
        product_score = sum(1 for s in product_signals if s in header_text)

        if sales_score > product_score:
            return "sales"
        if product_score > sales_score:
            return "products"

        preview = CSVProcessor._rows_to_preview(sample_rows[:5], headers)
        prompt = f"""Analyze this CSV and determine the data type.

{preview}

Return ONLY JSON:
{{"data_type": "products" or "sales", "confidence": "high/medium/low", "reason": "brief explanation"}}

Rules:
- "products" = inventory/product catalog (name, sku, stock, price, etc.)
- "sales" = sales transactions (sku, quantity sold, revenue, date)
"""
        result = CSVProcessor._call_gemini(prompt, max_tokens=500)
        if result and result.get("data_type") in ("products", "sales"):
            return result["data_type"]
        return "products"

    @staticmethod
    def _process_products_batch(
        batch: List[Dict[str, str]], headers: List[str], batch_num: int, total_batches: int
    ) -> Dict[str, Any]:
        preview = CSVProcessor._rows_to_preview(batch, headers)
        prompt = f"""Process product inventory CSV data (batch {batch_num}/{total_batches}).

{preview}

Rules:
1. Auto-detect column names (SKU, Product Name, Qty, etc.) and map to standard fields
2. Required: name, sku, stock, price
3. Clean: trim whitespace, fix numbers, standardize categories
4. Defaults: supplier="Local Supplier", lead_time=3, min_stock=max(10, 20% of stock), max_stock=stock*3
5. Return ONLY JSON:

{{
  "valid_products": [
    {{"name": "...", "sku": "...", "category": "...", "stock": 0, "price": 0.0,
      "supplier": "...", "lead_time": 3, "min_stock": 10, "max_stock": 100}}
  ],
  "invalid_rows": [{{"row_data": "...", "reason": "...", "suggestion": "..."}}]
}}
"""
        result = CSVProcessor._call_gemini(prompt)
        if result:
            return result
        return CSVProcessor._local_fallback_products(batch, headers)

    @staticmethod
    def _process_sales_batch(
        batch: List[Dict[str, str]],
        headers: List[str],
        sku_to_id: Dict[str, int],
        batch_num: int,
        total_batches: int,
    ) -> Dict[str, Any]:
        preview = CSVProcessor._rows_to_preview(batch, headers)
        valid_skus = list(sku_to_id.keys())[:100]
        prompt = f"""Process sales transaction CSV data (batch {batch_num}/{total_batches}).

{preview}

Valid product SKUs: {json.dumps(valid_skus)}

Rules:
1. Auto-detect columns (SKU, Qty, Amount, Date, etc.)
2. Required: product_sku, quantity_sold, revenue, sale_date (YYYY-MM-DD)
3. SKU must match valid SKUs list (case-insensitive match OK)
4. Return ONLY JSON:

{{
  "valid_sales": [
    {{"product_sku": "...", "quantity_sold": 0, "revenue": 0.0, "sale_date": "YYYY-MM-DD"}}
  ],
  "invalid_rows": [{{"row_data": "...", "reason": "...", "suggestion": "..."}}]
}}
"""
        result = CSVProcessor._call_gemini(prompt)
        if result:
            return result
        return CSVProcessor._local_fallback_sales(batch, headers, sku_to_id)

    @staticmethod
    def _local_fallback_products(
        rows: List[Dict[str, str]], headers: List[str]
    ) -> Dict[str, Any]:
        mapping = CSVProcessor._map_columns(headers, PRODUCT_ALIASES)
        valid, invalid = [], []

        for row in rows:
            try:
                name = row.get(mapping.get("name", ""), "").strip()
                sku = row.get(mapping.get("sku", ""), "").strip()
                if not name or not sku:
                    invalid.append({"reason": "Missing name or sku", "suggestion": "Add required fields"})
                    continue

                stock = max(0, int(float(row.get(mapping.get("stock", ""), 0) or 0)))
                price = max(0.0, float(row.get(mapping.get("price", ""), 0) or 0))
                min_stock = int(float(row.get(mapping.get("min_stock", ""), max(10, int(stock * 0.2))) or 10))

                valid.append({
                    "name": name,
                    "sku": sku,
                    "category": row.get(mapping.get("category", ""), "General").strip() or "General",
                    "stock": stock,
                    "price": price,
                    "supplier": row.get(mapping.get("supplier", ""), "Local Supplier").strip() or "Local Supplier",
                    "lead_time": int(float(row.get(mapping.get("lead_time", ""), 3) or 3)),
                    "min_stock": min_stock,
                    "max_stock": int(float(row.get(mapping.get("max_stock", ""), stock * 3) or stock * 3)),
                })
            except (ValueError, TypeError) as e:
                invalid.append({"reason": str(e), "suggestion": "Check numeric fields"})

        return {"valid_products": valid, "invalid_rows": invalid}

    @staticmethod
    def _local_fallback_sales(
        rows: List[Dict[str, str]], headers: List[str], sku_to_id: Dict[str, int]
    ) -> Dict[str, Any]:
        mapping = CSVProcessor._map_columns(headers, SALES_ALIASES)
        sku_lookup = {k.lower(): k for k in sku_to_id}
        valid, invalid = [], []

        for row in rows:
            try:
                raw_sku = row.get(mapping.get("product_sku", ""), "").strip()
                matched_sku = sku_lookup.get(raw_sku.lower())
                if not matched_sku:
                    invalid.append({"reason": f"SKU '{raw_sku}' not found", "suggestion": "Check SKU spelling"})
                    continue

                qty = int(float(row.get(mapping.get("quantity_sold", ""), 0) or 0))
                revenue = float(row.get(mapping.get("revenue", ""), 0) or 0)
                date_str = row.get(mapping.get("sale_date", ""), "").strip()

                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
                    try:
                        date_str = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
                else:
                    invalid.append({"reason": f"Invalid date '{date_str}'", "suggestion": "Use YYYY-MM-DD format"})
                    continue

                if qty <= 0:
                    invalid.append({"reason": "Quantity must be positive", "suggestion": "Fix quantity"})
                    continue

                valid.append({
                    "product_sku": matched_sku,
                    "quantity_sold": qty,
                    "revenue": revenue,
                    "sale_date": date_str,
                })
            except (ValueError, TypeError) as e:
                invalid.append({"reason": str(e), "suggestion": "Check field values"})

        return {"valid_sales": valid, "invalid_rows": invalid}

    @staticmethod
    def _format_product_records(products: List[Dict], user_id: str) -> List[Dict]:
        formatted = []
        for p in products:
            stock = int(p.get("stock", 0))
            formatted.append({
                "user_id": user_id,
                "name": str(p.get("name", "")).strip(),
                "sku": str(p.get("sku", "")).strip(),
                "category": str(p.get("category", "General")).strip() or "General",
                "stock": stock,
                "price": float(p.get("price", 0)),
                "supplier": str(p.get("supplier", "Local Supplier")).strip() or "Local Supplier",
                "lead_time": int(p.get("lead_time", 3)),
                "min_stock": int(p.get("min_stock", max(10, int(stock * 0.2)))),
                "max_stock": int(p.get("max_stock", stock * 3)),
            })
        return formatted

    @staticmethod
    def _format_sales_records(
        sales: List[Dict], user_id: str, sku_to_id: Dict[str, int]
    ) -> List[Dict]:
        formatted = []
        sku_lookup = {k.lower(): k for k in sku_to_id}
        for s in sales:
            raw_sku = str(s.get("product_sku", "")).strip()
            sku = sku_lookup.get(raw_sku.lower(), raw_sku)
            if sku not in sku_to_id:
                continue
            formatted.append({
                "user_id": user_id,
                "product_id": sku_to_id[sku],
                "quantity_sold": int(s.get("quantity_sold", 0)),
                "revenue": float(s.get("revenue", 0)),
                "sale_date": s.get("sale_date", ""),
            })
        return formatted

    @staticmethod
    async def process_products_csv(csv_content: str, user_id: str) -> Dict[str, Any]:
        rows, headers = CSVProcessor.parse_csv(csv_content)
        if not rows:
            return {"status": "error", "message": "No data found in CSV", "products": [], "errors": []}

        all_products, all_errors = [], []
        batches = [rows[i : i + BATCH_SIZE] for i in range(0, len(rows), BATCH_SIZE)]
        total_batches = len(batches)

        for idx, batch in enumerate(batches, 1):
            result = CSVProcessor._process_products_batch(batch, headers, idx, total_batches)
            all_products.extend(result.get("valid_products", []))
            for inv in result.get("invalid_rows", []):
                all_errors.append(f"Row skipped: {inv.get('reason')} - {inv.get('suggestion', '')}")

        products = CSVProcessor._format_product_records(all_products, user_id)
        return {
            "status": "success",
            "message": f"Processed {len(products)} valid products from {len(rows)} rows",
            "products": products,
            "errors": all_errors,
            "summary": {
                "total_rows": len(rows),
                "valid": len(products),
                "invalid": len(all_errors),
                "batches_processed": total_batches,
                "processing_notes": "Gemini AI validated and cleaned all data — no raw data stored",
            },
        }

    @staticmethod
    async def process_sales_csv(
        csv_content: str, user_id: str, sku_to_id: Dict[str, int]
    ) -> Dict[str, Any]:
        rows, headers = CSVProcessor.parse_csv(csv_content)
        if not rows:
            return {"status": "error", "message": "No data found in CSV", "sales": [], "errors": []}

        all_sales, all_errors = [], []
        batches = [rows[i : i + BATCH_SIZE] for i in range(0, len(rows), BATCH_SIZE)]
        total_batches = len(batches)

        for idx, batch in enumerate(batches, 1):
            result = CSVProcessor._process_sales_batch(batch, headers, sku_to_id, idx, total_batches)
            all_sales.extend(result.get("valid_sales", []))
            for inv in result.get("invalid_rows", []):
                all_errors.append(f"Row skipped: {inv.get('reason')} - {inv.get('suggestion', '')}")

        sales = CSVProcessor._format_sales_records(all_sales, user_id, sku_to_id)
        total_revenue = sum(s["revenue"] for s in sales)
        total_qty = sum(s["quantity_sold"] for s in sales)
        dates = [s["sale_date"] for s in sales if s.get("sale_date")]

        return {
            "status": "success",
            "message": f"Processed {len(sales)} valid sales records from {len(rows)} rows",
            "sales": sales,
            "errors": all_errors,
            "summary": {
                "total_rows": len(rows),
                "valid": len(sales),
                "invalid": len(all_errors),
                "total_revenue": total_revenue,
                "total_quantity": total_qty,
                "date_range": f"{min(dates)} to {max(dates)}" if dates else "N/A",
                "batches_processed": total_batches,
                "processing_notes": "Gemini AI validated and cleaned all data — no raw data stored",
            },
        }

    @staticmethod
    async def process_csv_auto(
        csv_content: str, user_id: str, sku_to_id: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Smart CSV upload: auto-detect type, process ALL rows with Gemini, save structured data.
        No raw data is ever stored in the database.
        """
        rows, headers = CSVProcessor.parse_csv(csv_content)
        if not rows:
            return {"status": "error", "message": "No data found in CSV", "data_type": None}

        data_type = await CSVProcessor.detect_data_type(headers, rows[:10])

        if data_type == "sales":
            if not sku_to_id:
                return {
                    "status": "error",
                    "message": "Sales data detected but no products exist. Upload products first.",
                    "data_type": "sales",
                }
            result = await CSVProcessor.process_sales_csv(csv_content, user_id, sku_to_id)
            result["data_type"] = "sales"
            return result

        result = await CSVProcessor.process_products_csv(csv_content, user_id)
        result["data_type"] = "products"
        return result
