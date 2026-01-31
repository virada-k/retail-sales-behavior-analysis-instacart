# 📢 Machine Learning: Customer Segmentation

<br>


## 📜 Overview & Methodology
<br>

- **Algorithm:** K-Means Clustering
  
- **Feature Selection:** RF (Recency & Frequency) Analysis

    *1. Recency:* The number of days since the customer's most recent order.

    *2. Frequency:* The total number of orders the customer has ever placed.

    *Note:* Monetary (M) was excluded due to the lack of pricing data in the Instacart dataset.

- **Optimal K:** Selected k=4 clusters based on personal suitability.

<br>

## 📜 K-Means Precess

| Cluster | Customer Level | Avg Recency (Days) | Avg Frequency (Orders) | Customer Count |
| :---: | :--- | ---: | ---: | ---: |
| 1 | New Customers | 5.84 | 8.41 | 42,611 |
| 2 | Lost Customers | 25.50 | 5.89 | 75,184 |
| 3 | Core Loyalists | 5.48 | 42.30 | 37,525 |
| 4 | At-Risk Loyalists | 21.10 | 18.80 | 50,889 |
