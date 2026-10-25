-- ==============================================================================
-- ASSESSMENT: Data Science M4-A1 | Modules 3-4
-- Section C - Mini Capstone Project: SQL Queries
-- Database: SQLite (food_delivery.db)
-- ==============================================================================

-- Query 1: Category-Level Performance using GROUP BY and Aggregates
-- Computes total order count, total revenue, average order value, and average rating
SELECT 
    r.category,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS total_revenue,
    ROUND(AVG(o.order_value), 2) AS avg_order_value,
    ROUND(AVG(o.rating), 2) AS avg_rating
FROM restaurants r
JOIN orders o 
    ON r.restaurant_id = o.restaurant_id
GROUP BY 
    r.category
ORDER BY 
    total_revenue DESC;

-- Query 2: Detailed Order & Restaurant Cross-Join with City Delivery Metrics
-- Displays order details along with restaurant name, category, and city
SELECT 
    o.order_id,
    r.name AS restaurant_name,
    r.category,
    r.city,
    o.order_value,
    o.delivery_time_mins,
    o.rating
FROM orders o
INNER JOIN restaurants r 
    ON o.restaurant_id = r.restaurant_id
ORDER BY 
    o.order_value DESC
LIMIT 10;

-- Query 3: City-Wise Performance Metrics
SELECT 
    r.city,
    COUNT(DISTINCT r.restaurant_id) AS active_restaurants,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.order_value), 2) AS city_revenue,
    ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_time_mins
FROM restaurants r
LEFT JOIN orders o 
    ON r.restaurant_id = o.restaurant_id
GROUP BY 
    r.city
ORDER BY 
    city_revenue DESC;
