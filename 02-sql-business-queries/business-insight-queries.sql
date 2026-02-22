-- 📌 GOLDEN HOUR ANALYSIS
-- Analyze "PEAK Ordering Time" to arrange staff for packing and delivering orders.

SELECT
    order_hour_of_day AS order_hour,
    COUNT(*) AS count_order_hour
FROM orders
GROUP BY order_hour
ORDER BY count_order_hour DESC
LIMIT 10;

-- 📢 Note: The data shows that the peak shopping time for customers is between 9 a.m. and 5 p.m.



-- 📌 GOLDEN DAY ANALYSIS
-- Analyze the days with the highest customer orders volume to prepare the stock.

SELECT
    CASE
      WHEN order_dow = 0 THEN 'Sunday'
      WHEN order_dow = 1 THEN 'Monday'
      WHEN order_dow = 2 THEN 'Tuesday'
      WHEN order_dow = 3 THEN 'Wednesday'
      WHEN order_dow = 4 THEN 'Thursday'
      WHEN order_dow = 5 THEN 'Friday'
      ELSE 'Saturday'
    END AS day_of_week, 
    COUNT(*) AS count_order_day
FROM orders
GROUP BY order_dow
ORDER BY count_order_day DESC;

-- 📢 Note: The data shows that the three days with the highest number of product orders are Sunday to Tuesday.



-- 📌 CUSTOMER MAXIMUM REORDER
-- Analyze the product to consider how often customers will repurchase.

SELECT
    op.product_id,
    p.product_name,
    COUNT(*) AS total_reorders,
    ROUND(AVG(o.days_since_prior_order), 1) AS avg_day_gap
FROM orders AS o
INNER JOIN order_products__prior AS op ON o.order_id = op.order_id
INNER JOIN products AS p ON op.product_id = p.product_id
WHERE op.reordered = 1 
  AND o.days_since_prior_order IS NOT NULL
GROUP BY op.product_id, p.product_name
HAVING total_reorders > 600 -- The number 600 comes from the top 10% of best-selling products.
ORDER BY total_reorders DESC
LIMIT 100;

-- 📢 Note: The data shows that Vegetables and fruits had the highest number of orders.



-- 📌 OFF-PEAK STRATEGY ANALYSIS
-- Analyze the days and times with the fewest customer orders to organize a flash sale promotion (special discount).

SELECT
    CASE
      WHEN order_dow = 0 THEN 'Sunday'
      WHEN order_dow = 1 THEN 'Monday'
      WHEN order_dow = 2 THEN 'Tuesday'
      WHEN order_dow = 3 THEN 'Wednesday'
      WHEN order_dow = 4 THEN 'Thursday'
      WHEN order_dow = 5 THEN 'Friday'
      ELSE 'Saturday'
    END AS day_of_week,
    order_hour_of_day AS order_hour,
    COUNT(*) AS count_order
FROM orders
GROUP BY order_dow, order_hour_of_day
ORDER BY count_order;

-- 📢 Note: The data shows that Tuesday to Thursday are the days with the lowest sales.
