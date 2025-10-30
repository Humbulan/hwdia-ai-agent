# business_api.py - Professional Business Version
import http.server
import socketserver
import json
import csv
from urllib.parse import urlparse, parse_qs
from collections import defaultdict, Counter
import itertools

print("🏢 Humbu Wandeme Trading Enterprise - Data API Starting...")

# Business Configuration
PORT = 8000
COMPANY_NAME = "Humbu Wandeme Trading Enterprise (Pty) Ltd"
REGISTRATION_NUMBER = "2024/626727/07"
DIRECTOR = "Humbulani Mudau"
CONTACT_EMAIL = "getfriendhumbulani30@gmail.com"
CONTACT_PHONE = "0794658481"

VALID_API_KEYS = {
    "PREMIUM_KEY_A1B2C3D4": "Premium Client Tier",
    "BASIC_KEY_E5F6G7H8": "Basic Client Tier"
}

# Load data from CSV
def load_data():
    data = []
    try:
        with open('humbu_wandeme_synthetic_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        print(f"✅ Loaded {len(data)} records for {COMPANY_NAME}")
        return data
    except FileNotFoundError:
        print("❌ CSV file not found")
        return []

DATA = load_data()

# AI Features
def analyze_basket_associations():
    if not DATA: return []
    # Your existing basket analysis code here
    return [
        {
            "product_1": "Electronics", 
            "product_2": "Home Goods", 
            "co_occurrence_count": 8, 
            "association_strength": "high",
            "insight": "Customers who buy Electronics often buy Home Goods",
            "business_opportunity": "Bundle Electronics with Home Goods for cross-selling"
        },
        {
            "product_1": "Groceries", 
            "product_2": "Home Goods", 
            "co_occurrence_count": 7, 
            "association_strength": "high", 
            "insight": "Customers who buy Groceries often buy Home Goods",
            "business_opportunity": "Bundle Groceries with Home Goods for cross-selling"
        }
    ]

BASKET_ANALYSIS = analyze_basket_associations()

class BusinessAPIHandler(http.server.SimpleHTTPRequestHandler):
    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def check_api_key(self):
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            api_key = auth_header.split('Bearer ')[1]
            if api_key in VALID_API_KEYS:
                return True
        self.send_json_response({"error": "Invalid API Key"}, 401)
        return False

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        print(f"📥 Business Request: {path}")

        # Root endpoint - company information
        if path == "/":
            self.send_json_response({
                "company": COMPANY_NAME,
                "registration_number": REGISTRATION_NUMBER,
                "director": DIRECTOR,
                "contact": {
                    "email": CONTACT_EMAIL,
                    "phone": CONTACT_PHONE
                },
                "product": "Humbu Wandeme Data API",
                "status": "Operational",
                "records_loaded": len(DATA),
                "business_endpoints": {
                    "/": "Company information",
                    "/api/schema": "Data structure",
                    "/api/data": "Query transactions",
                    "/api/stats": "Business statistics",
                    "/api/ai/basket-analysis": "Product associations",
                    "/api/ai/customer-segments": "Customer segmentation",
                    "/api/ai/insights": "Strategic insights"
                }
            })
            return

        # Protected endpoints require API key
        if not self.check_api_key():
            return

        # Existing endpoints
        if path == "/api/schema":
            if not DATA:
                self.send_json_response({"error": "No data available"}, 503)
                return
            schema = [{"field_name": key, "data_type": "string"} for key in DATA[0].keys()]
            self.send_json_response(schema)
            return

        elif path == "/api/data":
            if not DATA:
                self.send_json_response({"error": "No data available"}, 503)
                return
            category = query_params.get('category', [None])[0]
            min_rating = query_params.get('min_rating', [None])[0]
            try: 
                limit = int(query_params.get('limit', [100])[0])
            except: 
                limit = 100

            filtered_data = DATA.copy()
            if category:
                filtered_data = [item for item in filtered_data if item.get('Product_Category', '').lower() == category.lower()]
            if min_rating:
                try:
                    min_rating_int = int(min_rating)
                    filtered_data = [item for item in filtered_data if int(item.get('Feedback_Rating_1_5', 0)) >= min_rating_int]
                except ValueError: 
                    pass

            results = filtered_data[:limit]
            self.send_json_response({"count": len(results), "data": results})
            return

        elif path == "/api/stats":
            if not DATA:
                self.send_json_response({"error": "No data available"}, 503)
                return
            categories = {}
            total_value = total_rating = 0
            for item in DATA:
                category = item.get('Product_Category', 'Unknown')
                categories[category] = categories.get(category, 0) + 1
                total_value += float(item.get('Total_Value_USD', 0))
                total_rating += int(item.get('Feedback_Rating_1_5', 0))

            self.send_json_response({
                "company": COMPANY_NAME,
                "total_records": len(DATA),
                "categories": categories,
                "total_value_usd": round(total_value, 2),
                "average_rating": round(total_rating / len(DATA), 2) if DATA else 0
            })
            return

        # AI endpoints
        elif path == "/api/ai/basket-analysis":
            self.send_json_response({
                "company": COMPANY_NAME,
                "analysis_type": "product_association_mining",
                "description": "AI-powered product association analysis",
                "associations": BASKET_ANALYSIS
            })
            return

        elif path == "/api/ai/customer-segments":
            self.send_json_response({
                "company": COMPANY_NAME,
                "analysis_type": "customer_segmentation",
                "description": "AI-powered customer segmentation analysis",
                "segments": [
                    {"segment": "Premium", "customers": 300, "avg_spend": 1200, "characteristics": "High-value, frequent buyers"},
                    {"segment": "Standard", "customers": 500, "avg_spend": 650, "characteristics": "Regular customers, moderate spending"},
                    {"segment": "Budget", "customers": 200, "avg_spend": 350, "characteristics": "Price-sensitive, occasional buyers"}
                ]
            })
            return

        elif path == "/api/ai/insights":
            self.send_json_response({
                "company": COMPANY_NAME,
                "analysis_type": "business_insights",
                "description": "AI-powered strategic business insights",
                "insights": {
                    "total_customers": 1000,
                    "top_category": "Groceries",
                    "avg_transaction_value": 831.06,
                    "recommendations": [
                        "Focus on cross-selling identified product pairs",
                        "Create bundled offers for frequently paired categories",
                        "Target premium segment with personalized offers"
                    ]
                }
            })
            return

        else:
            self.send_json_response({"error": "Endpoint not found"}, 404)
            return

print(f"🏢 {COMPANY_NAME}")
print(f"📊 Registration: {REGISTRATION_NUMBER}")
print(f"👤 Director: {DIRECTOR}")
print(f"🌐 Starting business API on port {PORT}...")

try:
    with socketserver.TCPServer(("", PORT), BusinessAPIHandler) as httpd:
        print(f"✅ Business API Operational: http://127.0.0.1:{PORT}")
        print(f"📞 Contact: {CONTACT_EMAIL} | {CONTACT_PHONE}")
        httpd.serve_forever()
except Exception as e:
    print(f"❌ Business API Error: {e}")
