# 📢 Business Insight
I analyzed the data to find answers to three points:
1. **Golden Hour**: Find the best time to arrange staff for packing and delivery.
2. **Golden Day**: Find the peak days of each week to ensure we have enough stock for customers.
3. **Customer Reorder Cycle**: To understand how often products are repurchased.

You can find the full script in [business-insight-queries.sql](business-insight-queries.sql).

<br>

## 📜 Business Insight Results
These screenshots show the results of the 3 points mentioned above.

<br>

### 📝 Question 1: What is the peak time for ordering?
```sql
-- Analyzing "PEAK Ordering Time" to arrange staff for packing and delivering orders.

SELECT
    order_hour_of_day AS order_hour,
    COUNT(*) AS count_order_hour
FROM orders
GROUP BY order_hour
ORDER BY count_order_hour DESC
LIMIT 10;
```
<br>

🛎️ **Golden Hour Result:** The data shows that the peak time for customers purchase is between 9 am and 5 pm.

![Golden Hour Result](result-of-golden-hour-analysis.PNG)

<br>

<br>

### 📝 Question 2: What are the peak days of each week for ordering?

```sql
-- Analyze the days with the highest customers order volume to prepare the stock.

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
```
<br>

🛎️ **Golden Days Result:** The data shows that the three days with the highest number of orders are Sunday, Monday and Tuesday.

![Golden Days Result](result-of-golden-day-analysis.PNG)

<br>

<br>

### 📝 Question 3: How often do customers repurchase products?

```sql
-- Analyze the product to determine how often customers will repurchase.

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
ORDER BY ROUND(AVG(o.days_since_prior_order)) DESC
LIMIT 10;
```
<br>

🛎️ **Customer Reorder Cycle Result:** The data shows that most products follow a typical purchase cycle.
Such as "Bulk Products", like laundry detergents, are often bought monthly (on average, twice a month).

![Customer Reorder Cycle Result](result-of-customer-reorder-cycle-analysis.PNG)
