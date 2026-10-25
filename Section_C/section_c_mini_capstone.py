"""
Section C: Mini Capstone Project - Food Delivery Analytics Console Application
Assessment: Data Science M4-A1 | Modules 3-4
Platform: Food Delivery Analytics
"""

import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

DB_FILE = "food_delivery.db"
EXCEL_FILE = "food_delivery_report.xlsx"
CHART_FILE = "capstone_charts.png"

class FoodDeliveryApp:
    def __init__(self):
        self.cleaned_df = None
        self.sql_summary_df = None
        self.sql_join_df = None
        self.ensure_database()

    def ensure_database(self):
        """Ensures food_delivery.db exists; if not, initializes it self-contained."""
        if not os.path.exists(DB_FILE):
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                restaurant_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                city TEXT NOT NULL
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                restaurant_id INTEGER NOT NULL,
                order_value REAL NOT NULL,
                delivery_time_mins REAL NOT NULL,
                rating REAL NOT NULL,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id)
            );
            """)
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
            cur.executemany("INSERT OR IGNORE INTO restaurants VALUES (?, ?, ?, ?);", restaurants)
            orders = [
                (101, 1, 450.0, 35.0, 4.5), (102, 1, 520.0, 31.0, 4.6), (103, 1, 480.0, 33.0, 4.9),
                (104, 2, 680.0, 28.0, 4.8), (105, 2, 720.0, 32.0, 4.7), (106, 2, 1150.0, 36.0, 4.5),
                (107, 3, 320.0, 25.0, 3.9), (108, 3, 310.0, 22.0, 3.7), (109, 4, 850.0, 42.0, 4.2),
                (110, 4, 740.0, 40.0, 4.0), (111, 4, 910.0, 45.0, 4.4), (112, 5, 1200.0, 38.0, 4.7),
                (113, 5, 1450.0, 41.0, 4.8), (114, 5, 980.0, 35.0, 4.6), (115, 5, 1600.0, 44.0, 4.9),
                (116, 6, 610.0, 30.0, 4.3), (117, 6, 580.0, 28.0, 4.4), (118, 7, 920.0, 45.0, 4.4),
                (119, 7, 840.0, 39.0, 4.2), (120, 8, 220.0, 20.0, 4.6), (121, 8, 260.0, 24.0, 4.7),
                (122, 9, 890.0, 44.0, 4.3), (123, 9, 645.0, 50.0, 4.1), (124, 10, 290.0, 22.0, 4.4),
                (125, 10, 340.0, 26.0, 3.8), (126, 1, 610.0, 29.0, 4.8), (127, 2, 890.0, 34.0, 4.6),
                (128, 5, 1350.0, 37.0, 4.8)
            ]
            cur.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?);", orders)
            conn.commit()
            conn.close()

    def print_header(self, title):
        print("\n" + "=" * 80)
        print(f" {title.upper()} ")
        print("=" * 80)

    # -------------------------------------------------------------
    # OPTION 1: LOAD & CLEAN DATA
    # -------------------------------------------------------------
    def option_load_and_clean_data(self):
        self.print_header("Option 1: Load & Clean Data Pipeline")

        # 1. Create realistic simulated food delivery DataFrame (30 records with issues)
        np.random.seed(101)
        categories = ['North Indian', 'Italian', 'Chinese', 'Fast Food', 'Healthy', 'South Indian']
        restaurants = ['Spice Villa', 'Pizza Roma', 'Dragon Wok', 'Burger Barn', 'Green Bowl', 'Dosa Hub']
        names = ['Aarav', 'Diya', 'Rohan', 'Ananya', 'Kabir', 'Ishita', 'Siddharth', 'Pooja', 'Vikram', 'Neha']

        raw_records = []
        for i in range(1, 26):
            raw_records.append({
                "order_id": 2000 + i,
                "customer_name": np.random.choice(names),
                "restaurant_name": np.random.choice(restaurants),
                "category": np.random.choice(categories),
                "delivery_time_mins": float(np.random.randint(20, 55)),
                "order_value": float(np.random.randint(250, 1200)),
                "rating": round(float(np.random.uniform(3.5, 5.0)), 1)
            })

        df_raw = pd.DataFrame(raw_records)

        # Introduce missing values
        df_raw.loc[2, 'delivery_time_mins'] = np.nan
        df_raw.loc[7, 'delivery_time_mins'] = np.nan
        df_raw.loc[4, 'order_value'] = np.nan
        df_raw.loc[11, 'rating'] = np.nan
        df_raw.loc[14, 'category'] = np.nan

        # Introduce 2 extreme outliers in order_value
        df_raw.loc[8, 'order_value'] = 4200.0
        df_raw.loc[18, 'order_value'] = 3900.0

        # Introduce 3 duplicate rows
        df_raw = pd.concat([df_raw, df_raw.iloc[[1, 5, 9]]], ignore_index=True)

        print("[A] RAW DATA QUALITY ASSESSMENT:")
        print(f"  * Total Raw Records: {len(df_raw)}")
        print(f"  * Duplicated Rows Detected: {df_raw.duplicated().sum()}")
        print("\nMissing Values Count by Column (BEFORE):")
        print(df_raw.isnull().sum())

        # Clean Missing Values
        med_delivery = df_raw['delivery_time_mins'].median()
        med_value = df_raw['order_value'].median()
        mean_rating = round(df_raw['rating'].mean(), 1)
        mode_category = df_raw['category'].mode()[0]

        df_raw['delivery_time_mins'] = df_raw['delivery_time_mins'].fillna(med_delivery)
        df_raw['order_value'] = df_raw['order_value'].fillna(med_value)
        df_raw['rating'] = df_raw['rating'].fillna(mean_rating)
        df_raw['category'] = df_raw['category'].fillna(mode_category)

        # Deduplication
        shape_before = df_raw.shape
        df_clean = df_raw.drop_duplicates().copy()
        shape_after = df_clean.shape

        # Outlier Detection and Capping via IQR
        Q1 = df_clean['order_value'].quantile(0.25)
        Q3 = df_clean['order_value'].quantile(0.75)
        IQR = Q3 - Q1
        upper_fence = Q3 + 1.5 * IQR

        outlier_count = (df_clean['order_value'] > upper_fence).sum()
        df_clean['order_value'] = df_clean['order_value'].clip(lower=0, upper=upper_fence)

        print("\n" + "-" * 80)
        print("[B] BEFORE-AND-AFTER DATA QUALITY SUMMARY:")
        summary_table = [
            ["Metric", "Before Cleaning", "After Cleaning", "Strategy / Action Taken"],
            ["Total Rows", str(shape_before[0]), str(shape_after[0]), f"Removed {shape_before[0] - shape_after[0]} duplicate records"],
            ["Missing Delivery Times", "2", str(df_clean['delivery_time_mins'].isnull().sum()), f"Imputed with median ({med_delivery:.1f} mins)"],
            ["Missing Order Values", "1", str(df_clean['order_value'].isnull().sum()), f"Imputed with median (${med_value:.2f})"],
            ["Missing Ratings", "1", str(df_clean['rating'].isnull().sum()), f"Imputed with rounded mean ({mean_rating:.1f})"],
            ["Missing Categories", "1", str(df_clean['category'].isnull().sum()), f"Imputed with mode ('{mode_category}')"],
            ["Order Value Outliers", str(outlier_count), "0 (Capped)", f"Capped upper outliers at ${upper_fence:.2f} using clip()"]
        ]
        print(tabulate(summary_table, headers="firstrow", tablefmt="grid"))

        self.cleaned_df = df_clean
        print("\n[SUCCESS] Cleaned DataFrame cached into memory successfully (Shape: {}).".format(self.cleaned_df.shape))

    # -------------------------------------------------------------
    # OPTION 2: RUN SQL ANALYSIS
    # -------------------------------------------------------------
    def option_run_sql_analysis(self):
        self.print_header("Option 2: Run SQL Database Analysis")
        conn = sqlite3.connect(DB_FILE)

        # Query 1: GROUP BY with aggregate functions (COUNT, SUM, AVG)
        print("\n[QUERY 1] Category Performance Summary (GROUP BY with COUNT, SUM, AVG):")
        query_group_by = """
        SELECT 
            r.category,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.order_value), 2) AS total_revenue,
            ROUND(AVG(o.order_value), 2) AS avg_order_value,
            ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_time,
            ROUND(AVG(o.rating), 2) AS avg_rating
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.category
        ORDER BY total_revenue DESC;
        """
        self.sql_summary_df = pd.read_sql_query(query_group_by, conn)
        print(tabulate(self.sql_summary_df, headers='keys', tablefmt='psql', showindex=False))

        # Query 2: JOIN between restaurants and orders with City Delivery Metrics
        print("\n" + "-" * 80)
        print("[QUERY 2] City Delivery Performance Analysis (JOIN restaurants and orders):")
        query_join = """
        SELECT 
            r.city,
            COUNT(DISTINCT r.restaurant_id) AS partner_restaurants,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.order_value), 2) AS total_revenue,
            ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_mins,
            ROUND(AVG(o.rating), 2) AS avg_customer_rating
        FROM restaurants r
        JOIN orders o ON r.restaurant_id = o.restaurant_id
        GROUP BY r.city
        ORDER BY total_revenue DESC;
        """
        self.sql_join_df = pd.read_sql_query(query_join, conn)
        print(tabulate(self.sql_join_df, headers='keys', tablefmt='psql', showindex=False))

        conn.close()
        print("\n[SUCCESS] SQL analysis executed successfully against SQLite database.")

    # -------------------------------------------------------------
    # OPTION 3: VIEW CHARTS
    # -------------------------------------------------------------
    def option_view_charts(self):
        self.print_header("Option 3: Generate Multi-Panel Visual Charts")
        if self.cleaned_df is None:
            print("[INFO] Cleaned dataset not in memory. Automatically running Option 1 first...")
            self.option_load_and_clean_data()

        conn = sqlite3.connect(DB_FILE)
        city_orders_df = pd.read_sql_query("""
            SELECT r.city, o.delivery_time_mins 
            FROM orders o JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        """, conn)
        conn.close()

        # Set style
        sns.set_theme(style="whitegrid", palette="muted")
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle("Food Delivery Analytics — Operational Insights", fontsize=15, fontweight='bold')

        # Chart 1: Seaborn countplot showing orders by category
        order_order = self.cleaned_df['category'].value_counts().index
        sns.countplot(
            data=self.cleaned_df,
            x='category',
            order=order_order,
            ax=axes[0],
            palette='crest',
            hue='category',
            legend=False
        )
        axes[0].set_title("Orders Count by Category (Cleaned Dataset)", fontsize=12, fontweight='bold', pad=10)
        axes[0].set_xlabel("Food Category", fontweight='bold')
        axes[0].set_ylabel("Order Volume", fontweight='bold')
        axes[0].tick_params(axis='x', rotation=20)
        for p in axes[0].patches:
            height = int(p.get_height())
            if height > 0:
                axes[0].annotate(f"{height}",
                                 (p.get_x() + p.get_width() / 2., height),
                                 ha='center', va='bottom', xytext=(0, 2),
                                 textcoords='offset points', fontweight='bold')

        # Chart 2: Seaborn barplot showing average delivery time by city
        city_order = city_orders_df.groupby('city')['delivery_time_mins'].mean().sort_values(ascending=False).index
        sns.barplot(
            data=city_orders_df,
            x='city',
            y='delivery_time_mins',
            order=city_order,
            ax=axes[1],
            palette='flare',
            errorbar=None,
            hue='city',
            legend=False
        )
        axes[1].set_title("Average Delivery Time by City (Minutes)", fontsize=12, fontweight='bold', pad=10)
        axes[1].set_xlabel("City", fontweight='bold')
        axes[1].set_ylabel("Avg Delivery Time (Mins)", fontweight='bold')
        for p in axes[1].patches:
            val = p.get_height()
            if val > 0:
                axes[1].annotate(f"{val:.1f}m",
                                 (p.get_x() + p.get_width() / 2., val),
                                 ha='center', va='bottom', xytext=(0, 2),
                                 textcoords='offset points', fontweight='bold')

        plt.tight_layout()
        plt.savefig(CHART_FILE, dpi=150, bbox_inches='tight')
        plt.close()

        print(f"\n[SUCCESS] Side-by-side charts successfully generated and saved to:")
        print(f"  * File Path: {os.path.abspath(CHART_FILE)}")
        print(f"  * Left Chart : Seaborn Countplot (Orders by Category)")
        print(f"  * Right Chart: Seaborn Barplot (Average Delivery Time by City)")

    # -------------------------------------------------------------
    # OPTION 4: EXPORT REPORT
    # -------------------------------------------------------------
    def option_export_report(self):
        self.print_header("Option 4: Export Multi-Sheet Excel Report")
        if self.cleaned_df is None:
            print("[INFO] Cleaned dataset not in memory. Automatically running Option 1 first...")
            self.option_load_and_clean_data()
        if self.sql_summary_df is None or self.sql_join_df is None:
            print("[INFO] SQL analysis results not in memory. Automatically running Option 2 first...")
            self.option_run_sql_analysis()

        # Export using pandas.ExcelWriter as separate sheets
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            self.cleaned_df.to_excel(writer, sheet_name='Cleaned_Orders_Data', index=False)
            self.sql_summary_df.to_excel(writer, sheet_name='Category_SQL_Analysis', index=False)
            self.sql_join_df.to_excel(writer, sheet_name='City_SQL_Analysis', index=False)

        abs_path = os.path.abspath(EXCEL_FILE)
        file_size_kb = os.path.getsize(EXCEL_FILE) / 1024

        print(f"\n[SUCCESS] Report exported successfully!")
        print(f"  * File Name    : {EXCEL_FILE}")
        print(f"  * Full Path    : {abs_path}")
        print(f"  * File Size    : {file_size_kb:.2f} KB")
        print(f"  * Sheets Saved :")
        print(f"      1. 'Cleaned_Orders_Data'    ({len(self.cleaned_df)} rows)")
        print(f"      2. 'Category_SQL_Analysis'  ({len(self.sql_summary_df)} rows)")
        print(f"      3. 'City_SQL_Analysis'      ({len(self.sql_join_df)} rows)")

    # -------------------------------------------------------------
    # CONSOLE LOOP MENU
    # -------------------------------------------------------------
    def run_menu(self):
        while True:
            print("\n" + "=" * 60)
            print("   FOOD DELIVERY ANALYTICS CONSOLE APPLICATION")
            print("=" * 60)
            print(" [1] Load & Clean Data")
            print(" [2] Run SQL Analysis")
            print(" [3] View Charts")
            print(" [4] Export Report")
            print(" [0] Exit")
            print("=" * 60)

            choice = input("Enter your option (0-4): ").strip()
            if choice == "1":
                self.option_load_and_clean_data()
            elif choice == "2":
                self.option_run_sql_analysis()
            elif choice == "3":
                self.option_view_charts()
            elif choice == "4":
                self.option_export_report()
            elif choice == "0":
                print("\nExiting Food Delivery Analytics Application. Goodbye!\n")
                break
            else:
                print("\n[INVALID INPUT] Please select a valid option from 0 to 4.")

def main():
    app = FoodDeliveryApp()
    # Check if run non-interactively or in demo mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print("Running in Automated End-to-End Demo Mode...\n")
        app.option_load_and_clean_data()
        app.option_run_sql_analysis()
        app.option_view_charts()
        app.option_export_report()
        print("\nAll capstone workflows completed successfully.")
    else:
        app.run_menu()

if __name__ == "__main__":
    main()
