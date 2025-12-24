# Hybrid Inventory Management System (SQL + NoSQL)

**Module:** M605 Advanced Databases  
**Assessment:** Individual Project - Polyglot Persistence Implementation  
**Student Name:** [YOUR NAME HERE]  
**Student ID:** [YOUR ID HERE]

---

## 📖 Project Overview
This project implements a **Hybrid Database System** for an E-Commerce Inventory Management domain. It demonstrates the concept of **Polyglot Persistence** by integrating two distinct database technologies:

1.  **PostgreSQL (SQL):** Handles structured, transactional data (Users, Products, Orders, Inventory) requiring ACID compliance.
2.  **MongoDB (NoSQL):** Handles unstructured, semi-structured data (Customer Reviews, System Logs) requiring schema flexibility.
3.  **Python Application Layer:** Acts as the bridge, fetching data from both databases to present a unified view to the user.
---

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Relational Database:** PostgreSQL 16
* **Document Database:** MongoDB Community Server
* **Libraries:** `psycopg2` (PostgreSQL driver), `pymongo` (MongoDB driver), `Faker` (Data generation)

---

## 📂 Repository Structure
* `schema.sql` - SQL script to create tables, constraints, and indexes in PostgreSQL.
* `mongodb_schema.js` - JavaScript commands to create collections in MongoDB.
* `populate_data.py` - Python script that generates 100+ synthetic records for both databases, ensuring referential integrity.
* `hybrid_app.py` - The main application script that demonstrates the hybrid integration.
* `queries.sql` - List of functional SQL queries used for testing.
* `README.md` - Project documentation.

---

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have the following installed locally:
* Python 3.x
* PostgreSQL
* MongoDB (running on `localhost:27017`)

### 2. Install Python Dependencies
Open your terminal and run:
```bash
pip install psycopg2-binary pymongo faker
