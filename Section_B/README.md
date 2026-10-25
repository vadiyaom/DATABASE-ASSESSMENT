# Section B: Practical Coding Tasks
**Course:** Data Science (Modules 3–4: Data Collection, Cleaning & Visualization › Working with Databases)  
**Assessment Code:** M4-A1  

---

## Tasks Overview & Files

### Task 1: Daily Order Analysis with NumPy
* **Source Script:** [task1_daily_orders.py](file:///g:/Assessment_SQl/Section_B/task1_daily_orders.py)
* **Terminal Output Screenshot:** [Task1_Terminal_Output.png](file:///g:/Assessment_SQl/Section_B/screenshots/Task1_Terminal_Output.png)
* **Execution:** `python task1_daily_orders.py`
* **Summary:** Analyzes 30 days of daily order counts and revenue generated via `np.random.seed(42)`. Identifies peak surge days (> mean + 1.0 std dev) using boolean masks, and reshapes array into a 5×6 matrix to calculate weekly volume totals.

### Task 2: Food Delivery Orders Data Cleaning Pipeline
* **Source Script:** [task2_data_cleaning.py](file:///g:/Assessment_SQl/Section_B/task2_data_cleaning.py)
* **Terminal Output Screenshot:** [Task2_Terminal_Output.png](file:///g:/Assessment_SQl/Section_B/screenshots/Task2_Terminal_Output.png)
* **Execution:** `python task2_data_cleaning.py`
* **Summary:** Implements a complete Pandas cleaning pipeline. Handles missing numeric and categorical columns using medians, mean, and mode; drops duplicates; detects outliers via the 1.5×IQR fence method and caps them using `clip()`.

### Task 3: Food Delivery Visualisation Dashboard
* **Source Script:** [task3_visualisation_dashboard.py](file:///g:/Assessment_SQl/Section_B/task3_visualisation_dashboard.py)
* **Output Figure:** [food_delivery_dashboard.png](file:///g:/Assessment_SQl/Section_B/food_delivery_dashboard.png)
* **Terminal Output Screenshot:** [Task3_Terminal_Output.png](file:///g:/Assessment_SQl/Section_B/screenshots/Task3_Terminal_Output.png)
* **Execution:** `python task3_visualisation_dashboard.py`
* **Summary:** Renders a 2×2 multi-panel dashboard containing a Seaborn countplot, Seaborn boxplot, Matplotlib horizontal bar chart, and Seaborn correlation heatmap with annotations, saved at 150 DPI.

### Task 4: SQL + Python Restaurant Performance Report
* **Source Script:** [task4_sql_performance.py](file:///g:/Assessment_SQl/Section_B/task4_sql_performance.py)
* **SQL Query File:** [task4_queries.sql](file:///g:/Assessment_SQl/Section_B/task4_queries.sql)
* **Database File:** [food_delivery.db](file:///g:/Assessment_SQl/Section_B/food_delivery.db)
* **Exported CSV Report:** [restaurant_performance_report.csv](file:///g:/Assessment_SQl/Section_B/restaurant_performance_report.csv)
* **Terminal Output Screenshot:** [Task4_Terminal_Output.png](file:///g:/Assessment_SQl/Section_B/screenshots/Task4_Terminal_Output.png)
* **SQLite GUI Screenshot:** [Task4_SQLite_Query_Results.png](file:///g:/Assessment_SQl/Section_B/screenshots/Task4_SQLite_Query_Results.png)
* **Execution:** `python task4_sql_performance.py`
* **Summary:** Seeds a relational SQLite database with `restaurants` and `orders` tables. Queries aggregate performance with `COUNT()`, `SUM()`, `AVG()`, loads results into Pandas, ranks restaurants by revenue, displays top-5 rankings, and exports to CSV.
