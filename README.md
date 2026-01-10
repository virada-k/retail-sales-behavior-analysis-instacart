# 🛒 instacart-predictive-analytics-for-customer-behavior
Customer behavior analysis and reorder prediction using SQL, R, and Python.

<br>

## Database Simulation
I designed a relational schema.
You can find the full simulation script in [database-simulation.sql](./01-SQL-database-simulation/database-simulation.sql).

<br>

### Database Simulation Results
This screenshot shows the successfully created 'orders' table with sample data in Beekeeper Studio.
![Order Table Result](01-SQL-database-simulation/result-of-order-sample.PNG)

<br>
<br>

## Business Insight
I analyzed the data to find answers to three points:
1. Identify the "golden hour" when customers place the most orders, in order to allocate staff for packing and shipping orders.
2. Identify the "golden day (peak days of each week)" to ensure sufficient stock to meet customer demand.
3. Identify the "customer reorder cycle" to analyze customer repurchase behavior for each product type.

You can find the full script in [business-insight-queries.sql](./02-SQL-queries/business-insight-queries.sql).

<br>

### Business Insight Results
These screenshots shows the answers three points as mentioned above.

<br>

📢 Golden Hour Result
<br>
![Golden Hour Result](02-SQL-queries/result-of-golden-hour-analysis.PNG)

<br>

📢 Golden Days Result
![Golden Days Result](02-SQL-queries/result-of-golden-day-analysis.PNG)

<br>

📢 Customer Reorder Cycle Result
![Customer Reorder Cycle Result](02-SQL-queries/result-of-customer-reorder-cycle-analysis.PNG)


<br>
<br>

## Data Source
"Kaggle dataset": https://www.kaggle.com/datasets/yasserh/instacart-online-grocery-basket-analysis-dataset/data
