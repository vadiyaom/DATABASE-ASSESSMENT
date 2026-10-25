# Section C: Mini Capstone Project
**Project:** Food Delivery Analytics Console Application  
**Assessment Code:** M4-A1 | Modules 3–4  

---

## Application Overview
A console-based food delivery analytics application integrating data cleaning (Module 3), SQL database operations (Module 4), and data visualization (Module 3) into an interactive menu-driven interface.

### Menu Options
1. **Option 1: Load & Clean Data** — Simulates raw order data, handles missing values via median/mean/mode imputation, removes duplicates, caps outliers via IQR, and prints a before-and-after data quality table.
2. **Option 2: Run SQL Analysis** — Connects to SQLite and executes:
   - Category performance summary using `GROUP BY` with `COUNT`, `SUM`, and `AVG`.
   - City delivery performance analysis using `INNER JOIN` between restaurants and orders.
3. **Option 3: View Charts** — Renders two side-by-side Seaborn charts (orders by cuisine and average delivery duration by city) saved to `capstone_charts.png`.
4. **Option 4: Export Report** — Exports cleaned order records and SQL query results into 3 distinct worksheets within a single Excel workbook (`food_delivery_report.xlsx`) using `pandas.ExcelWriter`.
0. **Option 0: Exit** — Safely exits the console loop.

---

## Deliverables & Files
* **Source Script:** [section_c_mini_capstone.py](file:///g:/Assessment_SQl/Section_C/section_c_mini_capstone.py)
* **SQL Query File:** [section_c_queries.sql](file:///g:/Assessment_SQl/Section_C/section_c_queries.sql)
* **Generated Excel Workbook:** [food_delivery_report.xlsx](file:///g:/Assessment_SQl/Section_C/food_delivery_report.xlsx)
* **Generated Visualization:** [capstone_charts.png](file:///g:/Assessment_SQl/Section_C/capstone_charts.png)
* **Database File:** [food_delivery.db](file:///g:/Assessment_SQl/Section_C/food_delivery.db)
* **Terminal Screenshots:**
  - [SectionC_Menu_Option1_CleanData.png](file:///g:/Assessment_SQl/Section_C/screenshots/SectionC_Menu_Option1_CleanData.png)
  - [SectionC_Menu_Option2_SQLAnalysis.png](file:///g:/Assessment_SQl/Section_C/screenshots/SectionC_Menu_Option2_SQLAnalysis.png)
  - [SectionC_Menu_Option3_Charts.png](file:///g:/Assessment_SQl/Section_C/screenshots/SectionC_Menu_Option3_Charts.png)
  - [SectionC_Menu_Option4_ExcelExport.png](file:///g:/Assessment_SQl/Section_C/screenshots/SectionC_Menu_Option4_ExcelExport.png)

## Execution Instructions
* **Interactive Menu Mode:**
  ```powershell
  python section_c_mini_capstone.py
  ```
* **Automated Demonstration Mode:**
  ```powershell
  python section_c_mini_capstone.py --demo
  ```
