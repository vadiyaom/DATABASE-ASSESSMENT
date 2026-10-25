-- ==============================================================================
-- ASSESSMENT: Data Science M4-A1 | Modules 3-4
-- Section B - Task 4: SQL Queries & Relational Database Analytics
-- Database: SQLite (food_delivery.db)
-- ==============================================================================

-- 1. DDL: Create Tables
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS restaurants;

CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    order_value REAL NOT NULL,
    delivery_time_mins REAL NOT NULL,
    rating REAL NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id)
);

-- 2. DML: Insert at least 8 Restaurants
INSERT INTO restaurants (restaurant_id, name, category, city) VALUES
(1, 'Spice Villa', 'North Indian', 'Mumbai'),
(2, 'Pizza Roma', 'Italian', 'Mumbai'),
(3, 'Burger Barn', 'Fast Food', 'Delhi'),
(4, 'Dragon Wok', 'Chinese', 'Delhi'),
(5, 'Royal Biryani', 'North Indian', 'Hyderabad'),
(6, 'Green Bowl', 'Healthy', 'Bangalore'),
(7, 'Pasta Fresca', 'Italian', 'Bangalore'),
(8, 'Dosa Hub', 'South Indian', 'Chennai'),
(9, 'Tandoor Treats', 'North Indian', 'Mumbai'),
(10, 'Subway Express', 'Fast Food', 'Delhi');

-- 3. DML: Insert at least 25 Orders
INSERT INTO orders (order_id, restaurant_id, order_value, delivery_time_mins, rating) VALUES
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
(128, 5, 1350.0, 37.0, 4.8);

-- 4. Analytical Performance Query (Task 4)
-- Groups by restaurant, computes total orders, total revenue, and average rating
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
ORDER BY 
    total_revenue DESC;
