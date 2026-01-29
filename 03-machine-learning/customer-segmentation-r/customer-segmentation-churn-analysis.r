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

# ## Note: I found the RF (Recency & Frequency) analysis, not the M analysis (Monetary), because this dataset does not contain price data.

## R (Recency) analysis
recency_data <- cus_seg %>%
  group_by(customer_id) %>%
  filter(order_number == max(order_number)) %>%
  summarise(last_order_date = max(date_diff),
            .groups = 'drop')

print(recency_data)
# ## result:
# A tibble: 206,209 × 2
   customer_id last_order_date
         <int>           <dbl>
 1           1              14
 2           2              30
 3           3              15
 4           4               0
 5           5               6
 6           6              12
 7           7               6
 8           8              10
 9           9              30
10          10              30
# ℹ 206,199 more rows
# ℹ Use `print(n = ...)` to see more rows


## F (Frequency) analysis
frequency_data <- cus_seg %>%
  group_by(customer_id) %>%
  summarise(count_order_num = n_distinct(order_number),
            .groups = 'drop')

print(frequency_data)
# ## result:
# A tibble: 206,209 × 2
   customer_id count_order_num
         <int>           <int>
 1           1              11
 2           2              15
 3           3              12
 4           4               5
 5           5               5
 6           6               3
 7           7              21
 8           8               4
 9           9               4
10          10               6
# ℹ 206,199 more rows
# ℹ Use `print(n = ...)` to see more rows


## Merge tables between "recency_data" & "frequency_data".
rf_data <- recency_data %>%
  inner_join(frequency_data, by = "customer_id")

print(rf_data)
# ## result:
# A tibble: 206,209 × 4
   customer_id last_order_date count_order_num cluster
         <int>           <dbl>           <int>   <int>
 1           1              14              11       4
 2           2              30              15       4
 3           3              15              12       4
 4           4               0               5       1
 5           5               6               5       1
 6           6              12               3       2
 7           7               6              21       3
 8           8              10               4       1
 9           9              30               4       2
10          10              30               6       2
# ℹ 206,199 more rows
# ℹ Use `print(n = ...)` to see more rows


## Check which items have a value of 0.

sum(rf_data$last_order_date == 0)
# ## result:
[1] 3255

sum(rf_data$count_order_num == 0)
# ## result:
[1] 0


## Adjust the scale to avoid outlines by log() function.
rf_data_scaled <- rf_data %>%
  mutate(R_log = log(last_order_date + 1),
         F_log = log(count_order_num + 1)) %>%
  select(R_log, F_log) %>%
  scale()


## Manage the NA value
rf_data_scaled <- na.omit(rf_data_scaled)

# ## Note: I used the na.omit() function to remove all NA (missing value) to avoid errors during the K-means process.



# ML: K-means process

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
# ## result:
# A tibble: 4 × 5
  cluster customer_level    avg_recency avg_frequency customer_count
    <int> <chr>                   <dbl>         <dbl>          <int>
1       1 New Customers            5.84          8.41          42611
2       2 Lost Customers          25.5           5.89          75184
3       3 Core Loyalists           5.48         42.3           37525
4       4 At-Risk Loyalists       21.1          18.8           50889


## Create the cluster_labels
cluster_labels <- segment_summary %>%
  select(cluster, customer_level)

print(cluster_labels)
# ## result:
# A tibble: 4 × 2
  cluster customer_level   
    <int> <chr>            
1       1 New Customers    
2       2 Lost Customers   
3       3 Core Loyalists   
4       4 At-Risk Loyalists


## Create a Customer Group
 
## Merge table between "rf_data & cluster_labels"
customer_cluster <- rf_data %>%
  select(customer_id, last_order_date, count_order_num, cluster) %>%
  left_join(cluster_labels, by = "cluster") %>%
  select(customer_id, cluster, customer_level, everything())

print(customer_cluster)
# ## result:
# A tibble: 206,209 × 5
   customer_id cluster customer_level    last_order_date count_order_num
         <int>   <int> <chr>                       <dbl>           <int>
 1           1       4 At-Risk Loyalists              14              11
 2           2       4 At-Risk Loyalists              30              15
 3           3       4 At-Risk Loyalists              15              12
 4           4       1 New Customers                   0               5
 5           5       1 New Customers                   6               5
 6           6       2 Lost Customers                 12               3
 7           7       3 Core Loyalists                  6              21
 8           8       1 New Customers                  10               4
 9           9       2 Lost Customers                 30               4
10          10       2 Lost Customers                 30               6
# ℹ 206,199 more rows
# ℹ Use `print(n = ...)` to see more rows


## Cluster no. 1 "New Customers"
new_customers <- customer_cluster %>%
  filter(cluster == 1)

print(new_customers)
# ## result:
# A tibble: 42,611 × 5
   customer_id cluster customer_level last_order_date count_order_num
         <int>   <int> <chr>                    <dbl>           <int>
 1           4       1 New Customers                0               5
 2           5       1 New Customers                6               5
 3           8       1 New Customers               10               4
 4          13       1 New Customers                8              13
 5          18       1 New Customers                7               7
 6          19       1 New Customers                8               9
 7          20       1 New Customers                7               4
 8          26       1 New Customers                7              12
 9          49       1 New Customers                2               9
10          56       1 New Customers                6              13
# ℹ 42,601 more rows
# ℹ Use `print(n = ...)` to see more rows


## Cluster no. 2 "Lost Customers"
lost_customers <- customer_cluster %>%
  filter(cluster == 2)

print(lost_customers)
# ## result:
# A tibble: 75,184 × 5
   customer_id cluster customer_level last_order_date count_order_num
         <int>   <int> <chr>                    <dbl>           <int>
 1           6       2 Lost Customers              12               3
 2           9       2 Lost Customers              30               4
 3          10       2 Lost Customers              30               6
 4          11       2 Lost Customers              30               7
 5          12       2 Lost Customers              30               5
 6          16       2 Lost Customers              26               6
 7          23       2 Lost Customers              30               5
 8          25       2 Lost Customers              30               3
 9          30       2 Lost Customers              22               9
10          32       2 Lost Customers              30               5
# ℹ 75,174 more rows
# ℹ Use `print(n = ...)` to see more rows


## Cluster no. 3 "Core Loyalists"
core_loyalists <- customer_cluster %>%
  filter(cluster == 3)

print(core_loyalists)
# ## result:
# A tibble: 37,525 × 5
   customer_id cluster customer_level last_order_date count_order_num
         <int>   <int> <chr>                    <dbl>           <int>
 1           7       3 Core Loyalists               6              21
 2          24       3 Core Loyalists               0              19
 3          27       3 Core Loyalists               4              82
 4          31       3 Core Loyalists               0              20
 5          36       3 Core Loyalists               7              37
 6          50       3 Core Loyalists               7              68
 7          52       3 Core Loyalists               3              28
 8          54       3 Core Loyalists               1              77
 9          63       3 Core Loyalists              13              40
10          67       3 Core Loyalists               5              25
# ℹ 37,515 more rows
# ℹ Use `print(n = ...)` to see more rows


## Cluster no. 4 "At-Risk Loyalists"
at_risk_loyalists <- customer_cluster %>%
  filter(cluster == 4)

print(at_risk_loyalists)
# ## result:
# A tibble: 50,889 × 5
   customer_id cluster customer_level    last_order_date count_order_num
         <int>   <int> <chr>                       <dbl>           <int>
 1           1       4 At-Risk Loyalists              14              11
 2           2       4 At-Risk Loyalists              30              15
 3           3       4 At-Risk Loyalists              15              12
 4          14       4 At-Risk Loyalists              11              14
 5          15       4 At-Risk Loyalists              14              22
 6          17       4 At-Risk Loyalists              30              41
 7          21       4 At-Risk Loyalists              28              34
 8          22       4 At-Risk Loyalists              30              15
 9          28       4 At-Risk Loyalists              13              24
10          29       4 At-Risk Loyalists              13              19
# ℹ 50,879 more rows
# ℹ Use `print(n = ...)` to see more rows



## Predictive Churn Analysis

## Create the cycle_time
# ## Note: I created the variable cycle_time to compare variable between the cycle_time (past behavior) and recency (current behavior) to filter out customers who likely to stop purchasing product.


cycle_time <- cus_seg %>%
  select(customer_id, date_diff) %>%
  group_by(customer_id) %>%
  summarise(avg_order_date = mean(date_diff, na.rm = TRUE), 
            .groups = 'drop')

print(cycle_time)
# ## result:
# A tibble: 206,209 × 2
   customer_id avg_order_date
         <int>          <dbl>
 1           1           19  
 2           2           16.3
 3           3           12.1
 4           4           13.8
 5           5           11.5
 6           6            9  
 7           7           10.4
 8           8           23.3
 9           9           22  
10          10           21.8
# ℹ 206,199 more rows
# ℹ Use `print(n = ...)` to see more rows


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
# ## result:
# A tibble: 206,209 × 7
   cus_id cluster customer_level    last_date n_order_num avg_order_date
    <int>   <int> <chr>                 <dbl>       <int>          <dbl>
 1      1       4 At-Risk Loyalists        14          11           19  
 2      2       4 At-Risk Loyalists        30          15           16.3
 3      3       4 At-Risk Loyalists        15          12           12.1
 4      4       1 New Customers             0           5           13.8
 5      5       1 New Customers             6           5           11.5
 6      6       2 Lost Customers           12           3            9  
 7      7       3 Core Loyalists            6          21           10.4
 8      8       1 New Customers            10           4           23.3
 9      9       2 Lost Customers           30           4           22  
10     10       2 Lost Customers           30           6           21.8
# ℹ 206,199 more rows
# ℹ 1 more variable: recency_vs_cycle <dbl>
# ℹ Use `print(n = ...)` to see more rows


## Target Groups Analysis (At-Risk Loyalists & Lost Customers)
check_cluster_2_4 <- cluster_cycle_analysis %>%
  filter(cluster %in% c(2, 4)) %>%
  mutate(customer_level = case_when(
    customer_level == "Lost Customers" ~ "Lost Cust",
    customer_level == "At-Risk Loyalists" ~ "Loyal Risk"
  )) %>%
  select(cus_id, cluster, customer_level, n_order_num, last_date, 
         avg_order_date, recency_vs_cycle)

# ## Note: I would like to focus only on cluster 2 and 4, as these two clusters have a high risk of customer churn.

print(check_cluster_2_4)
# ## result:
# A tibble: 126,073 × 7
   cus_id cluster customer_level n_order_num last_date avg_order_date
    <int>   <int> <chr>                <int>     <dbl>          <dbl>
 1      1       4 Loyal Risk              11        14           19  
 2      2       4 Loyal Risk              15        30           16.3
 3      3       4 Loyal Risk              12        15           12.1
 4      6       2 Lost Cust                3        12            9  
 5      9       2 Lost Cust                4        30           22  
 6     10       2 Lost Cust                6        30           21.8
 7     11       2 Lost Cust                7        30           20.5
 8     12       2 Lost Cust                5        30           25  
 9     14       4 Loyal Risk              14        11           21.2
10     15       4 Loyal Risk              22        14           10.8
# ℹ 126,063 more rows
# ℹ 1 more variable: recency_vs_cycle <dbl>
# ℹ Use `print(n = ...)` to see more rows


## Cluster 4: High-Value Churn Risk
cluster4_high_churn_risk <- check_cluster_2_4 %>%
  filter(cluster == 4,
         # >= 1.3 is more than 30% from average order date.
         recency_vs_cycle >= 1.30)

# ## Note 1: I selected date more than 30% of average order date is high risk for churn, because in case below 30%, it's possible customers may forgot or may not be available to purchase as it's not their holiday.

# ## Note 2: Inform the Marketing Team. 
# ## This is the group where we need to utilize the highest level of "Win-back Campaigns," such as personalized discount coupons or calling to survey customer satisfaction, because bringing this group back is far more worthwhile than acquiring new customers.

print(cluster4_high_churn_risk)
# ## result:
# A tibble: 29,761 × 7
   cus_id cluster customer_level n_order_num last_date avg_order_date
    <int>   <int> <chr>                <int>     <dbl>          <dbl>
 1      2       4 Loyal Risk              15        30           16.3
 2     17       4 Loyal Risk              41        30            8  
 3     21       4 Loyal Risk              34        28           10.5
 4     22       4 Loyal Risk              15        30           13.6
 5     38       4 Loyal Risk              13        30           21.8
 6     43       4 Loyal Risk              12        26           11.8
 7     62       4 Loyal Risk              11        29           16.8
 8     64       4 Loyal Risk              11        27           11.7
 9     65       4 Loyal Risk              15        30           14  
10     70       4 Loyal Risk              14        30           19.9
# ℹ 29,751 more rows
# ℹ 1 more variable: recency_vs_cycle <dbl>
# ℹ Use `print(n = ...)` to see more rows


## Cluster 2: Churn Risk
cluster2_high_churn_risk <- check_cluster_2_4 %>%
  filter(cluster == 2,
         last_date < 30) %>%
  mutate(num_of_day = last_date - avg_order_date) %>%
  filter(num_of_day > 2,
         num_of_day <= 5) %>%
  select(cus_id, cluster, customer_level, n_order_num, last_date,
         avg_order_date, num_of_day)

# ## Note 1: I selected last_date < 30, because this dataset has the max date of 30 days (if more than that, the data will still be recorded for 30 days as well), ensuring data integrity since the dataset caps intervals at 30 days. This allows for a more precise 'Early Warning' analysis, and for the group that has been there for 30 days or more, we can immediately conclude that they are "lost."

# ## Note 2: I selected 5 days because we wanted to capture customers during the Critical Window. If we let more than 5 days pass, the Cluster 4 customers (who didn't buy frequently to begin with) would be highly likely to be lost. Therefore, we used the 5-day criterion as an 'Early Warning System' for the marketing team to quickly intervene and rebuild relationships before the retention cost increases further.

# ## Note 3: Inform the Customer Service Team.
# ## For this customer group, we should send "Personalized Reminders" such as "We have a new product you might like" or "Your points are about to expire" to encourage them to engage again before they become permanently lost customers.

print(cluster2_high_churn_risk)
# ## result:
# A tibble: 5,427 × 7
   cus_id cluster customer_level n_order_num last_date avg_order_date
    <int>   <int> <chr>                <int>     <dbl>          <dbl>
 1      6       2 Lost Cust                3        12           9   
 2     16       2 Lost Cust                6        26          21.8 
 3     88       2 Lost Cust                8        23          18.3 
 4    135       2 Lost Cust                5        17          13.2 
 5    144       2 Lost Cust                8        12           7.29
 6    172       2 Lost Cust                6        14          10.6 
 7    183       2 Lost Cust                5        19          15.2 
 8    215       2 Lost Cust                6        29          26.2 
 9    291       2 Lost Cust                5        17          12.8 
10    340       2 Lost Cust                6        14          10   
# ℹ 5,417 more rows
# ℹ 1 more variable: num_of_day <dbl>
# ℹ Use `print(n = ...)` to see more rows



# Chart

## Prepare data set 1 (Total Count)
total_data <- segment_summary %>%
  select(customer_level, customer_count) %>%
  mutate(Type = "Total in Segment")

print(total_data)
# ## result:
# A tibble: 4 × 3
  customer_level    customer_count Type            
  <chr>                      <int> <chr>           
1 New Customers              42611 Total in Segment
2 Lost Customers             75184 Total in Segment
3 Core Loyalists             37525 Total in Segment
4 At-Risk Loyalists          50889 Total in Segment


## Prepare data set 2 (High Churn Risk)
risk_count_data <- data.frame(
  customer_level = c("Lost Customers", "At-Risk Loyalists"),
  customer_count = c(nrow(cluster2_high_churn_risk), 
                     nrow(cluster4_high_churn_risk)),
  Type = "High Churn Risk"
)

print(risk_count_data)
# ## result:
     customer_level customer_count            Type
1    Lost Customers           5427 High Churn Risk
2 At-Risk Loyalists          29761 High Churn Risk


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
# ## result:
# A tibble: 6 × 3
  customer_level    customer_count Type            
  <fct>                      <int> <fct>           
1 New Customers              42611 Total in Segment
2 Lost Customers             75184 Total in Segment
3 Core Loyalists             37525 Total in Segment
4 At-Risk Loyalists          50889 Total in Segment
5 Lost Customers              5427 High Churn Risk 
6 At-Risk Loyalists          29761 High Churn Risk 


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
# ## Note: I exported the data to send customer information to Marketing and Customer Service Team.

write.csv(cluster2_high_churn_risk, "cluster2_high_churn_risk.csv", row.names = F)
write.csv(cluster4_high_churn_risk, "cluster4_high_churn_risk.csv", row.names = F)
write.csv(cluster_cycle_analysis, "cluster_cycle_analysis.csv", row.names = F)
