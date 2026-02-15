# 📢 Machine Learning: Repeat Order Prediction
Repeat Order Prediction is a machine learning project designed to forecast whether a customer will reorder a previously purchased product.

<br>

## 🏷️ Business Motivation
This project aims to optimize Instacart's marketing efficiency. By using **Logistic Regression** and key behavioral features, we identify high-propensity customers. This allows the marketing team to execute **Targeted Campaigns** that increase conversion rates, improve customer retention, and significantly reduce wasted promotional costs.

<br>

## 📜 Overview

- **Algorithm:** Logistic Regression

- **4 Core Features:**

    **1. Purchase Frequency (count_orders):** How many times a user bought the product.

    **2. Reorder Intervals (avg_days_between_reorder):** Average number of days between repeat purchases of that product.

    **3. Product Popularity (prod_reorder_rate):** The overall global probability of the product being reordered.

    **4. User Habits (user_avg_days_between_orders):** The customer's general shopping frequency across all orders.

<br>

## 📜 Key Results
   - **Model Performance:** Achieved a **ROC AUC score of 0.81**, demonstrating an 81% ability to separate between reorder and non-reorder cases.
   - **Optimal Strategy:** By setting a **Threshold of 0.40**, the model effectively balances Precision and Recall, identifying the customers most likely to make purchase decision.
   - **Business Impact:** Generated a **Targeted Marketing** List of over **1.9 million** user-product pairs, sorted (ranked) by probability, to prioritize marketing efforts and maximize **Return on Investment (ROI)**.

<br>

## 📜 **Strategic Insights (Error Analysis)**

A deep dive into **False Negatives** (Missed Opportunities) revealed that the model occasionally struggles with "long-cycle" items, such as spices and pantry staples (household items).

**Future Roadmap (Model V.2)**: To further enhance performance, future iterations will include:

   - **Recency Features:** Time elapsed since the very last purchase.
   - **Product Category Analysis:** To better capture diverse purchase cycles across different aisles.
  
<br>


## 📊

  
