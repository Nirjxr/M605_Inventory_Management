import psycopg2
from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime

# --- CONFIGURATION ---
db_password = "hammad123"  
sql_config = {
    'user': 'postgres',        
    'password': db_password,
    'host': 'localhost',
    'dbname': 'inventory_db'   
}

# --- CONNECT TO DATABASES ---
fake = Faker()
try:
    sql_conn = psycopg2.connect(**sql_config)
    sql_cursor = sql_conn.cursor()
    mongo_client = MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["inventory_logs"]
    print("Connected to databases!")
except Exception as e:
    print(f"Connection failed: {e}")
    exit()

def execute_sql(query, val):
    sql_cursor.execute(query, val)
    return sql_cursor.fetchone()[0]

# --- 1. POPULATE CATEGORIES ---
print("Populating Categories...")
category_ids = []
categories = ['Electronics', 'Furniture', 'Clothing', 'Books', 'Toys']
for cat in categories:
    sql = "INSERT INTO categories (name, description) VALUES (%s, %s) RETURNING id"
    cat_id = execute_sql(sql, (cat, fake.sentence()))
    category_ids.append(cat_id)

# --- 2. POPULATE SUPPLIERS ---
print("Populating Suppliers...")
supplier_ids = []
for _ in range(20):
    sql = "INSERT INTO suppliers (name, email, phone, address) VALUES (%s, %s, %s, %s) RETURNING id"
    sup_id = execute_sql(sql, (fake.company(), fake.email(), fake.phone_number()[:20], fake.address()))
    supplier_ids.append(sup_id)

# --- 3. POPULATE PRODUCTS ---
print("Populating Products (100+)...")
product_ids = []
for _ in range(120):
    sql = "INSERT INTO products (name, description, price, status, category_id, supplier_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
    vals = (
        fake.catch_phrase(),
        fake.text(),
        round(random.uniform(10.0, 500.0), 2),
        random.choice(['Active', 'Discontinued', 'Out of Stock']),
        random.choice(category_ids),
        random.choice(supplier_ids)
    )
    pid = execute_sql(sql, vals)
    product_ids.append(pid)
    
    # Create Inventory
    inv_sql = "INSERT INTO inventory (product_id, available_quantity) VALUES (%s, %s) RETURNING id"
    execute_sql(inv_sql, (pid, random.randint(0, 100)))

# --- 4. POPULATE USERS ---
print("Populating Users...")
user_ids = []
for _ in range(100):
    sql = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id"
    uid = execute_sql(sql, (fake.name(), fake.unique.email(), "hashed_pass", random.choice(['Admin', 'Customer'])))
    user_ids.append(uid)

# --- 5. POPULATE NO-SQL REVIEWS (MongoDB) ---
print("Populating MongoDB Reviews...")
reviews = []
for _ in range(150):
    review = {
        "productId": random.choice(product_ids),
        "userId": random.choice(user_ids),
        "rating": random.randint(1, 5),
        "comment": fake.sentence(),
        "createdAt": datetime.now()
    }
    reviews.append(review)
mongo_db.product_reviews.insert_many(reviews)

# --- 6. POPULATE ORDERS & ITEMS ---
print("Populating Orders...")
for _ in range(100):
    # Create PO
    sql_po = "INSERT INTO purchase_orders (supplier_id, order_date, status, total_amount) VALUES (%s, %s, %s, %s) RETURNING id"
    po_id = execute_sql(sql_po, (random.choice(supplier_ids), fake.date_this_year(), 'Completed', 0))
    
    # Create Items
    total = 0
    for _ in range(random.randint(1, 5)):
        prod_id = random.choice(product_ids)
        qty = random.randint(1, 10)
        price = round(random.uniform(10, 100), 2)
        total += (price * qty)
        
        sql_item = "INSERT INTO purchase_order_items (purchase_order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s) RETURNING id"
        execute_sql(sql_item, (po_id, prod_id, qty, price))

    # Update total
    sql_cursor.execute("UPDATE purchase_orders SET total_amount = %s WHERE id = %s", (total, po_id))

# Commit and Close
sql_conn.commit()
print("Data Generation Complete! Created 100+ records.")