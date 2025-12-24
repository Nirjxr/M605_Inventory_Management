import psycopg2
from pymongo import MongoClient

# --- CONFIGURATION ---
db_password = "" 
pg_config = {
    'dbname': 'inventory_db',
    'user': 'postgres',
    'password': db_password,
    'host': 'localhost'
}

# --- CONNECT ---
try:
    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(**pg_config)
    pg_cursor = pg_conn.cursor()
    
    # Connect to MongoDB
    mongo_client = MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["inventory_logs"]
    
    print("✅ Successfully connected to both databases!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

def get_product_dashboard(product_id):
    print(f"\n--- FETCHING DATA FOR PRODUCT ID: {product_id} ---")
    
    # 1. SQL: Get Structured Data (Name, Price, Stock)
    sql = """
    SELECT p.name, p.price, s.name, i.available_quantity
    FROM products p
    JOIN suppliers s ON p.supplier_id = s.id
    JOIN inventory i ON p.id = i.product_id
    WHERE p.id = %s
    """
    pg_cursor.execute(sql, (product_id,))
    product = pg_cursor.fetchone()
    
    if not product:
        print("❌ Product not found in SQL database.")
        return

    print(f"📦 Product: {product[0]}")
    print(f"💰 Price: ${product[1]}")
    print(f"🏭 Supplier: {product[2]}")
    print(f"📊 Stock Level: {product[3]}")

    # 2. NoSQL: Get Unstructured Data (Reviews)
    reviews = list(mongo_db.product_reviews.find({"productId": product_id}))
    
    print(f"\n--- USER REVIEWS (Found {len(reviews)}) ---")
    if reviews:
        for r in reviews[:3]: 
            stars = "★" * r['rating']
            print(f"{stars} : {r['comment']}")
    else:
        print("No reviews yet.")

# --- RUN THE TEST ---
get_product_dashboard(42)

