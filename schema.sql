-- USERS
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CATEGORIES
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SUPPLIERS
CREATE TABLE suppliers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150),
    email VARCHAR(150),
    phone VARCHAR(20),
    address TEXT,
    active BOOLEAN DEFAULT TRUE
);

-- PRODUCTS
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150),
    description TEXT,
    price DECIMAL(10,2),
    status VARCHAR(20),
    category_id BIGINT,
    supplier_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES categories(id),

    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE INDEX idx_product_category ON products(category_id);
CREATE INDEX idx_product_supplier ON products(supplier_id);

-- INVENTORY
CREATE TABLE inventory (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT UNIQUE,
    available_quantity INT DEFAULT 0,
    reserved_quantity INT DEFAULT 0,

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id) REFERENCES products(id)
);

-- PURCHASE ORDERS
CREATE TABLE purchase_orders (
    id BIGSERIAL PRIMARY KEY,
    supplier_id BIGINT,
    order_date DATE,
    status VARCHAR(30),
    total_amount DECIMAL(12,2),

    CONSTRAINT fk_po_supplier
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE INDEX idx_po_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_po_date ON purchase_orders(order_date);

-- PURCHASE ORDER ITEMS
CREATE TABLE purchase_order_items (
    id BIGSERIAL PRIMARY KEY,
    purchase_order_id BIGINT,
    product_id BIGINT,
    quantity INT,
    price DECIMAL(10,2),

    CONSTRAINT fk_poi_po
        FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id),

    CONSTRAINT fk_poi_product
        FOREIGN KEY (product_id) REFERENCES products(id)
);

-- STOCK TRANSACTIONS
CREATE TABLE stock_transactions (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT,
    quantity INT,
    transaction_type VARCHAR(10),
    reason VARCHAR(255),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_stock_product
        FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE INDEX idx_stock_product ON stock_transactions(product_id);

-- AUDIT LOGS (Optional: If you still want it in SQL)
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    entity_name VARCHAR(100),
    entity_id BIGINT,
    action VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);