# Section A — Concept Application
**Course:** Data Science (Modules 3–4: Data Collection, Cleaning & Visualization › Working with Databases)  
**Assessment Code:** M4-A1  
**Stack:** Python 3 / SQL (SQLite)  

---

## Scenario 1 (S1): Handling Missing Data & Type Casting in Pandas

### Scenario
> You are a Data Analyst at a food delivery startup. You have loaded a dataset of 50,000 order records into a Pandas DataFrame. The `'delivery_time_mins'` column has 14% missing values, and the `'customer_rating'` column contains some entries stored as strings (e.g., `'4.5'`) instead of `float64`.

### Question
> Explain which strategy you would choose to handle the missing values in `'delivery_time_mins'` — dropping rows versus imputation with mean or median — and justify your reasoning based on the percentage of missing data and skewness of delivery times. Also describe the exact Pandas steps needed to fix the `'customer_rating'` column type before any analysis is performed.

---

### Detailed Answer & Solution

#### 1. Missing Value Strategy for `'delivery_time_mins'`: Imputation vs. Dropping
* **Evaluation of Dropping Rows:**
  - With 50,000 records, a 14% missing rate corresponds to **7,000 dropped observations**.
  - As a standard data science rule of thumb, dropping rows (listwise deletion) is only permissible when missingness is under **3% to 5%** and verified to be Missing Completely at Random (MCAR).
  - Discarding 14% of the dataset leads to a severe loss of statistical power and introduces systematic **selection bias** (e.g., deliveries that experienced delivery tracking failures or operational delays might have higher missing rates).
  - Therefore, **dropping rows must be rejected**.

* **Mean vs. Median Imputation:**
  - **Distribution Skewness:** Real-world logistics and food delivery times are strictly non-negative and inherently **right-skewed (positively skewed)**. While most orders are delivered within 25–40 minutes, a significant right tail exists due to severe traffic congestion, adverse weather, peak kitchen preparation bottlenecks, and long-distance deliveries (extending to 70–120+ minutes).
  - **Sensitivity of the Mean:** The arithmetic mean is heavily influenced by extreme values in the right tail, which would pull the imputed average upward and artificially overestimate delivery durations for missing rows.
  - **Robustness of the Median:** The median (50th percentile) represents the true operational center of a skewed distribution and is completely resistant to extreme outlier distortions.
  - **Strategy Conclusion:** **Median imputation** is the optimal strategy. In advanced production pipelines, imputing the median grouped by restaurant category or delivery radius (`df.groupby('category')['delivery_time_mins'].transform('median')`) yields even higher domain fidelity.

#### 2. Exact Pandas Steps to Fix the `'customer_rating'` Column Type
The `'customer_rating'` column has mixed data types (strings, numeric objects, potential leading/trailing whitespaces, or corrupt text values like `'N/A'`, `'?'`, or empty strings).

```python
import pandas as pd
import numpy as np

# Step 1: Strip accidental whitespace from string representations
df['customer_rating'] = df['customer_rating'].astype(str).str.strip()

# Step 2: Convert to numeric float64 safely using errors='coerce'
# Any unparseable string (e.g., 'N/A', 'missing') safely becomes NaN
df['customer_rating'] = pd.to_numeric(df['customer_rating'], errors='coerce')

# Step 3: Verify that the dtype is now float64
assert df['customer_rating'].dtype == 'float64'

# Step 4: Validate domain boundaries (ratings must fall strictly between 1.0 and 5.0)
invalid_ratings = df[(df['customer_rating'] < 1.0) | (df['customer_rating'] > 5.0)]
if not invalid_ratings.empty:
    df.loc[(df['customer_rating'] < 1.0) | (df['customer_rating'] > 5.0), 'customer_rating'] = np.nan

# Step 5: Impute missing ratings with rounded mean rating
mean_rating = round(df['customer_rating'].mean(), 1)
df['customer_rating'] = df['customer_rating'].fillna(mean_rating)
```

---

## Scenario 2 (S2): NumPy Vectorization & Boolean Indexing for Surge Detection

### Scenario
> You are building a weekly performance report for a food delivery platform. You have a NumPy array of daily order counts across 30 days. Your manager wants to flag 'surge days' — days where the order count exceeds the mean by more than 1.5 standard deviations — and compute the total revenue only for those surge days using a matching revenue array.

### Question
> Describe how NumPy boolean indexing and statistical functions (`np.mean`, `np.std`) work together to identify surge days without using a Python loop. Explain what a boolean mask is and why element-wise array operations make this approach significantly faster than looping through each element individually.

---

### Detailed Answer & Solution

#### 1. How NumPy Functions and Boolean Indexing Work Together
Instead of iterating through indices using a traditional `for` loop, NumPy coordinates vectorized statistical computation and boolean masking in three concise steps:

```python
import numpy as np

# 30 days of simulated orders and revenue
np.random.seed(42)
orders = np.random.randint(100, 800, size=30)
revenue = np.random.uniform(5000, 50000, size=30)

# Step 1: Calculate the statistical surge threshold
mean_orders = np.mean(orders)
std_orders = np.std(orders)
surge_threshold = mean_orders + (1.5 * std_orders)

# Step 2: Create a boolean mask via element-wise comparison
surge_mask = orders > surge_threshold

# Step 3: Apply the mask to extract surge days and aggregate revenue
surge_orders = orders[surge_mask]
surge_revenue = revenue[surge_mask]
total_surge_revenue = np.sum(surge_revenue)
surge_day_indices = np.where(surge_mask)[0]
```

#### 2. What a Boolean Mask Is
A **boolean mask** is an array of boolean flags (`True` and `False`) whose dimensions and shape match the underlying target array. It acts as an element-by-element conditional filter:
- When evaluating `orders > surge_threshold`, NumPy broadcasts the scalar threshold across all 30 elements of `orders` and executes an element-wise logical comparison.
- When passing this mask into bracket indexing `revenue[surge_mask]`, NumPy selectively extracts only the elements corresponding to `True` indices, completely filtering out `False` values without requiring temporary lists or conditional branching statements.

#### 3. Why Element-Wise Vectorization Outperforms Python Loops
1. **Homogeneous C-Level Execution:** NumPy arrays are contiguous blocks of memory containing uniform C primitives (e.g., `int32`, `float64`). A standard Python loop deals with dynamic `PyObject` wrappers, requiring type inspection, pointer dereferencing, and garbage collection tracking on every single iteration.
2. **Elimination of Interpreter Overhead:** Vectorized operations execute within compiled C routines, avoiding Python bytecode interpretation per element.
3. **CPU Cache Locality & SIMD Optimization:** Contiguous data structures maximize CPU L1/L2 cache hits. Furthermore, modern CPU compilers leverage **SIMD (Single Instruction, Multiple Data)** vector registers (e.g., AVX2, AVX-512), allowing 4 to 8 floating-point comparisons and additions to execute simultaneously in a single processor clock cycle. This results in execution speeds typically **50x to 100x faster** than native Python loops.

---

## Scenario 3 (S3): Exploratory Data Analysis & Visualization Strategy

### Scenario
> You are conducting EDA for a food delivery product team. Your dataset contains columns: `restaurant_category`, `average_order_value`, `customer_rating`, and `delivery_time_mins`. The team wants to know (a) whether delivery time is correlated with customer rating, and (b) how average order value is distributed across restaurant categories.

### Question
> Identify whether each business question requires univariate, bivariate, or multivariate analysis. For each question, name one specific Seaborn chart type that would best visualise the relationship and explain why that chart type is more appropriate than a simple line plot for this data.

---

### Detailed Answer & Solution

#### Question (a): Correlation between Delivery Time and Customer Rating
* **Analysis Classification:** **Bivariate Analysis**  
  *Justification:* It examines the statistical relationship and dependency between exactly two continuous quantitative variables (`delivery_time_mins` as the independent predictor and `customer_rating` as the dependent response).
* **Recommended Seaborn Chart:** `sns.scatterplot()` or `sns.regplot()`
  ```python
  sns.regplot(data=df, x='delivery_time_mins', y='customer_rating', 
              scatter_kws={'alpha': 0.6}, line_kws={'color': 'crimson'})
  ```
* **Why Better than a Simple Line Plot:**
  - A line plot sequentially connects consecutive points with line segments, implicitly assuming that the data is continuous, sequential, or time-ordered.
  - In cross-sectional food delivery orders, data points are unordered independent observations. Connecting these points with a line plot produces an unintelligible, tangled "spiderweb" of zigzagging lines.
  - A scatter plot displays every individual order as an independent coordinate $(x, y)$, immediately revealing point clustering, non-linear inflection thresholds (e.g., ratings falling steeply when delivery exceeds 45 mins), dispersion, heteroscedasticity, and outliers. Adding a regression trendline directly answers the correlation hypothesis.

#### Question (b): Distribution of Average Order Value across Restaurant Categories
* **Analysis Classification:** **Bivariate Analysis**  
  *Justification:* It investigates the distribution of one continuous quantitative variable (`average_order_value`) conditional upon one discrete categorical grouping variable (`restaurant_category`).
* **Recommended Seaborn Chart:** `sns.boxplot()` (or `sns.violinplot()`)
  ```python
  sns.boxplot(data=df, x='restaurant_category', y='average_order_value', palette='Set2')
  ```
* **Why Better than a Simple Line Plot:**
  - `restaurant_category` is a nominal, categorical variable (e.g., Fast Food, Italian, Cafe, Biryani) with no intrinsic ordinal continuity. Drawing a line across categories falsely implies a continuous gradient between distinct business entities.
  - A boxplot visualizes the full five-number summary for each category: the median (Q2), interquartile range (IQR from Q1 to Q3), whiskers representing data spread, and explicitly plotted outlier points. This allows stakeholders to evaluate median spending, variance, and pricing skewness across cuisines at a single glance.

---

## Scenario 4 (S4): Relational Database Joins & Data Completeness

### Scenario
> You are managing a food delivery database with three tables: `orders` (`order_id`, `customer_id`, `restaurant_id`, `order_value`), `restaurants` (`restaurant_id`, `name`, `city`, `category`), and `customers` (`customer_id`, `name`, `area`). A business team asks for a report showing every restaurant's name and total revenue, including restaurants that have not yet received any orders.

### Question
> Explain which SQL JOIN type must be used to include restaurants with zero orders and describe what would happen if an INNER JOIN were used instead. Justify your choice of join type in terms of how it handles unmatched rows between the two tables.

---

### Detailed Answer & Solution

#### 1. Required SQL JOIN Type
To guarantee that all restaurants appear in the final report regardless of order history, a **`LEFT OUTER JOIN`** (or simply `LEFT JOIN`) must be used, designating the `restaurants` table as the left entity:

```sql
SELECT 
    r.restaurant_id,
    r.name AS restaurant_name,
    r.category,
    r.city,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.order_value), 0.0) AS total_revenue
FROM restaurants r
LEFT JOIN orders o 
    ON r.restaurant_id = o.restaurant_id
GROUP BY 
    r.restaurant_id, r.name, r.category, r.city
ORDER BY 
    total_revenue DESC;
```

#### 2. Consequence of Using an `INNER JOIN`
- An `INNER JOIN` strictly enforces bidirectional referential intersection: a row is returned if and only if matching values exist in **both** tables simultaneously (`r.restaurant_id = o.restaurant_id`).
- If a restaurant is newly registered, temporarily inactive, or has not yet received orders, its `restaurant_id` will be absent from the `orders` table.
- Consequently, an `INNER JOIN` will **completely eliminate newly onboarded or zero-revenue restaurants** from the report.
- **Business Impact:** This creates a dangerous survivorship bias in business reporting. The operations team would be blind to non-performing partners, onboarding bottlenecks, or dormant vendors.

#### 3. Theoretical Justification of Unmatched Row Handling
- **Preservation of Left Dimension:** A `LEFT JOIN` mandates that 100% of rows from the left table (`restaurants`) are retained in the virtual result set.
- **Null Extension:** When no matching record is found in the right table (`orders`), the SQL engine populates all attributes of the right table with `NULL`.
- **Handling Aggregates:** Using `COUNT(o.order_id)` evaluates exclusively to `0` for unmatched rows (as `COUNT` skips `NULL`s). Applying `COALESCE(SUM(o.order_value), 0.0)` gracefully converts `NULL` sums into a clean `0.00`, ensuring mathematically sound reporting.

---

## Scenario 5 (S5): Advanced SQL Window Functions vs. Aggregation

### Scenario
> You are working on a food delivery analytics dashboard. Management wants to rank all delivery agents within each city by their number of completed deliveries for the current month, and also display how each agent's count compares to the agent ranked directly above them in that city.

### Question
> Identify the two SQL window functions you would use — one for ranking and one for retrieving the previous row's value — and explain why using window functions with PARTITION BY produces more accurate and maintainable results for this requirement than a GROUP BY with a self-join or correlated subquery approach.

---

### Detailed Answer & Solution

#### 1. Identification of the Two SQL Window Functions
1. **For Ranking within City:**
   - Function: **`DENSE_RANK() OVER (PARTITION BY city ORDER BY completed_deliveries DESC)`**
   - *Rationale:* `DENSE_RANK()` assigns consecutive integer ranks ($1, 2, 3, \dots$) without skipping rank positions in the event of identical delivery counts (unlike standard `RANK()` which creates gaps).
2. **For Retrieving Previous Row's Value:**
   - Function: **`LAG(completed_deliveries, 1) OVER (PARTITION BY city ORDER BY completed_deliveries DESC)`**
   - *Rationale:* `LAG()` inspects the preceding record within the partitioned window frame, enabling instantaneous calculation of delivery differences between consecutive ranks.

```sql
SELECT 
    agent_id,
    agent_name,
    city,
    completed_deliveries,
    DENSE_RANK() OVER (
        PARTITION BY city 
        ORDER BY completed_deliveries DESC
    ) AS city_rank,
    LAG(completed_deliveries, 1) OVER (
        PARTITION BY city 
        ORDER BY completed_deliveries DESC
    ) AS above_agent_deliveries,
    COALESCE(
        LAG(completed_deliveries, 1) OVER (
            PARTITION BY city 
            ORDER BY completed_deliveries DESC
        ) - completed_deliveries, 
        0
    ) AS deficit_from_agent_above
FROM monthly_agent_performance
ORDER BY city, city_rank;
```

#### 2. Why Window Functions are Superior to `GROUP BY` + Self-Joins / Correlated Subqueries
| Architectural Dimension | Window Functions (`PARTITION BY`) | `GROUP BY` + Self-Join / Subquery |
| :--- | :--- | :--- |
| **Row Granularity** | Computes running metrics while **preserving every individual row's identity**. | Collapses rows into group aggregates; requiring complex joins to restore agent details. |
| **Computational Complexity** | **$O(N \log N)$**: The engine sorts the partitioned data once and computes values in a single streaming scan. | **$O(N^2)$**: Correlated subqueries or Cartesian self-joins perform repetitive quadratic table scans. |
| **Tie Handling** | Standardized, deterministic resolution of ties via explicit ordering criteria. | Highly fragile; duplicate delivery counts cause Cartesian duplicates in joins. |
| **Code Maintainability** | Declarative, concise, and modular SQL that is easy to read and optimize. | Deeply nested, verbose, and difficult to maintain or debug. |

---

## Scenario 6 (S6): Query Optimization: Common Table Expressions (CTEs) vs. Nested Subqueries

### Scenario
> You are optimising a SQL report for a food delivery operations team. The report first identifies the top 5 restaurant categories by total order count, and then retrieves the full order details only for restaurants belonging to those top categories. A colleague has written this as a deeply nested subquery inside the WHERE clause.

### Question
> Compare using a CTE (`WITH` clause) versus a nested subquery for this two-step requirement. Evaluate the trade-offs in terms of readability, ability to reuse the intermediate result, and debuggability. In what specific situation would you prefer the nested subquery over a CTE?

---

### Detailed Answer & Solution

#### 1. Comparative Implementation: CTE vs. Nested Subquery

##### Approach A: Clean CTE Implementation (`WITH` Clause)
```sql
WITH TopCategories AS (
    -- Step 1: Identify the top 5 restaurant categories by total order count
    SELECT 
        r.category,
        COUNT(o.order_id) AS total_orders
    FROM restaurants r
    JOIN orders o ON r.restaurant_id = o.restaurant_id
    GROUP BY r.category
    ORDER BY total_orders DESC
    LIMIT 5
)
-- Step 2: Retrieve full order details for restaurants in those categories
SELECT 
    o.order_id,
    o.restaurant_id,
    r.name AS restaurant_name,
    r.category,
    o.order_value,
    o.delivery_time_mins,
    o.rating
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN TopCategories tc ON r.category = tc.category
ORDER BY tc.total_orders DESC, o.order_id ASC;
```

##### Approach B: Deeply Nested Subquery
```sql
SELECT 
    o.order_id,
    o.restaurant_id,
    r.name AS restaurant_name,
    r.category,
    o.order_value,
    o.delivery_time_mins,
    o.rating
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE r.category IN (
    SELECT category FROM (
        SELECT 
            r_sub.category,
            COUNT(o_sub.order_id) AS total_orders
        FROM restaurants r_sub
        JOIN orders o_sub ON r_sub.restaurant_id = o_sub.restaurant_id
        GROUP BY r_sub.category
        ORDER BY total_orders DESC
        LIMIT 5
    ) AS sub
);
```

#### 2. Trade-Off Evaluation

* **Readability and Cognitive Load:**
  - *CTE:* Adheres to a sequential, top-to-bottom storytelling flow. It names intermediate logical datasets explicitly (`TopCategories`), allowing any engineer to immediately comprehend the two-step architecture.
  - *Nested Subquery:* Forces the developer to read from the inside out ("inverted pyramid"). Indentation nesting obscures the primary business intent of the outer query.
* **Reusability of Intermediate Results:**
  - *CTE:* Can be referenced multiple times across the main query (e.g., joining with `orders`, calculating category market shares, and computing aggregate summary benchmarks simultaneously).
  - *Nested Subquery:* Scoped strictly to the specific `WHERE` clause. Reusing it requires copy-pasting the entire subquery block, increasing maintenance overhead and risking logic divergence.
* **Debuggability & Testing:**
  - *CTE:* Can be tested interactively in seconds by commenting out the outer query and running `SELECT * FROM TopCategories;`.
  - *Nested Subquery:* Testing requires isolating sub-blocks, manually handling aliasing, and re-assembling the query.

#### 3. When Would You Prefer a Nested Subquery Over a CTE?
1. **Simple Scalar Comparisons & `EXISTS` Predicates:** For lightweight, single-row lookups (e.g., `WHERE order_value > (SELECT AVG(order_value) FROM orders)` or `WHERE EXISTS (...)`), an inline subquery is succinct and avoids unnecessary naming overhead.
2. **Legacy Database Engine Support:** Older database engines (e.g., MySQL versions prior to 8.0, older embedded SQLite versions prior to 3.8.3) do not support the SQL standard `WITH` clause.
3. **Optimizer Inefficiencies with CTE Materialization:** In certain database engines (such as PostgreSQL prior to version 12), CTEs were treated as strict optimization fences, forcing the engine to materialize intermediate results to temporary memory rather than pushing down filters and indexes. In such legacy environments, an inline subquery allows the query planner to inline and optimize predicates across joins.
