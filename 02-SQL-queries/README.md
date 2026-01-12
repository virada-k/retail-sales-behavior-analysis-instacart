# 📢 Business Insight
I analyzed the data to find answers to three points:
1. **Golden Hour**: Find the best time to arrange staff for packing and delivery.
2. **Golden Day**: Find the peak days of each week to ensure we have enough stock for customers.
3. **Customer Reorder Cycle**: To understand how often products are repurchased.

You can find the full script in [business-insight-queries.sql](business-insight-queries.sql).

<br>

## Business Insight Results
These screenshots show the results of the 3 points mentioned above.

<br>

### Question 1: What are the peak time for ordering?
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

📝 **Golden Hour Result:** The data shows that the peak time for customers purchase is between 9 am and 5 pm.

![Golden Hour Result](result-of-golden-hour-analysis.PNG)

<br>

 📝 **Golden Days Result:** The data shows that the three days with the highest number of product orders are Sunday to Tuesday.

![Golden Days Result](result-of-golden-day-analysis.PNG)

<br>

📝 **Customer Reorder Cycle Result:** The data shows that most products follow a typical purchase cycle.
Such as "Bulk Products", like laundry detergents, are often bought monthly (on average, twice a month).

![Customer Reorder Cycle Result](result-of-customer-reorder-cycle-analysis.PNG)
