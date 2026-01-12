# 📢 Database Simulation
I designed a relational schema.
You can find the full simulation script in [database-simulation.sql](database-simulation.sql).

<br>

## Create Table
'''sql
-- This script is designed to create a relational database schema based on the InstaCart Online dataset.
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  user_id INT NOT NULL,
  eval_set TEXT NOT NULL, -- eval = evaluation // eval_set includes: prior, train, test
  order_number INT NOT NULL,
  order_dow INT NOT NULL, -- 0-6 (Sunday to Saturday)
  order_hour_of_day INT NOT NULL,
  days_since_prior_order REAL -- can be NULL value for the first order of each user_id
);

<br>

## Database Simulation Results
This screenshot shows the 'orders' table with sample data created in Beekeeper Studio.

![Order Table Result](result-of-order-sample.PNG)
