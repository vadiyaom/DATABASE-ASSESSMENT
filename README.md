# DATABASE-ASSESSMENT: Data Science (Modules 3–4)
**Assessment Code:** M4-A1  
**Program:** Data Science  
**Institution:** TOPS Technologies  
**Stack:** Python 3 / SQL (SQLite) / Pandas / NumPy / Matplotlib / Seaborn  

---

## 📂 Repository Structure & Sections

### 1. [Section A: Concept Application](./Section_A/)
* Detailed theoretical solutions and code snippets for Scenarios S1 through S6:
  - **S1:** Missing value handling (median imputation vs data loss of dropping 14%) & `customer_rating` data type conversion.
  - **S2:** NumPy vectorization & boolean indexing (`np.mean`, `np.std`, boolean mask, and SIMD CPU execution advantages).
  - **S3:** Exploratory Data Analysis (bivariate correlation with scatter/regplot; categorical distribution with boxplots).
  - **S4:** Relational database joins (`LEFT JOIN` necessity for zero-order partners vs `INNER JOIN` data loss; `COALESCE` handling).
  - **S5:** SQL Window functions (`DENSE_RANK()` and `LAG()` with `PARTITION BY` vs slow $O(N^2)$ `GROUP BY` self-joins).
  - **S6:** CTEs (`WITH` clause) vs nested subqueries in `WHERE` (readability, reusability, debuggability trade-offs).
* [Section_A_Concept_Application.md](./Section_A/Section_A_Concept_Application.md)

---

### 2. [Section B: Practical Coding Tasks](./Section_B/)
* **Task 1: Daily Order Analysis with NumPy** — `task1_daily_orders.py`
* **Task 2: Food Delivery Orders Data Cleaning Pipeline** — `task2_data_cleaning.py`
* **Task 3: Food Delivery Visualisation Dashboard** — `task3_visualisation_dashboard.py` (saves `food_delivery_dashboard.png`)
* **Task 4: SQL + Python Restaurant Performance Report** — `task4_sql_performance.py` & `task4_queries.sql` (exports `restaurant_performance_report.csv`)
* Includes real terminal and database viewer screenshots in [`Section_B/screenshots/`](./Section_B/screenshots/).

---

### 3. [Section C: Mini Capstone Project](./Section_C/)
* **Food Delivery Analytics Console Application** (`section_c_mini_capstone.py`)
  - `(1) Load & Clean Data` (prints before/after summary)
  - `(2) Run SQL Analysis` (executes category `GROUP BY` and city delivery `JOIN` queries)
  - `(3) View Charts` (generates side-by-side charts saved to `capstone_charts.png`)
  - `(4) Export Report` (exports 3 sheets into `food_delivery_report.xlsx` via `pandas.ExcelWriter`)
  - `(0) Exit`
* SQL queries file: `section_c_queries.sql`
* Database file: `food_delivery.db`
* Screenshots in [`Section_C/screenshots/`](./Section_C/screenshots/).

---

### 4. [Section D: AI-Augmented Learning](./Section_D/)
* **AI-Assisted Development & Debugging Workflow** (`section_d_ai_learning.py`)
  1. Exact prompt given to the AI tool.
  2. AI's original code vs corrected, debugged production version.
  3. 3–4 line explanatory note detailing the fixes (syntax error with `HAVING` before `GROUP BY`, missing database file checks, unhandled empty DataFrame crashes, and chart annotations).
* Generated chart: `section_d_top3_chart.png`
* Screenshots in [`Section_D/screenshots/`](./Section_D/screenshots/).
* Documentation: [Section_D_AI_Submission.md](./Section_D/Section_D_AI_Submission.md)

---

### 5. [Master Report](./Master_Report/)
* [Master_Assessment_Submission.md](./Master_Report/Master_Assessment_Submission.md): Complete, unified master assessment documentation.
* [generate_screenshots.py](./Master_Report/generate_screenshots.py): High-resolution terminal and SQLite GUI screenshot generator.

---

## 🚀 Quick Execution
```powershell
# Section B Tasks
python Section_B\task1_daily_orders.py
python Section_B\task2_data_cleaning.py
python Section_B\task3_visualisation_dashboard.py
python Section_B\task4_sql_performance.py

# Section C Mini Capstone (Interactive or Demo)
python Section_C\section_c_mini_capstone.py --demo

# Section D AI Learning & Debugging
python Section_D\section_d_ai_learning.py
```
