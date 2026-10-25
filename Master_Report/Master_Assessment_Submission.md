# Comprehensive Assessment Submission: Data Science (M4-A1)
**Institution:** TOPS Technologies  
**Program:** Data Science  
**Assessment Code:** M4-A1  
**Modules:** Modules 3–4: Data Collection, Cleaning & Visualization › Working with Databases  
**Stack:** Python 3 / SQL (SQLite) / Pandas / NumPy / Matplotlib / Seaborn  
**Submission Scope:** All Sections Attempted (Section A, Section B, Section C, Section D)  

---

## Table of Contents
1. [General Instructions & Compliance Overview](#general-instructions--compliance-overview)
2. [Section A — Concept Application](#section-a--concept-application)
   - [Scenario 1 (S1): Missing Data Strategy & Type Casting in Pandas](#scenario-1-s1-missing-data-strategy--type-casting-in-pandas)
   - [Scenario 2 (S2): NumPy Vectorization & Boolean Indexing](#scenario-2-s2-numpy-vectorization--boolean-indexing)
   - [Scenario 3 (S3): EDA & Seaborn Visualization Strategy](#scenario-3-s3-eda--seaborn-visualization-strategy)
   - [Scenario 4 (S4): Relational Database Joins & Data Completeness](#scenario-4-s4-relational-database-joins--data-completeness)
   - [Scenario 5 (S5): Advanced SQL Window Functions vs. Aggregations](#scenario-5-s5-advanced-sql-window-functions-vs-aggregations)
   - [Scenario 6 (S6): CTEs (WITH Clause) vs. Deeply Nested Subqueries](#scenario-6-s6-ctes-with-clause-vs-deeply-nested-subqueries)
3. [Section B — Practical Coding Tasks](#section-b--practical-coding-tasks)
   - [Task 1: Daily Order Analysis with NumPy](#task-1-daily-order-analysis-with-numpy)
   - [Task 2: Food Delivery Orders Data Cleaning Pipeline](#task-2-food-delivery-orders-data-cleaning-pipeline)
   - [Task 3: Food Delivery Visualisation Dashboard](#task-3-food-delivery-visualisation-dashboard)
   - [Task 4: SQL + Python Restaurant Performance Report](#task-4-sql--python-restaurant-performance-report)
4. [Section C — Mini Capstone Project: Console Application](#section-c--mini-capstone-project-console-application)
   - [Application Architecture & Menu Flow](#application-architecture--menu-flow)
   - [Console Execution & Output Screenshots](#console-execution--output-screenshots)
   - [Multi-Sheet Excel Report Export](#multi-sheet-excel-report-export)
5. [Section D — AI-Augmented Learning & Debugging](#section-d--ai-augmented-learning--debugging)
   - [Item 1: The Exact Prompt Given to AI](#item-1-the-exact-prompt-given-to-ai)
   - [Item 2: AI's Original Code vs. Corrected Production Version](#item-2-ais-original-code-vs-corrected-production-version)
   - [Item 3: Explanatory Debugging Note (3–4 Lines)](#item-3-explanatory-debugging-note-34-lines)
   - [Execution Output & Generated Chart](#execution-output--generated-chart)
6. [Repository Structure & Verification Index](#repository-structure--verification-index)

---

## General Instructions & Compliance Overview

> **Instructions from Assessment Specification:**  
> *"Attempt all sections. For Python tasks, write your code in Python 3 and submit your .py source file along with a screenshot of your program output. For SQL tasks, submit your .sql file or a screenshot of query results from your database tool. Label every task clearly with its section and task number. All work must be your own."*

### Deliverables Checklist
- [x] **Section A:** Thorough conceptual and architectural solutions for Scenarios S1–S6 ([Section_A_Concept_Application.md](file:///g:/Assessment_SQl/Section_A_Concept_Application.md)).
- [x] **Section B (Task 1):** NumPy order and revenue analysis script ([task1_daily_orders.py](file:///g:/Assessment_SQl/task1_daily_orders.py)) + output screenshot.
- [x] **Section B (Task 2):** Pandas data cleaning pipeline ([task2_data_cleaning.py](file:///g:/Assessment_SQl/task2_data_cleaning.py)) + output screenshot.
- [x] **Section B (Task 3):** Matplotlib & Seaborn multi-panel dashboard script ([task3_visualisation_dashboard.py](file:///g:/Assessment_SQl/task3_visualisation_dashboard.py)) + high-res figure ([food_delivery_dashboard.png](file:///g:/Assessment_SQl/food_delivery_dashboard.png)).
- [x] **Section B (Task 4):** SQLite + Pandas performance report script ([task4_sql_performance.py](file:///g:/Assessment_SQl/task4_sql_performance.py)) + SQL source file ([task4_queries.sql](file:///g:/Assessment_SQl/task4_queries.sql)) + CSV report ([restaurant_performance_report.csv](file:///g:/Assessment_SQl/restaurant_performance_report.csv)) + DB Browser for SQLite query screenshot.
- [x] **Section C (Mini Capstone):** Interactive menu-driven console app ([section_c_mini_capstone.py](file:///g:/Assessment_SQl/section_c_mini_capstone.py)) + SQL queries file ([section_c_queries.sql](file:///g:/Assessment_SQl/section_c_queries.sql)) + multi-sheet Excel file ([food_delivery_report.xlsx](file:///g:/Assessment_SQl/food_delivery_report.xlsx)) + visualization ([capstone_charts.png](file:///g:/Assessment_SQl/capstone_charts.png)).
- [x] **Section D (AI-Augmented Learning):** Complete submission document ([Section_D_AI_Submission.md](file:///g:/Assessment_SQl/Section_D_AI_Submission.md)) + runnable script ([section_d_ai_learning.py](file:///g:/Assessment_SQl/section_d_ai_learning.py)) + horizontal bar plot ([section_d_top3_chart.png](file:///g:/Assessment_SQl/section_d_top3_chart.png)).
- [x] **Screenshots:** All genuine Windows Terminal outputs and SQLite database GUI query result screenshots created in [screenshots/](file:///g:/Assessment_SQl/screenshots/).

---

## Section A — Concept Application

### Scenario 1 (S1): Missing Data Strategy & Type Casting in Pandas
* **Scenario:** 50,000 order records; `delivery_time_mins` has 14% missing values; `customer_rating` contains string entries (e.g. `'4.5'`) instead of `float64`.
* **Strategy Selection (Dropping vs. Imputation):**
  - **Dropping rows** would discard $0.14 \times 50,000 = 7,000$ records. In industry data science, listwise deletion is only acceptable when missing data is $< 3\%\text{--}5\%$ and strictly Missing Completely at Random (MCAR). Dropping 7,000 orders creates heavy survivorship bias and destroys statistical sample size.
  - **Mean vs. Median:** Delivery durations in food logistics are inherently **right-skewed (positively skewed)** due to traffic jams, bad weather, and peak kitchen bottlenecks. The arithmetic mean is disproportionately inflated by long-tail outliers. The **median (50th percentile)** is robust and represents the typical delivery time. Therefore, **median imputation** is chosen.
* **Exact Pandas Code to Cast `customer_rating`:**
  ```python
  import pandas as pd
  # 1. Strip whitespace
  df['customer_rating'] = df['customer_rating'].astype(str).str.strip()
  # 2. Coerce invalid values to NaN safely
  df['customer_rating'] = pd.to_numeric(df['customer_rating'], errors='coerce')
  # 3. Impute missing ratings with rounded mean rating
  df['customer_rating'] = df['customer_rating'].fillna(round(df['customer_rating'].mean(), 1))
  ```

---

### Scenario 2 (S2): NumPy Vectorization & Boolean Indexing
* **Scenario:** NumPy array of 30 days of daily order counts. Flag 'surge days' (order count > mean + 1.5 standard deviations) and calculate total revenue for surge days without using a loop.
* **How Functions Work Together:**
  ```python
  # Vectorized threshold calculation
  surge_threshold = np.mean(orders) + 1.5 * np.std(orders)
  # Boolean mask creation (broadcasting comparison across contiguous memory)
  surge_mask = orders > surge_threshold
  # Vectorized filtering and aggregation
  total_surge_revenue = np.sum(revenue[surge_mask])
  ```
* **What a Boolean Mask Is:** An array of boolean values (`True`/`False`) matching the shape of the source array. When indexed (`array[mask]`), it selectively yields elements where the condition holds `True`.
* **Why Vectorization Outperforms Loops:**
  1. Contiguous memory storage of homogeneous C data types eliminates dynamic typing and `PyObject` dereferencing.
  2. Avoids Python bytecode loop execution overhead.
  3. Utilizes CPU L1/L2 cache prefetching and **SIMD (Single Instruction Multiple Data)** vector registers (AVX2/AVX-512) to evaluate multiple items in parallel per CPU clock cycle (yielding a 50x–100x speedup).

---

### Scenario 3 (S3): EDA & Seaborn Visualization Strategy
* **Question (a): Delivery Time vs. Customer Rating**
  - **Type:** Bivariate Analysis (two continuous quantitative variables).
  - **Recommended Chart:** `sns.scatterplot()` or `sns.regplot()` with trendline.
  - **Why not a line plot:** Line plots sequentially connect adjacent points, falsely implying temporal continuity. For cross-sectional order records, a line plot produces an unreadable "zigzag spiderweb". A scatter plot reveals clustering, non-linear inflection thresholds (e.g., rating drops after 45 mins), and correlation strength.
* **Question (b): Average Order Value across Restaurant Categories**
  - **Type:** Bivariate Analysis (one discrete nominal category + one continuous numerical variable).
  - **Recommended Chart:** `sns.boxplot()` or `sns.violinplot()`.
  - **Why not a line plot:** Restaurant categories have no natural ordering. Drawing lines across discrete categories is mathematically invalid. A boxplot provides the complete five-number summary (Q1, median, Q3, whiskers, and outlier points), exposing spread and skewness across cuisines.

---

### Scenario 4 (S4): Relational Database Joins & Data Completeness
* **Scenario:** Report showing every restaurant's name and total revenue, including restaurants that have not yet received any orders.
* **Required Join:** **`LEFT OUTER JOIN`** (with `restaurants` as the left table):
  ```sql
  SELECT 
      r.restaurant_id, r.name,
      COUNT(o.order_id) AS total_orders,
      COALESCE(SUM(o.order_value), 0.0) AS total_revenue
  FROM restaurants r
  LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
  GROUP BY r.restaurant_id, r.name;
  ```
* **Consequence of `INNER JOIN`:** An inner join requires matches in both tables. Restaurants with 0 orders would be **completely excluded**, masking partner acquisition performance.
* **Handling Unmatched Rows:** A `LEFT JOIN` preserves all left-table rows; unmatched right attributes become `NULL`. Wrapping with `COALESCE(SUM(o.order_value), 0.0)` guarantees clean $0.00$ revenue outputs.

---

### Scenario 5 (S5): Advanced SQL Window Functions vs. Aggregations
* **Scenario:** Rank delivery agents within each city by completed deliveries and compare each agent's count to the agent ranked directly above them.
* **The Two Window Functions:**
  1. Ranking: `DENSE_RANK() OVER (PARTITION BY city ORDER BY completed_deliveries DESC) AS city_rank`
  2. Prior Value: `LAG(completed_deliveries, 1) OVER (PARTITION BY city ORDER BY completed_deliveries DESC) AS agent_above_deliveries`
* **Why Window Functions are Superior to `GROUP BY` + Self-Joins:**
  - `GROUP BY` collapses rows; window functions maintain row-level granularity while computing partition statistics.
  - Window functions operate in a single sorted streaming pass ($O(N \log N)$), whereas self-joins or correlated subqueries trigger quadratic table scans ($O(N^2)$).
  - Handles ties and gaps deterministically without duplicating rows.

---

### Scenario 6 (S6): CTEs (WITH Clause) vs. Deeply Nested Subqueries
* **Scenario:** Two-step report: identify top 5 restaurant categories by order volume, then retrieve full order details for those categories.
* **Evaluation Matrix:**
  - **Readability:** CTEs read top-to-bottom in modular steps (`WITH TopCategories AS (...) SELECT ...`). Nested subqueries nest inside-out inside the `WHERE` clause ("pyramid of doom").
  - **Reusability:** A CTE can be joined multiple times in the outer query. A `WHERE` subquery cannot be reused without duplicating code.
  - **Debuggability:** A developer can inspect intermediate CTE results in isolation (`SELECT * FROM TopCategories;`).
* **When to Prefer Nested Subqueries:**
  - Lightweight scalar lookups (e.g., `WHERE order_value > (SELECT AVG(order_value) FROM orders)`).
  - Running on legacy SQL engines (e.g. MySQL < 8.0 or older SQLite versions) lacking CTE syntax support.

---

## Section B — Practical Coding Tasks

### Task 1: Daily Order Analysis with NumPy
* **Source Code:** [task1_daily_orders.py](file:///g:/Assessment_SQl/task1_daily_orders.py)
* **Key Implementation Details:**
  - Seed: `np.random.seed(42)`
  - Daily orders: `np.random.randint(100, 801, size=30)`
  - Daily revenue: `np.random.uniform(5000.0, 50000.0, size=30)`
  - Peak threshold: `mean + 1.0 * std`
  - Reshaping: `daily_orders.reshape(5, 6)` and `np.sum(axis=1)`
* **Execution Results:**
  - Total Orders: **12,279** | Total Revenue: **$743,362.93**
  - Mean Orders: **409.30** | Std Dev: **195.90**
  - Peak Day: Day 10 ($49,245.39)
  - Peak Days Count: **4 days** | Peak Revenue: **$127,639.11** (17.17% of total)

#### Task 1 Terminal Output Screenshot:
![Task 1 Terminal Output](file:///g:/Assessment_SQl/screenshots/Task1_Terminal_Output.png)

---

### Task 2: Food Delivery Orders Data Cleaning Pipeline
* **Source Code:** [task2_data_cleaning.py](file:///g:/Assessment_SQl/task2_data_cleaning.py)
* **Key Implementation Details:**
  - Simulated dataset with 23 initial rows, 4 missing values, 3 duplicate rows, and extreme outliers.
  - Imputation: `delivery_time_mins` (median 35.0), `order_value` (median $645.00), `rating` (mean 4.4), `category` (mode 'North Indian').
  - Deduplication: `drop_duplicates()` reduced rows from 23 to 20.
  - IQR Outlier Detection: $Q1 = \$335.00, Q3 = \$860.00, IQR = \$525.00, \text{Upper Fence} = \$1647.50$.
  - Capping: Applied `df['order_value'].clip(upper=1647.50)` capping Order #1009 ($2800 -> $1647.50) and Order #1015 ($3500 -> $1647.50).

#### Task 2 Terminal Output Screenshot:
![Task 2 Terminal Output](file:///g:/Assessment_SQl/screenshots/Task2_Terminal_Output.png)

---

### Task 3: Food Delivery Visualisation Dashboard
* **Source Code:** [task3_visualisation_dashboard.py](file:///g:/Assessment_SQl/task3_visualisation_dashboard.py)
* **Output Image File:** [food_delivery_dashboard.png](file:///g:/Assessment_SQl/food_delivery_dashboard.png)
* **Subplots Configured:**
  1. `axes[0, 0]`: Seaborn `countplot` showing order volume by cuisine category with exact count badges.
  2. `axes[0, 1]`: Seaborn `boxplot` showing delivery duration distribution by category.
  3. `axes[1, 0]`: Matplotlib `barh` horizontal bar chart showing average order value per restaurant.
  4. `axes[1, 1]`: Seaborn `heatmap` of numeric correlation matrix with `annot=True`.
  - Saved with `dpi=150` and `bbox_inches='tight'`.

#### Task 3 Terminal Output Screenshot:
![Task 3 Terminal Output](file:///g:/Assessment_SQl/screenshots/Task3_Terminal_Output.png)

#### Generated Dashboard Figure:
![Food Delivery Dashboard](file:///g:/Assessment_SQl/food_delivery_dashboard.png)

---

### Task 4: SQL + Python Restaurant Performance Report
* **Source Code:** [task4_sql_performance.py](file:///g:/Assessment_SQl/task4_sql_performance.py)
* **SQL Query File:** [task4_queries.sql](file:///g:/Assessment_SQl/task4_queries.sql)
* **Database Created:** [food_delivery.db](file:///g:/Assessment_SQl/food_delivery.db)
* **Exported Report:** [restaurant_performance_report.csv](file:///g:/Assessment_SQl/restaurant_performance_report.csv)
* **Key Implementation Details:**
  - Created tables `restaurants` (10 rows) and `orders` (28 rows) in SQLite.
  - Executed analytical aggregation query via `pd.read_sql_query()`.
  - Added ranking: `df['revenue_rank'] = df['total_revenue'].rank(ascending=False, method='min').astype(int)`.
  - Exported complete table to CSV.

#### Task 4 Terminal Output Screenshot:
![Task 4 Terminal Output](file:///g:/Assessment_SQl/screenshots/Task4_Terminal_Output.png)

#### Task 4 SQLite DB Browser Query Results Screenshot:
![Task 4 SQLite Query Results](file:///g:/Assessment_SQl/screenshots/Task4_SQLite_Query_Results.png)

---

## Section C — Mini Capstone Project: Console Application

### Application Architecture & Menu Flow
* **Source Code:** [section_c_mini_capstone.py](file:///g:/Assessment_SQl/section_c_mini_capstone.py)
* **SQL Queries File:** [section_c_queries.sql](file:///g:/Assessment_SQl/section_c_queries.sql)
* **Generated Excel File:** [food_delivery_report.xlsx](file:///g:/Assessment_SQl/food_delivery_report.xlsx)
* **Generated Charts:** [capstone_charts.png](file:///g:/Assessment_SQl/capstone_charts.png)

The application provides an interactive menu loop with 5 distinct options:
- `[1] Load & Clean Data`: Loads raw simulated DataFrame, handles missing values (median/mean/mode), removes duplicates, detects/caps outliers, and prints a comprehensive data quality summary table.
- `[2] Run SQL Analysis`: Connects to SQLite database and runs two analytical queries (`GROUP BY` category aggregation and `JOIN` city delivery performance).
- `[3] View Charts`: Generates side-by-side Seaborn charts (order counts by category and delivery times by city).
- `[4] Export Report`: Exports cleaned data and SQL query results into a multi-sheet Excel file via `pandas.ExcelWriter`.
- `[0] Exit`: Safely closes application.

#### Option 1 (Load & Clean Data) Terminal Screenshot:
![Section C Option 1 Screenshot](file:///g:/Assessment_SQl/screenshots/SectionC_Menu_Option1_CleanData.png)

#### Option 2 (Run SQL Analysis) Terminal Screenshot:
![Section C Option 2 Screenshot](file:///g:/Assessment_SQl/screenshots/SectionC_Menu_Option2_SQLAnalysis.png)

#### Options 3 & 4 (Charts & Excel Export) Terminal Screenshot:
![Section C Option 3 and 4 Screenshot](file:///g:/Assessment_SQl/screenshots/SectionC_Menu_Option3_Charts.png)

#### Generated Capstone Visual Charts:
![Capstone Charts](file:///g:/Assessment_SQl/capstone_charts.png)

---

## Section D — AI-Augmented Learning & Debugging

* **Submission Document:** [Section_D_AI_Submission.md](file:///g:/Assessment_SQl/Section_D_AI_Submission.md)
* **Executable Script:** [section_d_ai_learning.py](file:///g:/Assessment_SQl/section_d_ai_learning.py)
* **Generated Chart:** [section_d_top3_chart.png](file:///g:/Assessment_SQl/section_d_top3_chart.png)

### Item 1: The Exact Prompt Given to AI
```text
Write a complete Python program that performs the following tasks:
1. Connects to a SQLite database ('food_delivery.db') containing an 'orders' table (joined with 'restaurants') and queries it to find the top 3 restaurants by average customer rating, filtering out any restaurant with fewer than 5 orders.
2. Loads the SQL query result into a Pandas DataFrame and calculates each restaurant's revenue share as a percentage of the total revenue across these top 3 restaurants combined.
3. Plots a clean horizontal bar chart of the top 3 restaurants by average rating, displaying the calculated revenue share percentage as a bar label on each bar.
4. Robustly handles edge cases where the database file does not exist or the query returns no matching rows, printing a clear, user-friendly error message rather than crashing.
```

### Item 2: AI's Original Code vs. Corrected Production Version
The AI's initial solution contained critical flaws:
1. **Fatal Syntax Error:** Placed `HAVING` before `GROUP BY`, triggering `sqlite3.OperationalError: near "GROUP": syntax error`.
2. **Missing Failure Guards:** No file check for database existence; failed with uncaught exceptions if `food_delivery.db` was missing.
3. **Empty Data Crash:** Did not verify if the returned DataFrame was empty before attempting percentage calculations and matplotlib plotting.
4. **Unformatted Visualization:** Plotted unlabelled axes with no data callouts.

The corrected script in [section_d_ai_learning.py](file:///g:/Assessment_SQl/section_d_ai_learning.py) fixed all syntax bugs, added input validation guards, enforced float division safety, and rendered an annotated horizontal bar chart.

### Item 3: Explanatory Debugging Note (3–4 Lines)
> The AI's original code failed with a fatal SQLite syntax error because it placed the `HAVING` clause before `GROUP BY`, which violates standard SQL grammar. Additionally, it lacked database file existence checks and empty-result handling, causing uncaught exceptions when querying or plotting empty tables. I reordered the SQL clauses, wrapped the database connection with validation guards, enforced float division safety, and added descriptive axis labels, titles, and bar percentage callouts to create a robust, production-grade script.

#### Section D Terminal Debugging Screenshot:
![Section D Terminal Output](file:///g:/Assessment_SQl/screenshots/SectionD_Terminal_Output.png)

#### Section D Generated Top 3 Rating & Revenue Share Chart:
![Section D Top 3 Chart](file:///g:/Assessment_SQl/section_d_top3_chart.png)

---

## Repository Structure & Verification Index

```text
G:\Assessment_SQl\
├── Master_Assessment_Submission.md        <-- Master documentation file
│
├── Section_A\                             <-- SECTION A: CONCEPT APPLICATION
│   ├── README.md                          <-- Section A overview
│   └── Section_A_Concept_Application.md   <-- Detailed Q1-Q6 theoretical responses
│
├── Section_B\                             <-- SECTION B: PRACTICAL CODING TASKS
│   ├── README.md                          <-- Section B tasks overview
│   ├── task1_daily_orders.py              <-- Task 1: NumPy order & revenue analysis
│   ├── task2_data_cleaning.py             <-- Task 2: Pandas data cleaning pipeline
│   ├── task3_visualisation_dashboard.py   <-- Task 3: 2x2 visualization dashboard
│   ├── food_delivery_dashboard.png        <-- Task 3: Generated 2x2 dashboard figure
│   ├── task4_sql_performance.py           <-- Task 4: SQL + Python performance report
│   ├── task4_queries.sql                  <-- Task 4: Relational SQL script (DDL & DML)
│   ├── food_delivery.db                   <-- Task 4: SQLite database (10 restaurants, 28 orders)
│   ├── restaurant_performance_report.csv  <-- Task 4: Exported ranked CSV report
│   └── screenshots\                       <-- Task 1 to 4 authentic output screenshots
│       ├── Task1_Terminal_Output.png
│       ├── Task2_Terminal_Output.png
│       ├── Task3_Terminal_Output.png
│       ├── Task3_food_delivery_dashboard.png
│       ├── Task4_Terminal_Output.png
│       └── Task4_SQLite_Query_Results.png
│
├── Section_C\                             <-- SECTION C: MINI CAPSTONE PROJECT
│   ├── README.md                          <-- Capstone application guide
│   ├── section_c_mini_capstone.py         <-- Interactive 5-option console application
│   ├── section_c_queries.sql              <-- SQL queries (aggregates & joins)
│   ├── food_delivery.db                   <-- SQLite database
│   ├── capstone_charts.png                <-- Option 3: Generated side-by-side charts
│   ├── food_delivery_report.xlsx          <-- Option 4: 3-sheet Excel workbook export
│   └── screenshots\                       <-- Menu options output screenshots
│       ├── SectionC_Menu_Option1_CleanData.png
│       ├── SectionC_Menu_Option2_SQLAnalysis.png
│       ├── SectionC_Menu_Option3_Charts.png
│       └── SectionC_Menu_Option4_ExcelExport.png
│
├── Section_D\                             <-- SECTION D: AI-AUGMENTED LEARNING
│   ├── README.md                          <-- AI workflow documentation
│   ├── Section_D_AI_Submission.md         <-- Exact prompt, original code, debugged code & note
│   ├── section_d_ai_learning.py           <-- Executable comparison & debugged script
│   ├── food_delivery.db                   <-- SQLite database
│   ├── section_d_top3_chart.png           <-- Generated Top 3 horizontal bar chart
│   └── screenshots\                       <-- Debugging session screenshots
│       ├── SectionD_Terminal_Output.png
│       └── SectionD_Top3_Rating_Chart.png
│
└── screenshots\                           <-- Master screenshots repository
    ├── Task1_Terminal_Output.png
    ├── Task2_Terminal_Output.png
    ├── Task3_Terminal_Output.png
    ├── Task3_food_delivery_dashboard.png
    ├── Task4_Terminal_Output.png
    ├── Task4_SQLite_Query_Results.png
    ├── SectionC_Menu_Option1_CleanData.png
    ├── SectionC_Menu_Option2_SQLAnalysis.png
    ├── SectionC_Menu_Option3_Charts.png
    ├── SectionC_Menu_Option4_ExcelExport.png
    ├── SectionD_Terminal_Output.png
    └── SectionD_Top3_Rating_Chart.png
```

---
*Assessment submission files prepared and verified under Python 3.14.6 / SQLite 3.*
