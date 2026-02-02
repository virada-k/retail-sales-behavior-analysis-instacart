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

- ⌨️ You can find the full script in [customer-segmentation-churn-analysis.r](customer-segmentation-churn-analysis.r).

<br>
<br>

## 📜 Code for K-Means Process

The code below is the K-Means process only.

<br>

```r
k <- 4

set.seed(93)
kmeans_model <- kmeans(rf_data_scaled, centers = k, nstart = 25)

rf_data$cluster <- kmeans_model$cluster

segment_summary <- rf_data %>%
  group_by(cluster) %>%
  summarise(
    avg_recency = mean(last_order_date),
    avg_frequency = mean(count_order_num),
    customer_count = n()
  ) %>%
  mutate(customer_level = case_when(
                            cluster == 1 ~ "New Customers",
                            cluster == 2 ~ "Lost Customers",
                            cluster == 3 ~ "Core Loyalists",
                            cluster == 4 ~ "At-Risk Loyalists")) %>%
  select(cluster, customer_level, avg_recency, avg_frequency,
         customer_count)
```

<br>
<br>

## 📜 Customer Segmentation Summary Table Result

<br>

The data obtained from the K-means process led to conclusions regarding customer segmentation to the following :

| Customer Segment | Description | Avg Recency (Days) | Avg Frequency (Orders) | Customer Count |
| :--- | :--- | ---: | ---: | ---: |
| **Core Loyalists** | High frequency & recently active. | 5.48 | 42.30 | 37,525 |
| **New Customers**  | Recently joined & low frequency. | 5.84 | 8.41 | 42,611 |
| **⚠️ At-Risk Loyalists** | High-value customers starting to slip away. | 21.10 | 18.80 | 50,889 |
| **⚠️ Lost Customers** | Low frequency & inactive for a long time. | 25.50 | 5.89 | 75,184 |


<br>
<br>

## 📜 Predictive Churn Analysis Process

<br>

I would like to focus only "At-Risk Loyalists" and "Lost Customers", as these two clusters have a high risk of customer churn.

The table below summarizes the number customers after I ran the code to Predictive Churn Analysis.

| Customer Segment | Predicted Churner | 🚨 High-Priority Risk |
| :--- | ---: | ---: |
| **At-Risk Loyalists** | 50,889 |  29,761 |
| **Lost Customers** | 75,184 |  5,427 |




