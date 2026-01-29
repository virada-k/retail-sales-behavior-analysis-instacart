# Download Library
library(dplyr)
library(data.table)
library(ggplot2)


# Download Dataset
cus_seg <- fread("orders.csv")


## Manage data within dataset
cus_seg <- cus_seg %>%
  filter(eval_set %in% c("prior", "train")) %>%
  select(user_id,
         order_number,
         days_since_prior_order) %>%
  rename(customer_id = user_id,
         date_diff = days_since_prior_order)


## Check data after revise name
head(cus_seg, n = 8)

# ## result:
   customer_id order_number date_diff
         <int>        <int>     <num>
1:           1            1        NA
2:           1            2        15
3:           1            3        21
4:           1            4        29
5:           1            5        28
6:           1            6        19
7:           1            7        20
8:           1            8        14


# Prepare the RF analysis for K-means modeling process

### Note: I found the RF (Recency & Frequency) analysis, not the M analysis (Monetary), because this dataset does not contain price data.

## R (Recency) analysis
recency_data <- cus_seg %>%
  group_by(customer_id) %>%
  filter(order_number == max(order_number)) %>%
  summarise(last_order_date = max(date_diff),
            .groups = 'drop')

print(recency_data)

## F (Frequency) analysis
frequency_data <- cus_seg %>%
  group_by(customer_id) %>%
  summarise(count_order_num = n_distinct(order_number),
            .groups = 'drop')

print(frequency_data)



## Merge tables between "recency_data" & "frequency_data".
rf_data <- recency_data %>%
  inner_join(frequency_data, by = "customer_id")

print(rf_data)


## Check which items have a value of 0.
sum(rf_data$last_order_date == 0)
sum(rf_data$count_order_num == 0)

# ⛔Not use: the results above will show the number of customers. ⛔
# count_order_num == 0 (result = 0): mean of "count_order_num == 0" >> count the number of customers whose order quantity = 0 | "result = 0" mean >> every customer has purchased something because no one has a "order = 0".
# last_order_date == 0 (result = 3152): mean of "last_order_date == 0" >> Date the customer last purchased the product, which == 0 is The last day the customer made a purchase was yesterday. | "result = 3152" mean >> the number of customers who purchased products yesterday was 3152.

# > recency = new = last = last_order_date = R_log
# > frequency = number = count = count_order_num = F_log



## Adjust the scale to avoid outlines by log() function.
rf_data_scaled <- rf_data %>%
  mutate(R_log = log(last_order_date + 1),
         F_log = log(count_order_num + 1)) %>%
  select(R_log, F_log) %>%
  scale()


## Manage the NA value
rf_data_scaled <- na.omit(rf_data_scaled)

### Note: I used the na.omit() function to remove all NA (missing value) to avoid errors during the K-means process.



## ⛔  Not Use
# Elbow Method
wss <- sapply(1:10, function(k){
  kmeans(rf_data_scaled, centers = k, nstart = 25)$tot.withinss
})

plot(1:10, wss, type="b", pch = 19, frame = FALSE, 
     xlab="Number of clusters K",
     ylab="Total within-clusters sum of squares",
     main="Elbow Method for Optimal K")





## ML: K-means process

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

print(segment_summary)


## Create the cluster_labels
cluster_labels <- segment_summary %>%
  select(cluster, customer_level)

print(cluster_labels)


## Create a Customer Group
 
## Merge table between "rf_data & cluster_labels"
customer_cluster <- rf_data %>%
  select(customer_id, last_order_date, count_order_num, cluster) %>%
  left_join(cluster_labels, by = "cluster") %>%
  select(customer_id, cluster, customer_level, everything())

print(customer_cluster)


## Cluster no. 1 "New Customers"
new_customers <- customer_cluster %>%
  filter(cluster == 1)

print(new_customers)


## Cluster no. 2 "Lost Customers"
lost_customers <- customer_cluster %>%
  filter(cluster == 2)

print(lost_customers)


## Cluster no. 3 "Core Loyalists"
core_loyalists <- customer_cluster %>%
  filter(cluster == 3)

print(core_loyalists)


## Cluster no. 4 "At-Risk Loyalists"
at_risk_loyalists <- customer_cluster %>%
  filter(cluster == 4)

print(at_risk_loyalists)




## Predictive Churn Analysis

## Create the cycle_time
### Note: I created the variable cycle_time to compare variable between the cycle_time (past behavior) and recency (current behavior) to filter out customers who likely to stop purchasing product.


cycle_time <- cus_seg %>%
  select(customer_id, date_diff) %>%
  group_by(customer_id) %>%
  summarise(avg_order_date = mean(date_diff, na.rm = TRUE), 
            .groups = 'drop')

print(cycle_time)




## Compare the cycle_time with each cluster_customer
cluster_cycle_analysis <- customer_cluster %>%
  left_join(cycle_time, by = "customer_id") %>%
  mutate(recency_vs_cycle = last_order_date / avg_order_date) %>%
  rename(cus_id = customer_id,
         last_date = last_order_date,
         n_order_num = count_order_num) %>%
  select(cus_id, cluster, customer_level, last_date, n_order_num, 
         avg_order_date, recency_vs_cycle)

print(cluster_cycle_analysis, n = 10)

### ⛔ Note: About the detail of result of recency_vs_cycle below.
# The result show "0" mean that it's the perfect time for customers to make a purchase.
# The result show "> 1" mean that the customers are purchasing products later than usual.
# The result show "< 1" mean that it's not yet time for customers to purchase the product.




## Target Groups Analysis (At-Risk Loyalists & Lost Customers)
check_cluster_2_4 <- cluster_cycle_analysis %>%
  filter(cluster %in% c(2, 4)) %>%
  mutate(customer_level = case_when(
    customer_level == "Lost Customers" ~ "Lost Cust",
    customer_level == "At-Risk Loyalists" ~ "Loyal Risk"
  )) %>%
  select(cus_id, cluster, customer_level, n_order_num, last_date, 
         avg_order_date, recency_vs_cycle)

print(check_cluster_2_4)

### Note: I only would like to check cluster 2 and 4 because these 2 groups have a high risk of discontinuous the service.




## Cluster 4: High-Value Churn Risk
cluster4_high_churn_risk <- check_cluster_2_4 %>%
  filter(cluster == 4,
         # >= 1.3 is more than 30% from average order date.
         recency_vs_cycle >= 1.30)

### Note 1: I selected date more than 30% of average order date is high risk for churn, because in case below 30%, it's possible customers may forgot or may not be available to purchase as it's not their holiday.

### Note 2: Inform the Marketing Team. 
### This is the group where we need to utilize the highest level of "Win-back Campaigns," such as personalized discount coupons or calling to survey customer satisfaction, because bringing this group back is far more worthwhile than acquiring new customers.

print(cluster4_high_churn_risk)




## Cluster 2: Churn Risk
cluster2_high_churn_risk <- check_cluster_2_4 %>%
  filter(cluster == 2,
         last_date < 30) %>%
  mutate(num_of_day = last_date - avg_order_date) %>%
  filter(num_of_day > 2,
         num_of_day <= 5) %>%
  select(cus_id, cluster, customer_level, n_order_num, last_date,
         avg_order_date, num_of_day)

### Note 1: I selected last_date < 30, because this dataset has the max date of 30 days (if more than that, the data will still be recorded for 30 days as well), ensuring data integrity since the dataset caps intervals at 30 days. This allows for a more precise 'Early Warning' analysis, and for the group that has been there for 30 days or more, we can immediately conclude that they are "lost."

### Note 2: I selected 5 days because we wanted to capture customers during the Critical Window. If we let more than 5 days pass, the Cluster 4 customers (who didn't buy frequently to begin with) would be highly likely to be lost. Therefore, we used the 5-day criterion as an 'Early Warning System' for the marketing team to quickly intervene and rebuild relationships before the retention cost increases further.

### Note 3: Inform the Customer Service Team.
### For this customer group, we should send "Personalized Reminders" such as "We have a new product you might like" or "Your points are about to expire" to encourage them to engage again before they become permanently lost customers.

print(cluster2_high_churn_risk)




# Chart

## Prepare data set 1 (Total Count)
total_data <- segment_summary %>%
  select(customer_level, customer_count) %>%
  mutate(Type = "Total in Segment")

print(total_data)

# ⛔ Type is a label function  ⛔ ---



## Prepare data set 2 (High Churn Risk)
risk_count_data <- data.frame(
  customer_level = c("Lost Customers", "At-Risk Loyalists"),
  customer_count = c(nrow(cluster2_high_churn_risk), 
                     nrow(cluster4_high_churn_risk)),
  Type = "High Churn Risk"
)

print(risk_count_data)


## Merge 2 tables
plot_data <- bind_rows(total_data, risk_count_data)


plot_data <- plot_data %>%
  mutate(customer_level = factor(customer_level,
                                levels = c("New Customers",
                                           "Core Loyalists",
                                           "At-Risk Loyalists",
                                           "Lost Customers")),
         Type = factor(Type,
                       levels = c("Total in Segment",
                                  "High Churn Risk"))
         )


print(plot_data)


## Create Bar Chart (Side-by-Side)
ggplot(plot_data, aes(x = customer_level, 
                      y = customer_count,
                      fill = Type)) +
  geom_col(position = "dodge") +
  geom_text(aes(label = scales::comma(customer_count)),
            position = position_dodge(width = 0.9), 
            vjust = -0.5, size = 3) +
  scale_fill_manual(values = c("Total in Segment" = "grey80", 
                               "High Churn Risk" = "#E64A19")) +
  theme_light() +
  labs(title = "Actionable Churn Insights: High-Priority Retention Targets",
       subtitle = "Identifying high-priority churn risks based on individual purchase cycle deviations",
       x = "Segment", 
       y = "Number of Customers",
       caption = "Data source: InstaCart Online Grocery Basket Analysis Dataset on Kaggle")
  



# Export Data
### Note: I exported the data to send customer information to Marketing and Customer Service Team.

write.csv(cluster2_high_churn_risk, "cluster2_high_churn_risk.csv", row.names = F)

write.csv(cluster4_high_churn_risk, "cluster4_high_churn_risk.csv", row.names = F)

write.csv(cluster_cycle_analysis, "cluster_cycle_analysis.csv", row.names = F)
