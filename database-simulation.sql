-- Database Simulation: Creating the orders table.

-- Drop the table if it already exists to allow rerunning the script.
DROP TABLE IF EXISTS orders;

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


-- Insert data into the Orders table.
INSERT INTO orders VALUES
  (1, 112108, 'train', 4, 4, 10, 9.0),
  (2, 202279, 'prior', 3, 5, 9, 8.0),
  (3, 205970, 'prior', 16, 5, 17, 12.0),
  (15, 54901, 'prior', 51, 3, 11, 2.0),
  (17, 36855, 'test', 5, 6, 15, 1.0),
  (20, 182912, 'prior', 1, 6, 17, NULL),
  (24, 193635, 'prior', 19, 0, 14, 0.0),
  (26, 153404, 'prior', 2, 0, 16, 7.0),
  (34, 35220, 'test', 20, 3, 11, 8.0),
  (38, 42756, 'train', 6, 6, 16, 24);


-- Verification Query
SELECT * FROM orders;
