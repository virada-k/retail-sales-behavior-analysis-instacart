# 📢 Machine Learning: Repeat Order Prediction
Repeat Order Prediction ML is the prediction of whether a customer will reorder products they have previously purchased again.

<br>

## 🏷️ Business Motivation
This project aims to optimize Instacart's marketing efficiency by predicting whether a customer will reorder a specific product. By using Logistic Regression and key behavioral features, we can identify high-propensity customers, allowing the marketing team to execute Targeted Campaigns that increase conversion rates and reduce wasted promotional costs.

<br>

## 📜 Overview

- **Algorithm:** Logistic Regression

- **4 Core Features:**

    **1. Purchase Frequency (count_orders):** How many times a user bought the product.

    **2. Reorder Intervals (avg_days_between_reorder):** Average number of days for repeat orders.

    **3. Product Popularity (prod_reorder_rate):** The overall chance of the product being bought again.

    **4. User Habits (user_avg_days_between_orders):** The customer's general shopping frequency.

- **Key Results:**
   - **Model Performance:** Achieved a ROC AUC score of this model is 0.81, which means it has the ability to separate positives from negatives by 81%.
   - **Optimal Strategy:** By setting a Threshold of 0.40, the model balances precision and recall, effectively identifying customers who are most likely to make purchase decision.
   - **Business Impact:** Generated a Targeted Marketing List of over 1.9 million user-product pairs, sorted (ranked) by probability, to prioritize marketing efforts and maximize "return on investment (ROI)".

- **Strategic Insights (Error Analysis)**
   A deep dive into False Negatives revealed that the model occasionally misses "long-cycle" items like spices and pantry staples (household items). This insight provides a clear roadmap for Model V.2, where adding "Recency" and "Product Category" features could further improve predictions for various product types.

<br>


  

  
