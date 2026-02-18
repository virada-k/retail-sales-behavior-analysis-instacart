# 📢 Machine Learning: Repeat Orders Prediction
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

- 🖥️ You can find the **full script** in [repeat order](reorder.py).

- 🖥️ You can **test run** this model in [google colab](https://colab.research.google.com/drive/1TkTDmAq5uZMpg0psWHBBz4Ak9AwpJ2gt?usp=sharing).

<br>

## 📜 Key Results
   - **Model Performance:** Achieved a **ROC AUC score of 0.81**, demonstrating an 81% ability to separate between reorder and non-reorder cases.
   - **Optimal Strategy:** By setting a **Threshold of 0.40**, the model effectively balances Precision and Recall, identifying the customers most likely to reorder.
   - **Business Impact:** Generated a **Targeted Marketing** List of over **1.9 million** user-product pairs, sorted (ranked) by probability, to prioritize marketing efforts and maximize **Return on Investment (ROI)**.

<br>

## 📜 **Strategic Insights (Error Analysis)**

A deep dive into **False Negatives** (Missed Opportunities) revealed that the model occasionally struggles with "long-cycle" items, such as spices and pantry staples (household items).

**Future Roadmap (Model V.2)**: To further enhance performance, future iterations will include:
   - **Recency Features:** Time elapsed since the very last purchase.
   - **Product Category Analysis:** To better capture diverse purchase cycles across different aisles.
  
<br>

## ⌨️ Code for the Logistic Regression process and setting Threshold.

<br>

```py
## Create training model.
model = LogisticRegression(solver = 'saga', # 'saga' is an algorithm suitable for big data.
                           max_iter = 1000,
                           random_state = 22,
                           n_jobs = -1)


## Apply Optimal Threshold (0.40) to Final Test Set
threshold = 0.40
y_pred = (y_pred_proba > threshold).astype(int)
```

<br>

## 📊 Chart

<br>

### 💡 Bar Chart

| Reordered | Count |
| :--- | ---: |
| Not Reordered | 2,844,299 |
| Reordered | 1,988,993 |

<br>

**Insight:** Based on the model's prediction with a 0.4 threshold, we identified approximately 1.99 million high-propensity user-product pairs (Reordered).

<br>

![test set bar chart](test-set-bar-chart-for-compare-reordered.png)

**Note:** The higher count of 'Not Reordered' cases compared to 'Reordered' is expected in real-world retail data. This is often due to customers trialing new products once, purchasing long-shelf-life items, or buying in bulk (packs), which results in a lower overall reorder frequency for those specific items.

<br>
<br>

🎫 An example of a customer list table to send to the marketing team for creating a coupon giveaway campaign.

<br>

| user_id | product_id | product_name | reordered_proba |
| ---: | ---: | :--- | ---: |
| 3 | 22035 | Organic Whole String Cheese | 0.78 |
| 3 | 16797 | Strawberries | 0.75 |
| 3 | 24010 | Wheat Gluten Free Waffles | 0.74 |
| 3 | 14992 | Green Beans | 0.72 |
| 3 | 44683 | Brussels Sprouts | 0.70 |

<br>

**Note:** This table shows a prioritized list, which helps marketing team to focus resources on items with the highest reorder probability.

For example, focusing on "Organic Whole String Cheese" for User 3, which has a 78% reorder probability.

<br>
<br>

### 💡 Histogram

The table below, mirroring the Histogram, shows examples of customer-product matching (user_id and product_id), which the "reordered_proba" column will use threshold 0.4 to determine the likelihood of a repeat order. If an item has a repeat purchase probability value >= 0.4 indicates a high probability of a repeat purchase, while a value < 0.4 means a low probability of repurchase.

| user_id | product_id | reordered_proba | reordered | 
| ---: | ---: | ---: | ---: |
| 3 | 248 | 0.14 | 0 |
| 3 | 1005 | 0.15 | 0 |
| 3 | 1819 | 0.66 | 1 |
| 3 | 7503 | 0.18 | 0 |
| 3 | 8021 | 0.19 | 0 |

<br>

![distribution](distribution-of-predicted-reorder-probability-on-test-set.png)



