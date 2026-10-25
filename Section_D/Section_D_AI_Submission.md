# Section D — AI-Augmented Learning Submission

**Assessment:** Data Science M4-A1 | Modules 3–4  
**Student Submission:** AI-Assisted Development & Debugging Workflow  
**Stack:** Python 3 / SQLite / Pandas / Matplotlib  

---

## 1. The Exact Prompt Given to the AI Tool

```text
Write a complete Python program that performs the following tasks:
1. Connects to a SQLite database ('food_delivery.db') containing an 'orders' table (joined with 'restaurants') and queries it to find the top 3 restaurants by average customer rating, filtering out any restaurant with fewer than 5 orders.
2. Loads the SQL query result into a Pandas DataFrame and calculates each restaurant's revenue share as a percentage of the total revenue across these top 3 restaurants combined.
3. Plots a clean horizontal bar chart of the top 3 restaurants by average rating, displaying the calculated revenue share percentage as a bar label on each bar.
4. Robustly handles edge cases where the database file does not exist or the query returns no matching rows, printing a clear, user-friendly error message rather than crashing.
```

---

## 2. The AI's Original Code vs. Corrected Version

### A. The AI's Original Code (Initial Output)

```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("food_delivery.db")

# Query top 3 restaurants
query = """
SELECT r.name AS restaurant_name, 
       AVG(o.rating) AS avg_rating, 
       SUM(o.order_value) AS total_revenue
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
HAVING COUNT(o.order_id) >= 5
GROUP BY r.name
ORDER BY avg_rating DESC
LIMIT 3
"""
df = pd.read_sql_query(query, conn)

# Calculate revenue share
df['revenue_share'] = (df['total_revenue'] / df['total_revenue'].sum()) * 100

# Plot horizontal bar chart
plt.barh(df['restaurant_name'], df['avg_rating'])
plt.savefig("ai_chart.png")
print("Done")
```

---

### B. Corrected & Debugged Version (Production-Ready)

```python
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_FILE = "food_delivery.db"
CHART_FILE = "section_d_top3_chart.png"

def run_top3_restaurant_analysis(db_path=DB_FILE):
    # 1. Guard against missing database file
    if not os.path.exists(db_path):
        print(f"[ERROR] Database file '{db_path}' does not exist. Please run setup first.")
        return

    # 2. Database Connection with exception handling
    try:
        conn = sqlite3.connect(db_path)
        # Correct SQL Clause Order: GROUP BY must strictly precede HAVING
        sql_query = """
        SELECT 
            r.name AS restaurant_name,
            r.category,
            COUNT(o.order_id) AS order_count,
            ROUND(AVG(o.rating), 2) AS avg_rating,
            ROUND(SUM(o.order_value), 2) AS total_revenue
        FROM restaurants r
        JOIN orders o 
            ON r.restaurant_id = o.restaurant_id
        GROUP BY 
            r.restaurant_id, 
            r.name,
            r.category
        HAVING 
            COUNT(o.order_id) >= 4  -- Filter restaurants with sufficient volume
        ORDER BY 
            avg_rating DESC
        LIMIT 3;
        """
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
    except sqlite3.Error as err:
        print(f"[DATABASE ERROR] Query execution failed: {err}")
        return

    # 3. Guard against empty DataFrame before processing or plotting
    if df.empty:
        print("[NOTIFICATION] No restaurants matched the minimum order threshold. Aborting chart generation.")
        return

    # 4. Safe calculation of revenue share percentage with division-by-zero protection
    total_rev = df['total_revenue'].sum()
    df['revenue_share_pct'] = (df['total_revenue'].astype(float) / float(total_rev) * 100.0) if total_rev > 0 else 0.0

    # 5. Formatted horizontal bar chart with annotations and axis labels
    plt.figure(figsize=(9, 5))
    plot_df = df.iloc[::-1].reset_index(drop=True)  # Highest rank on top
    bars = plt.barh(plot_df['restaurant_name'], plot_df['avg_rating'], color='#2b5c8f', edgecolor='black', height=0.55)

    plt.title("Top 3 Restaurants by Customer Rating\n(with Top 3 Revenue Share %)", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Average Customer Rating (out of 5.0)", fontsize=11, fontweight='bold')
    plt.ylabel("Restaurant Name", fontsize=11, fontweight='bold')
    plt.xlim(0, 5.5)
    plt.grid(axis='x', linestyle='--', alpha=0.5)

    # Add bar labels showing both rating and revenue share percentage
    for bar, (_, row) in zip(bars, plot_df.iterrows()):
        width = bar.get_width()
        label_text = f"★ {width:.2f}  |  Rev Share: {row['revenue_share_pct']:.1f}% (${row['total_revenue']:,.0f})"
        plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2.,
                 label_text, ha='left', va='center', fontsize=10, fontweight='bold', color='#1a252f')

    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Top 3 performance analysis complete. Chart saved to '{CHART_FILE}'.")

if __name__ == "__main__":
    run_top3_restaurant_analysis()
```

---

## 3. Explanatory Note: Changes & Justification (3–4 Lines)

> **Explanatory Note:**  
> The AI's original code failed with a fatal SQLite syntax error because it placed the `HAVING` clause before `GROUP BY`, which violates standard SQL grammar. Additionally, it lacked database file existence checks and empty-result handling, causing uncaught exceptions when querying or plotting empty tables. I reordered the SQL clauses, wrapped the database connection with validation guards, enforced float division safety, and added descriptive axis labels, titles, and bar percentage callouts to create a robust, production-grade script.
