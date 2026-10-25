"""
Task 4: SQL + Python Restaurant Performance Report
Assessment: Data Science M4-A1 | Modules 3-4
Platform: Food Delivery Analytics
"""

import sqlite3
import pandas as pd
from tabulate import tabulate

DB_FILE = "food_delivery.db"
CSV_FILE = "restaurant_performance_report.csv"

def init_database():
    """Initializes and seeds the SQLite food_delivery.db database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS restaurants;")

    # Create tables
    cursor.execute("""
    CREATE TABLE restaurants (
        restaurant_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        city TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        restaurant_id INTEGER NOT NULL,
        order_value REAL NOT NULL,
        delivery_time_mins REAL NOT NULL,
        rating REAL NOT NULL,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id)
    );
    """)

    # Insert 10 restaurants (exceeds requirement of at least 8)
    restaurants = [
        (1, 'Spice Villa', 'North Indian', 'Mumbai'),
        (2, 'Pizza Roma', 'Italian', 'Mumbai'),
        (3, 'Burger Barn', 'Fast Food', 'Delhi'),
        (4, 'Dragon Wok', 'Chinese', 'Delhi'),
        (5, 'Royal Biryani', 'North Indian', 'Hyderabad'),
        (6, 'Green Bowl', 'Healthy', 'Bangalore'),
        (7, 'Pasta Fresca', 'Italian', 'Bangalore'),
        (8, 'Dosa Hub', 'South Indian', 'Chennai'),
        (9, 'Tandoor Treats', 'North Indian', 'Mumbai'),
        (10, 'Subway Express', 'Fast Food', 'Delhi')
    ]
    cursor.executemany("INSERT INTO restaurants VALUES (?, ?, ?, ?);", restaurants)

    # Insert 28 orders (exceeds requirement of at least 25)
    orders = [
        (101, 1, 450.0, 35.0, 4.5),
        (102, 1, 520.0, 31.0, 4.6),
        (103, 1, 480.0, 33.0, 4.9),
        (104, 2, 680.0, 28.0, 4.8),
        (105, 2, 720.0, 32.0, 4.7),
        (106, 2, 1150.0, 36.0, 4.5),
        (107, 3, 320.0, 25.0, 3.9),
        (108, 3, 310.0, 22.0, 3.7),
        (109, 4, 850.0, 42.0, 4.2),
        (110, 4, 740.0, 40.0, 4.0),
        (111, 4, 910.0, 45.0, 4.4),
        (112, 5, 1200.0, 38.0, 4.7),
        (113, 5, 1450.0, 41.0, 4.8),
        (114, 5, 980.0, 35.0, 4.6),
        (115, 5, 1600.0, 44.0, 4.9),
        (116, 6, 610.0, 30.0, 4.3),
        (117, 6, 580.0, 28.0, 4.4),
        (118, 7, 920.0, 45.0, 4.4),
        (119, 7, 840.0, 39.0, 4.2),
        (120, 8, 220.0, 20.0, 4.6),
        (121, 8, 260.0, 24.0, 4.7),
        (122, 9, 890.0, 44.0, 4.3),
        (123, 9, 645.0, 50.0, 4.1),
        (124, 10, 290.0, 22.0, 4.4),
        (125, 10, 340.0, 26.0, 3.8),
        (126, 1, 610.0, 29.0, 4.8),
        (127, 2, 890.0, 34.0, 4.6),
        (128, 5, 1350.0, 37.0, 4.8)
    ]
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?);", orders)

    conn.commit()
    conn.close()
    print(f"[1] Database '{DB_FILE}' successfully initialized with 10 restaurants and 28 orders.")

def generate_performance_report():
    conn = sqlite3.connect(DB_FILE)

    # SQL query using GROUP BY with COUNT(), SUM(), ROUND(AVG(), 2)
    sql_query = """
    SELECT 
        r.restaurant_id,
        r.name,
        r.category,
        r.city,
        COUNT(o.order_id) AS total_orders,
        ROUND(SUM(o.order_value), 2) AS total_revenue,
        ROUND(AVG(o.rating), 2) AS avg_rating
    FROM restaurants r
    LEFT JOIN orders o 
        ON r.restaurant_id = o.restaurant_id
    GROUP BY 
        r.restaurant_id, 
        r.name, 
        r.category, 
        r.city
    """

    # Load result into Pandas DataFrame
    df = pd.read_sql_query(sql_query, conn)
    conn.close()

    # Fill NaN revenue if any restaurant has 0 orders
    df['total_revenue'] = df['total_revenue'].fillna(0.0)
    df['avg_rating'] = df['avg_rating'].fillna(0.0)

    # Add a rank column using df['revenue_rank'] = df['total_revenue'].rank(ascending=False, method='min').astype(int)
    df['revenue_rank'] = df['total_revenue'].rank(ascending=False, method='min').astype(int)

    # Sort by rank ascending
    df_sorted = df.sort_values(by='revenue_rank', ascending=True).reset_index(drop=True)

    print("\n" + "-" * 80)
    print("[2] Full Restaurant Performance Ranking Table:")
    print(tabulate(df_sorted, headers='keys', tablefmt='psql', showindex=False))

    # Print Top 5 restaurants by total revenue in a formatted table
    top_5_df = df_sorted.head(5).copy()
    print("\n" + "-" * 80)
    print("[3] Top 5 Restaurants by Total Revenue:")
    print(tabulate(top_5_df, headers='keys', tablefmt='grid', showindex=False))

    # Export complete report to CSV using df.to_csv() with index=False
    df_sorted.to_csv(CSV_FILE, index=False)
    print("\n" + "-" * 80)
    print(f"[4] Export Confirmation: Complete report exported to '{CSV_FILE}' with index=False.")

def main():
    print("=" * 80)
    print("SECTION B - TASK 4: SQL + PYTHON RESTAURANT PERFORMANCE REPORT")
    print("=" * 80)
    init_database()
    generate_performance_report()
    print("=" * 80)
    print("TASK 4 COMPLETED SUCCESSFULLY.")
    print("=" * 80)

if __name__ == "__main__":
    main()
