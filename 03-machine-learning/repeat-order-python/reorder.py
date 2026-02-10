# Project: Instacart Repeat Order Prediction


# 📢 Data Preparation

# --- Library Imports ---
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import gdown


# --- Data Loading ---
## Since the dataset is large, I fetch the data directly from Google Drive.
## In this project, I use the following files:
## 1. orders 2. order_products__prior 3. order_products__train 4. products 5. aisles
## Note 1: I will use the first 3 files (orders, prior, train) for Feature Engineering process.
## Note 2: I will use the last 2 files (products, aisles) for Error Analysis (False Negatives / False Positives) process.

# --- Download Example ---
## file_id = 'YOUR_FILE_ID'
## gdown.download(f'https://drive.google.com/uc?id={file_id}', 'orders.csv', quiet=False)


# --- Store dataset in Dataframes ---
orders = pd.read_csv('orders.csv', usecols=['order_id', 'user_id', 'eval_set', 'order_number', 'days_since_prior_order'])
## op_prior = pd.read_csv('order_products__prior.csv')
## op_train = pd.read_csv('order_products__train.csv')


# --- Merging Tables ---

## Merge 'op_prior' and 'orders' tables to prepare the base for Features Engineering (X).
prior_orders = op_prior.merge(
    orders[orders['eval_set'] == 'prior'][['order_id', 'user_id']],
    on = 'order_id',
    how = 'inner'
)

print(prior_orders.head())
# ## result:
#    order_id  product_id  add_to_cart_order  reordered  user_id
# 0         2       33120                  1          1   202279
# 1         2       28985                  2          1   202279
# 2         2        9327                  3          0   202279
# 3         2       45918                  4          1   202279
# 4         2       30035                  5          0   202279


## Merge 'op_train' and 'orders' tables to find the Target Variable (Y=1 (in reordered column)).
train_orders = op_train.merge(
    orders[orders['eval_set'] == 'train'][['order_id', 'user_id']],
    on = 'order_id',
    how = 'inner'
)

print(train_orders.head())
# ## result:
#    order_id  product_id  user_id
# 0         1       49302   112108
# 1         1       11109   112108
# 2         1       10246   112108
# 3         1       49683   112108
# 4         1       43633   112108



# 📢 Features Engineering

# --- 🔑 User Features (Customer level) ---

cust_features = prior_orders.groupby('user_id').aggregate(
    cust_total_prod = ('order_id', 'count'),
    cust_unique_prod = ('product_id', 'nunique'),
).reset_index()

print(cust_features.head())
# ## result:
#   user_id  cust_total_prod  cust_unique_prod
# 0        1               59                18
# 1        2              195               102
# 2        3               88                33
# 3        4               18                17
# 4        5               37                23


cust_orders_stats = orders[orders['eval_set'].isin(['prior', 'train'])].groupby('user_id').aggregate(
    user_total_orders = ('order_id', 'count'),
    user_avg_days_between_orders = ('days_since_prior_order', 'mean'),
).reset_index()

print(cust_orders_stats.head())
# ## result:
#    user_id  user_total_orders  user_avg_days_between_orders
# 0        1                 11                     19.000000
# 1        2                 15                     16.285714
# 2        3                 12                     12.090909
# 3        4                  5                     13.750000
# 4        5                  5                     11.500000


## Merge the 'cust_features' and 'cust_orders_stats' tables.
cust_features = cust_features.merge(
    cust_orders_stats,
    on = 'user_id',
    how = 'left'
)

print(cust_features.head())
# ## result:
#    user_id  cust_total_prod  cust_unique_prod  user_total_orders  user_avg_days_between_orders
# 0        1               59                18                 11                     19.000000
# 1        2              195               102                 15                     16.285714
# 2        3               88                33                 12                     12.090909
# 3        4               18                17                  5                     13.750000
# 4        5               37                23                  5                     11.500000



# --- 🔑 Product Features (Product level) ---

prod_features = prior_orders.groupby('product_id').aggregate(
    prod_total_pur = ('order_id', 'count'),
    prod_reorder_rate = ('reordered', 'mean'),
).reset_index()

print(prod_features.head())
# ## result:
#    product_id  prod_total_pur  prod_reorder_rate
# 0           1            1852           0.613391
# 1           2              90           0.133333
# 2           3             277           0.732852
# 3           4             329           0.446809
# 4           5              15           0.600000


# --- 🔑 User - Product Interaction Features
  
## Prepare table to calculating about "Time period" and "Order Number".
## Merge the 'prior_orders' and 'orders' tables.
prior_features_base = prior_orders.merge(
    orders[['order_id', 'order_number', 'days_since_prior_order']],
    on = 'order_id',
    how = 'left'
)

print(prior_features_base.head())
# ## result:
#    order_id  product_id  add_to_cart_order  reordered  user_id  order_number  days_since_prior_order
# 0         2       33120                  1          1   202279             3                     8.0
# 1         2       28985                  2          1   202279             3                     8.0   
# 2         2        9327                  3          0   202279             3                     8.0   
# 3         2       45918                  4          1   202279             3                     8.0   
# 4         2       30035                  5          0   202279             3                     8.0   

     
up_features = prior_features_base.groupby(['user_id', 'product_id']).aggregate(
    count_orders = ('order_id', 'count'),
    prod_reorder_ratio = ('reordered', 'mean'),
    last_order_number = ('order_number', 'max'),
    avg_add_to_cart = ('add_to_cart_order', 'mean')
).reset_index()

print(up_features.head())
# ## result:
#    user_id  product_id  count_orders  prod_reorder_ratio  last_order_number  avg_add_to_cart
# 0        1         196            10            0.900000                 10         1.400000   
# 1        1       10258             9            0.888889                 10         3.333333   
# 2        1       10326             1            0.000000                  5         5.000000   
# 3        1       12427            10            0.900000                 10         3.300000   
# 4        1       13032             3            0.666667                 10         6.333333   


## Calculate 'days_since_prior_order' column, focusing only on reordered products (reordered = 1).
reorder_time_features = prior_features_base[prior_features_base['reordered'] == 1].groupby(
    ['user_id', 'product_id']).aggregate(
        total_days_between_reorder = ('days_since_prior_order', 'sum'),
        count_reorder = ('order_id', 'count')
    ).reset_index()

## To find the average of repeated orders.
reorder_time_features['avg_days_between_reorder'] = (
    reorder_time_features['total_days_between_reorder'] /
    reorder_time_features['count_reorder']
)

print(reorder_time_features.head())
# ## result:
#    user_id  product_id  total_days_between_reorder  count_reorder     avg_days_between_reorder
# 0        1         196                       176.0              9                    19.555556
# 1        1       10258                       161.0              8                    20.125000
# 2        1       12427                       176.0              9                    19.555556
# 3        1       13032                        50.0              2                    25.000000
# 4        1       13176                        28.0              1                    28.000000


## Merge 'up_features' and 'reorder_time_features' tables.
up_features = up_features.merge(
    reorder_time_features[['user_id', 'product_id', 'avg_days_between_reorder']],
    on = ['user_id', 'product_id'],
    how = 'left'
)

print(up_features.head())
# ## result:
#    user_id  product_id  count_orders  prod_reorder_ratio  last_order_number  avg_add_to_cart  avg_days_between_reorder
# 0        1         196            10            0.900000                 10         1.400000                 19.555556   
# 1        1       10258             9            0.888889                 10         3.333333                 20.125000   
# 2        1       10326             1            0.000000                  5         5.000000                       NaN   
# 3        1       12427            10            0.900000                 10         3.300000                 19.555556   
# 4        1       13032             3            0.666667                 10         6.333333                 25.000000   


## Replace the NaN value with the number 30 in the 'avg_days_between_reorder' column (Feature Engineering).
## NaN indicates products that have never been reordered.
## I impute with 30 days (the typical max order interval) to represent a long/indefinite reorder cycle, preventing model bias toward zero.
up_features['avg_days_between_reorder'] = up_features['avg_days_between_reorder'].fillna(30)

print(up_features.head())
# ## result:
#    user_id  product_id  count_orders  prod_reorder_ratio  last_order_number  avg_add_to_cart  avg_days_between_reorder
# 0        1         196            10            0.900000                 10         1.400000                 19.555556
# 1        1       10258             9            0.888889                 10         3.333333                 20.125000
# 2        1       10326             1            0.000000                  5         5.000000                 30.000000
# 3        1       12427            10            0.900000                 10         3.300000                 19.555556   
# 4        1       13032             3            0.666667                 10         6.333333                 25.000000   



# 📢 Training Set

# --- Training Dataset: Create training dataset by negative sampling ---

## Positive Cases (Y=1)
positive_cases = train_orders[['user_id', 'product_id']].copy()
positive_cases['reordered_next'] = 1

print(positive_cases)
# ## result:
#         user_id  product_id  reordered_next
# 0         112108       49302               1
# 1         112108       11109               1
# 2         112108       10246               1
# 3         112108       49683               1
# 4         112108       43633               1
# ...          ...         ...             ...
# 1384612   169679       14233               1
# 1384613   169679       35548               1
# 1384614   139822       35951               1
# 1384615   139822       16953               1
# 1384616   139822        4724               1

# [1384617 rows x 3 columns]


## Negative Sampling (Y=0).
all_prior_user_prod = up_features[['user_id', 'product_id']].copy()


## Filter out data that does not repeat purchases in the "Training set".
merged_all = all_prior_user_prod.merge(
    positive_cases,
    on = ['user_id', 'product_id'],
    how = 'left',
    suffixes = ('_prior', '_train'))

merged_all['reordered_next'] = merged_all['reordered_next'].fillna(0)

negative_pool = merged_all[merged_all['reordered_next'] == 0].drop(columns = ['reordered_next'])

print(negative_pool)
# ## result:
#           user_id  product_id
# 2               1       10326
# 3               1       12427
# 5               1       13176
# 6               1       14084
# 7               1       17122
# ...           ...         ...
# 13307948   206209       43961
# 13307949   206209       44325
# 13307950   206209       48370
# 13307951   206209       48697
# 13307952   206209       48742

# [12479129 rows x 2 columns]


## Perform 1:1 negative sampling (with positive_cases)
N = len(positive_cases)
negative_sample = negative_pool.sample(n = min(N, len(positive_cases)), random_state = 22)
negative_sample['reordered_next'] = 0

print(negative_sample)
# ## result:
#          user_id  product_id  reordered_next
# 8204474   126808       28805               0
# 3888722    60302       23032               0
# 1361292    21288        1405               0
# 9646192   149360       45210               0
# 3289605    50986       37514               0
# ...          ...         ...             ...
# 3349504    51916        9119               0
# 1301497    20361       48745               0
# 7229772   111550       42495               0
# 6003210    92681       38881               0
# 2107550    32790       26384               0

# [1384617 rows x 3 columns]


## Merge tables between 'positive_cases' and 'negative_sample'.
final_train_data = pd.concat([positive_cases, negative_sample], ignore_index = True)

print(final_train_data)
# ## result:
#          user_id  product_id  reordered_next
# 0         112108       49302               1
# 1         112108       11109               1
# 2         112108       10246               1
# 3         112108       49683               1
# 4         112108       43633               1
# ...          ...         ...             ...
# 2769229    51916        9119               0
# 2769230    20361       48745               0
# 2769231   111550       42495               0
# 2769232    92681       38881               0
# 2769233    32790       26384               0

# [2769234 rows x 3 columns]


































































