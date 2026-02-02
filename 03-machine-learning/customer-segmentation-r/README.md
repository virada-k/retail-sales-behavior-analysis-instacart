# 📢 Machine Learning: Customer Segmentation

<br>


## 📜 Overview & Methodology
<br>

- **Algorithm:** K-Means Clustering
  
- **Feature Selection:** RF (Recency & Frequency) Analysis

    **1. Recency:** The number of days since the customer's most recent order.

    **2. Frequency:** The total number of orders the customer has ever placed.

    *Note:* Monetary (M) was excluded due to the lack of pricing data in the Instacart dataset.

- **Optimal K:** Selected k=4 clusters based on personal suitability.

<br>
<br>

## 📜 Customer Segmentation Summary Table Result

<br>

The data obtained from the K-means process led to conclusions regarding customer segmentation to the following :

| Customer Segment | Description | Avg Recency (Days) | Avg Frequency (Orders) | Customer Count |
| :--- | :--- | ---: | ---: | ---: |
| **Core Loyalists** | High frequency & recently active. | 5.48 | 42.30 | 37,525 |
| **New Customers** | Recently joined & low frequency. | 5.84 | 8.41 | 42,611 |
| **⚠️ At-Risk Loyalists** | High-value customers starting to slip away. | 21.10 | 18.80 | 50,889 |
| **⚠️ Lost Customers** | Low frequency & inactive for a long time. | 25.50 | 5.89 | 75,184 |
