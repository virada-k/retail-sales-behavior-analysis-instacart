# Project: Instacart Repeat Order Prediction


# 📢 Data Preparation

# --- 📂 Library Imports ---
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import gdown


# --- 📂 Data Loading ---
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


# --- 🔑 User - Product Interaction Features ---
  
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

# --- 🏷️ Training Dataset: Create training dataset by negative sampling ---

## Positive Cases (Y=1)
positive_cases = train_orders[['user_id', 'product_id']].copy()
positive_cases['reordered_next'] = 1

print(positive_cases.head())
# ## result:
#         user_id  product_id  reordered_next
# 0         112108       49302               1
# 1         112108       11109               1
# 2         112108       10246               1
# 3         112108       49683               1
# 4         112108       43633               1


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


## Perform 1:1 negative sampling (with positive_cases)
N = len(positive_cases)
negative_sample = negative_pool.sample(n = min(N, len(positive_cases)), random_state = 22)
negative_sample['reordered_next'] = 0

print(negative_sample.head())
# ## result:
#          user_id  product_id  reordered_next
# 8204474   126808       28805               0
# 3888722    60302       23032               0
# 1361292    21288        1405               0
# 9646192   149360       45210               0
# 3289605    50986       37514               0


## Merge tables between 'positive_cases' and 'negative_sample'.
final_train_data = pd.concat([positive_cases, negative_sample], ignore_index = True)

print(final_train_data.head())
# ## result:
#          user_id  product_id  reordered_next
# 0         112108       49302               1
# 1         112108       11109               1
# 2         112108       10246               1
# 3         112108       49683               1
# 4         112108       43633               1


## Merge all 3 features.
final_train_data = final_train_data.merge(
    cust_features,
    on = 'user_id',
    how = 'left'
)

final_train_data = final_train_data.merge(
    prod_features,
    on = 'product_id',
    how = 'left'
)

final_train_data = final_train_data.merge(
    up_features,
    on = ['user_id', 'product_id'],
    how = 'left'
)


# Replace the NaN value with the number 0 in count_orders column.
final_train_data.fillna(0, inplace = True)

print(final_train_data.head())
# ## result:
#    user_id  product_id  reordered_next  cust_total_prod  cust_unique_prod  user_total_orders  user_avg_days_between_orders  prod_total_pur  \
# 0   112108       49302               1               21                12                  4                     10.333333           163.0  
# 1   112108       11109               1               21                12                  4                     10.333333          4472.0 
# 2   112108       10246               1               21                12                  4                     10.333333         23826.0
# 3   112108       49683               1               21                12                  4                     10.333333         97315.0
# 4   112108       43633               1               21                12                  4                     10.333333           653.0

#    prod_reorder_rate  count_orders  prod_reorder_ratio  last_order_number  avg_add_to_cart  avg_days_between_reorder
# 0           0.619632           2.0                 0.5                2.0              2.5                       7.0
# 1           0.713775           2.0                 0.5                2.0              4.0                       7.0 
# 2           0.524553           0.0                 0.0                0.0              0.0                       0.0 
# 3           0.691702           0.0                 0.0                0.0              0.0                       0.0 
# 4           0.477795           2.0                 0.5                3.0              3.5                      15.0  


print(f"Final data size for training model: {len(final_train_data):,} rows")
# ## result:
# Final data size for training model: 2,769,234 rows



# --- 🏷️ Training Logistic Regression Model (4 main features) ---

core_features = [
    'count_orders',
    'avg_days_between_reorder',
    'prod_reorder_rate',
    'user_avg_days_between_orders'
]


## Check and Manage Outlier using IQR method (Capping)
for feature in core_features:

    # Calculate Q1, Q3 and IQR.
    Q1 = final_train_data[feature].quantile(0.25)
    Q3 = final_train_data[feature].quantile(0.75)
    IQR = Q3 - Q1
    # Calculate Upper Bound
    upper_bound = Q3 + 1.5 * IQR

    # Check Outlier Count
    outlier_count = final_train_data[final_train_data[feature] > upper_bound].shape[0]

    # Print status before capping
    print(f"--- Feature: {feature} ---")
    print(f"--- Upper Bound: {upper_bound:.2f}") # use .2 for clarity in displaying decimal points
    print(f"Outliers found: {outlier_count} row")

    # Apply Capping (Winsorizing) only if outliers are found.
    if outlier_count > 0:
        # Capping the outlier
        final_train_data[feature] = np.where(
            final_train_data[feature] > upper_bound,
            upper_bound,
            final_train_data[feature]
        )
        print(f"--- Outliers successfully capped at {upper_bound:.2f} ---")

# ## result:
# --- Feature: count_orders ---
# --- Upper Bound: 6.00
# Outliers found: 264368 row
# --- Outliers successfully capped at 6.00 ---
# --- Feature: avg_days_between_reorder ---
# --- Upper Bound: 68.00
# Outliers found: 0 row
# --- Feature: prod_reorder_rate ---
# --- Upper Bound: 0.97
# Outliers found: 0 row
# --- Feature: user_avg_days_between_orders ---
# --- Upper Bound: 34.27
# Outliers found: 0 row


x = final_train_data[core_features]
y = final_train_data['reordered_next']


## Split Training and Validation data.
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state = 22)

## x_train, x_val = features (cause) | y_train, y_val = target(0, 1) (effect)


## Create training model.
model = LogisticRegression(solver = 'saga', # 'saga' is an algorithm suitable for big data.
                           max_iter = 1000,
                           random_state = 22,
                           n_jobs = -1)

model.fit(x_train, y_train)
# ## result:
# LogisticRegression
# LogisticRegression(max_iter=1000, n_jobs=-1, random_state=22, solver='saga')


print(y_val.value_counts())
# ## result:
# reordered_next
# 1    277490
# 0    276357
# Name: count, dtype: int64



# --- 📊 Create Bar Chart to show the 'reordered_next' column from 'y_val' ---

# --- 📂 Library Imports ---
import seaborn as sns
import matplotlib.pyplot as plt


# --- 📂 Prepare data ---

## Count values (reordered_next) ​​to create a graph.
data_to_plot = pd.Series(y_val).value_counts().reset_index()

print(data_to_plot)
# ## result:
#    reordered_next   count
# 0               1  277490
# 1               0  276357


## Edit column name.
data_to_plot.columns = ['Reordered', 'Count']


## Convert number to text.
data_to_plot['Reordered'] = data_to_plot['Reordered'].astype(str).replace(
    {'0': 'Not Reordered',
     '1': 'Reordered'}
)

print(data_to_plot)
# ## result:
#        Reordered   Count
# 0      Reordered  277490
# 1  Not Reordered  276357



# --- 📊 Create a Chart ---

## Set Figure Size (Canvas Size).
plt.figure(figsize = (6, 4))
sns.barplot(x = 'Reordered',
            y = 'Count',
            data = data_to_plot)

## Customize the graph.
plt.title('Distribution of True Reordered Labels')  # Chart show 'true reordered' from Validation set.
plt.xlabel('Reordered Status')  # Merge between 'Order_id' and 'Product_id', it means order per product.
plt.ylabel('Number of Orders')
plt.show()



# 📢 Validation Set

# --- 🏷️ Evaluation and Interpretation ---

y_pred_proba = model.predict_proba(x_val)[: , 1]

## Report the result (ROC AUC Score).
print("\n--- 4 Core Features ---")
print(f"ROC AUC Score: {roc_auc_score(y_val, y_pred_proba):.4f}")
# ## result:
# --- 4 Core Features ---
# ROC AUC Score: 0.8128


## Show feature importance (Insight).
feature_importance = pd.DataFrame({
    'Feature': core_features,
    'Coefficient': model.coef_[0]
}).sort_values(by = 'Coefficient', ascending = False)

print("\n--- Feature Importance (Coefficient) ---")
print(feature_importance)
# ## result:
# --- Feature Importance (Coefficient) ---
#                         Feature  Coefficient
# 2             prod_reorder_rate     2.136447
# 3  user_avg_days_between_orders     0.109579
# 0                  count_orders    -0.056393
# 1      avg_days_between_reorder    -0.105589



# --- 🏷️ Optimal Threshold Identification ---

from sklearn.metrics import f1_score ## add f1_score

## Create y_pred (0 or 1) using the specified threshold.
threshold = 0.40
y_pred = (y_pred_proba > threshold).astype(int)

print(f"F1-Score @ Threshold {threshold}: {f1_score(y_val, y_pred):.4f}")
# ## result:
# F1-Score @ Threshold 0.4: 0.7476



# --- 🏷️ Error Analysis (False Negatives / False Positives) ---

# --- 📂 Download the 'products' and 'aisles' tables ---
## Since the dataset is large, I fetch the data directly from Google Drive.
## In this process, I use the following files:
## 1. products 2. aisles
## Note: For Error Analysis (False Negatives / False Positives) process.


# --- Store dataset in Dataframes ---
## products = pd.read_csv('products.csv')
## aisles = pd.read_csv('aisles.csv')


# --- Prepare the Validation dataframe ---

## Combine x_val and y_val table to create a dataframe.
validation_df = x_val.copy()
validation_df['reordered_actual'] = y_val

print(validation_df.head())
# ## result:
#          count_orders  avg_days_between_reorder  prod_reorder_rate  user_avg_days_between_orders  reordered_actual
# 527041            1.0                 30.000000           0.521021                     11.190476                 1
# 1694697           1.0                 30.000000           0.619973                     12.285714                 0
# 2111176           1.0                 30.000000           0.715237                      8.000000                 0   
# 2639205           1.0                 30.000000           0.854342                      6.100000                 0   
# 2440381           6.0                  8.166667           0.650427                      7.020833                 0   


## Add the product_id column back into validation_df.
product_id_val = final_train_data.loc[x_val.index, 'product_id']
validation_df['product_id'] = product_id_val


## Predict the outcome (y_pred) on x_val.
validation_df['reordered_proba'] = model.predict_proba(x_val)[:, 1]


## Set the prediction result (y_pred) by Threshold @ 0.40.
threshold = 0.40
validation_df['reordered_pred'] = (validation_df['reordered_proba'] > threshold).astype(int)

print(validation_df.head())
# ## result:
#          count_orders  avg_days_between_reorder  prod_reorder_rate   user_avg_days_between_orders  reordered_actual  product_id \
# 527041            1.0                 30.000000           0.521021                      11.190476                 1       40299  
# 1694697           1.0                 30.000000           0.619973                      12.285714                 0       31717
# 2111176           1.0                 30.000000           0.715237                       8.000000                 0       33845
# 2639205           1.0                 30.000000           0.854342                       6.100000                 0       29447
# 2440381           6.0                  8.166667           0.650427                       7.020833                 0        9387   

#          reordered_proba  reordered_pred  
# 527041          0.158635               0  
# 1694697         0.208004               0  
# 2111176         0.167549               0  
# 2639205         0.180331               0  
# 2440381         0.543526               1 



# --- Merging table ---

## Merge 3 tables between validation_df, products and aisles.
products_info = products[['product_id', 'aisle_id']].drop_duplicates()
aisles_info = aisles[['aisle_id', 'aisle']].drop_duplicates()

validation_df = validation_df.merge(
    products_info,
    on = 'product_id',
    how = 'left'
)

validation_df = validation_df.merge(
    aisles_info,
    on = 'aisle_id',
    how = 'left'
)


## Edit the column names 'aisle_id' and 'aisle'.
validation_df = validation_df.rename(columns = {
    'aisle_id': 'category_id',
    'aisle': 'category_name'
})



# --- 📌 Error Analysis (FN / FP) ---

## False Negatives (FN): Actual = 1, Predicted = 0 (Missed Opportunity).
df_fn = validation_df[
    (validation_df['reordered_actual'] == 1) &
    (validation_df['reordered_pred'] == 0)
]

print(df_fn.head())
# ## result:
#         count_orders  avg_days_between_reorder  prod_reorder_rate  user_avg_days_between_orders  reordered_actual  product_id \
# 0                1.0                      30.0           0.521021                     11.190476                 1       40299
# 12               1.0                      30.0           0.291203                     11.750000                 1       18598
# 28               2.0                      30.0           0.603038                     20.333333                 1       28199
# 34               2.0                      30.0           0.690094                     12.000000                 1       33548  
# 38               1.0                      30.0           0.081888                     13.333333                 1        6020  

#         reordered_proba  reordered_pred  category_id               category_name
# 0              0.158635               0          128        tortillas flat bread
# 12             0.109282               0           19               oils vinegars
# 28             0.366393               0          123  packaged vegetables fruits
# 34             0.218421               0          120                      yogurt
# 38             0.085349               0          104           spices seasonings



## Top 10 Category Names that cause False Negatives.
top10_fn_category = df_fn.groupby('category_name')['product_id'].count().sort_values(ascending=False).head(10)

print("Top 10 Category Names that cause False Negatives (Lost Sales Opportunity):\n", top10_fn_category)
# ## result:
# Top 10 Category Names that cause False Negatives (Lost Sales Opportunity):
#  category_name
# fresh vegetables                 5282
# fresh fruits                     3475
# packaged vegetables fruits       2543
# packaged cheese                  1486
# yogurt                           1345
# chips pretzels                   1068
# ice cream ice                     842
# frozen produce                    837
# water seltzer sparkling water     743
# crackers                          714
# Name: product_id, dtype: int64


## False Positives (FP): Actual = 0, Predicted = 1 (Wrong recommendation/wasted cost).
df_fp = validation_df[
    (validation_df['reordered_actual'] == 0) &
    (validation_df['reordered_pred'] == 1)
]

print(df_fp.head())
# ## result:
#         count_orders  avg_days_between_reorder  prod_reorder_rate  user_avg_days_between_orders  reordered_actual  product_id  \
# 4                6.0                  8.166667           0.650427                      7.020833                 0        9387
# 14               1.0                 30.000000           0.652174                     24.000000                 0       19064
# 18               6.0                 24.600000           0.510179                     22.454545                 0       20754
# 19               2.0                 15.000000           0.550313                     14.285714                 0        5460 
# 24               2.0                 15.000000           0.476649                     14.384615                 0       31506  

#         reordered_proba  reordered_pred  category_id         category_name  
# 4              0.543526               1           24          fresh fruits  
# 14             0.503859               1           33          kosher foods  
# 18             0.457835               1           37         ice cream ice  
# 19             0.564828               1           36                butter  
# 24             0.528529               1           19         oils vinegars  


## Top 10 category names that cause False Positives.
top10_fp_category = df_fp.groupby('category_name')['product_id'].count().sort_values(ascending=False).head(10)

print("Top 10 Category Names that cause False Positives (Wasted Recommendations):\n", top10_fp_category)
# ## result:
# Top 10 Category Names that cause False Positives (Wasted Recommendations):
#  category_name
# fresh vegetables                 13459
# fresh fruits                     12019
# packaged vegetables fruits        6460
# yogurt                            5113
# packaged cheese                   3659
# chips pretzels                    2720
# water seltzer sparkling water     2641
# milk                              2452
# bread                             2085
# soy lactosefree                   2072
# Name: product_id, dtype: int64



# --- 🏷️ Confusion Matrix ---

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

## Create the function for calculate all metrics.
def calculate_metrics(y_true, y_pred, model_name = "Model"):
  # 1.1 Create a confusion matrix (cm), to compare the actual value (y_true) with the predicted value (y_pred).
  cm = confusion_matrix(y_true, y_pred)

  # 1.2 Use .reval() to extract the value of "Negative, Positive" from Matrix.
  # TN = True Negative, FP = False Positive, FN = False Negative, TP = True Positive
  # NOTE: Sklearn CM format: [[TN, FP], [FN, TP]]
  TN, FP, FN, TP = cm.ravel()

  # 1.3 Calculate Metrics.
  # Accuracy: (TN + TP) / Total (TP + TN + FP + FN)
  accuracy = accuracy_score(y_true, y_pred)

  # Precision: TP / (TP + FP)
  precision = precision_score(y_true, y_pred)

  # Recall (Sensitivity): TP / (TP + FN)
  recall = recall_score(y_true, y_pred)

  # Specificity: TN / (TN + FP)
  # It is the model's ability to correctly predict '0'.
  specificity = TN / (TN + FP)

  # F1 score: 2 x (Precision x Recall) / (Precision + Recall)
  f1 = f1_score(y_true, y_pred)

  # 1.4 Create a datafame for result.
  results_df = pd.DataFrame({
      'Metric': ['Accuracy', 'Precision', 'Recall/Sensitivity', 'Specificity', 'F1 Score'],
      model_name: [accuracy, precision, recall, specificity, f1]
  }).set_index('Metric')

  print(f"\n--- Confision Matrix for {model_name} ---")

  # Display calculation results in an easy-to-read format.
  print("\n--- Breakdown of Outcomes ---")
  print(f"True Negative (TN): {TN}")
  print(f"False Positive (FP): {FP}")
  print(f"False Negative (FN): {FN}")
  print(f"True Positive (TP): {TP}")

  print("\n--- Summary Metrics ---")
  print(results_df.round(4))

  return cm, results_df

# --- 📌 Show results ---

y_true_labels = y_val

y_pred_at_04 = (model.predict_proba(x_val)[:, 1] >= 0.4).astype(int)

y_pred_labels = y_pred_at_04

## Call the calculate_metrics.
cm_results, metrics_summary_df = calculate_metrics(
    y_true = y_true_labels,
    y_pred = y_pred_labels,
    model_name = "Logistic Model after Outlier Capping"
)

# ## result:
# --- Confision Matrix for Logistic Model after Outlier Capping ---

# --- Breakdown of Outcomes ---
# True Negative (TN): 164302
# False Positive (FP): 112055
# False Negative (FN): 44970
# True Positive (TP): 232520

# --- Summary Metrics ---
#                     Logistic Model after Outlier Capping
# Metric                                                  
# Accuracy                                          0.7165
# Precision                                         0.6748
# Recall/Sensitivity                                0.8379
# Specificity                                       0.5945
# F1 Score                                          0.7476



# --- 🏷️ Error Analysis: Checking for False Negatives results ---
## FN (False Negative) = Missed sales opportunities


## Combine the x_val (Feature Engineer) and the y_val (Target Variable) tables.
df_val = x_val.copy()
df_val['y_true'] = y_val.values


## Add the y_pred column (threshold 0.4) into the df_val.
df_val['y_pred'] = y_pred_labels

print(df_val.head())
# ## result:
#          count_orders  avg_days_between_reorder  prod_reorder_rate  user_avg_days_between_orders  y_true  y_pred 
# 527041            1.0                 30.000000           0.521021                     11.190476       1       0 
# 1694697           1.0                 30.000000           0.619973                     12.285714       0       0    
# 2111176           1.0                 30.000000           0.715237                      8.000000       0       0  
# 2639205           1.0                 30.000000           0.854342                      6.100000       0       0  
# 2440381           6.0                  8.166667           0.650427                      7.020833       0       1 


## Create boolean mask and pull customer names (FN).

# FN is y_true = 1 and y_pred = 0
fn_mask = (df_val['y_true'] == 1) & (df_val['y_pred'] == 0)

print(fn_mask.head())
# ## result:
# 527041      True
# 1694697    False
# 2111176    False
# 2639205    False
# 2440381    False
# dtype: bool


## Filter
df_fn_list = df_val[fn_mask]



# --- Merging table ---

df_fn_list_reset = df_fn_list.reset_index()

print(df_fn_list_reset.head())
# ## result:
#     index  count_orders  avg_days_between_reorder  prod_reorder_rate  user_avg_days_between_orders  y_true  y_pred
# 0  527041           1.0                      30.0           0.521021                     11.190476       1       0 
# 1   16552           1.0                      30.0           0.291203                     11.750000       1       0
# 2  681850           2.0                      30.0           0.603038                     20.333333       1       0
# 3  809304           2.0                      30.0           0.690094                     12.000000       1       0
# 4  308569           1.0                      30.0           0.081888                     13.333333       1       0  


df_fn_list_reset = df_fn_list.reset_index()

## Revise index column to primary key.
df_fn_list_reset = df_fn_list_reset.rename(columns = {'index': 'order_product_key'})


## Merge table with 'op_train' to get 'order_id' and 'product_id' columns.
op_train_key = op_train.copy()
op_train_key = op_train_key.reset_index().rename(columns = {'index': 'order_product_key'})
op_train_key = op_train_key[['order_product_key', 'order_id', 'product_id']]

df_fn_with_order_id = df_fn_list_reset.merge(
    op_train_key,
    on = 'order_product_key',
    how = 'left'
)

print(df_fn_with_order_id.head())
# ## result:
#    order_product_key  count_orders  avg_days_between_reorder  prod_reorder_rate  user_avg_days_between_orders  y_true  y_pred  \
# 0             527041           1.0                      30.0           0.521021                     11.190476       1       0
# 1              16552           1.0                      30.0           0.291203                     11.750000       1       0
# 2             681850           2.0                      30.0           0.603038                     20.333333       1       0
# 3             809304           2.0                      30.0           0.690094                     12.000000       1       0
# 4             308569           1.0                      30.0           0.081888                     13.333333       1       0

#    order_id  product_id
# 0   1294839       40299
# 1     39970       18598
# 2   1674413       28199
# 3   1996250       33548
# 4    751608        6020


## Merge table with 'orders' to get 'user_id' column.
df_fn_with_ids = df_fn_with_order_id.merge(
    orders[['order_id', 'user_id']],
    on = 'order_id',
    how = 'left'
)


## Merge table with 'products' to get 'product_name' column.
fn_targeting_list = df_fn_with_ids.merge(
    products[['product_id', 'product_name']],
    on = 'product_id',
    how = 'left'
)



# --- 📌 False Negative list for checking ---

fn_final_list = fn_targeting_list[[
    'order_id',
    'user_id',
    'product_id',
    'product_name',
    'y_true',
    'y_pred'
]]

print("--- FN list for checking ---")
print(fn_final_list.head())
# ## result:
# --- FN list for checking ---
#    order_id  user_id  product_id                             product_name  y_true  y_pred 
# 0   1294839   205612       40299                Soft Taco Flour Tortillas       1       0
# 1     39970   190147       18598       Expeller Pressed Coconut Oil Spray       1       0
# 2   1674413   195355       28199                         Clementines, Bag       1       0
# 3   1996250    41783       33548  Peach on the Bottom Nonfat Greek Yogurt       1       0
# 4    751608    64424        6020               Organic Crushed Red Pepper       1       0 



# 📢 Test Set

# --- 📂 Download and Prepare the "Test Set" ---

## Download the 'testset' dataset.
orders_test = orders[orders['eval_set'] == 'test'][['order_id', 'user_id']]


test_user_products = up_features[['user_id', 'product_id']].copy()


## Merge the 'test_user_products' and 'orders_test' tables.
test_set = test_user_products.merge(
    orders_test[['user_id', 'order_id']],
    on = 'user_id',
    how = 'inner'
)

print(test_set.head())
# ## result:
#    user_id  product_id  order_id
# 0        3         248   2774568
# 1        3        1005   2774568
# 2        3        1819   2774568
# 3        3        7503   2774568
# 4        3        8021   2774568


print(f"Size of the 'Test set' to predict: {len(test_set):,} rows")
# ## result:
Size of the 'Test set' to predict: 4,833,292 rows



# --- 🏷️ Merge 3 features into a 'Test set' ---

## Merge user features (customer level).
test_set = test_set.merge(
    cust_features,
    on = 'user_id',
    how = 'left'
)


## Merge product features.
test_set = test_set.merge(
    prod_features,
    on = 'product_id',
    how = 'left'
)


## Merge user-product features.
test_set = test_set.merge(
    up_features,
    on = ['user_id', 'product_id'],
    how = 'left'
)



# --- 🏷️ Manage NaN value and select 4 main features ---

## check NaN value.
test_set.isna().sum()


## Select 4 core features to 'test set'.
core_features = [
    'count_orders',
    'avg_days_between_reorder',
    'prod_reorder_rate',
    'user_avg_days_between_orders'
]

x_test = test_set[core_features]

print(x_test.head())
# ## result:
#    count_orders  avg_days_between_reorder  prod_reorder_rate  user_avg_days_between_orders
# 0             1                      30.0           0.400251                     12.090909
# 1             1                      30.0           0.440605                     12.090909
# 2             3                       7.0           0.492162                     12.090909
# 3             1                      30.0           0.553551                     12.090909 
# 4             1                      30.0           0.591157                     12.090909



# --- 🏷️ Predicting outcomes and formatting ---

## Use the model trained with X_train to predict the probability in the test set.

## Predict the probability of repeat purchases (Y=1).
## LogisticRegression model

test_set['reordered_proba'] = model.predict_proba(x_test)[:, 1]


## Threshold
threshold = 0.4

test_set['reordered'] = (test_set['reordered_proba'] > threshold).astype(int)


## To see user_id, product_id, reordered_proba = probability, reordered = the last prediction.
print(test_set[['user_id', 'product_id', 'reordered_proba', 'reordered']].head())
# ## result:
#    user_id  product_id  reordered_proba  reordered
# 0        3         248         0.138504          0
# 1        3        1005         0.149115          0
# 2        3        1819         0.664711          1
# 3        3        7503         0.182388          0
# 4        3        8021         0.194676          0


## To see the distribution of predictions.
print(test_set['reordered'].value_counts())
# ## result:
# reordered
# 0    2844299
# 1    1988993
# Name: count, dtype: int64


## Descriptive Statistics of Predicted Probabilities [.describe()].
proba_stats = test_set['reordered_proba'].describe()
select_stats = proba_stats.loc[['count', 'mean', '50%', 'std']]

## Rename 50% to median.
select_stats = select_stats.rename({'50%': 'median'})

## Change the display format by def (def is function) use with mean, median and std.
def format_stats_series(series):
  format = []
  for index, value in series.items():
      if index == 'count':
          format.append(f"{int(value):,}")
      else:
          format.append(f"{value * 100:.2f}%")
  return pd.Series(format, index=series.index)

format_stats = format_stats_series(select_stats)

print(format_stats)
# ## result:
# count     4,833,292
# mean         35.11%
# median       31.35%
# std          21.92%
# dtype: object


## Filter data reordered = 1 only.
test_predictions = test_set[test_set['reordered'] == 1]


## Combine product_id into a single string for each order_id.
test_pred_agg = test_predictions.groupby('order_id').aggregate(
    products = ('product_id', lambda x: ' '.join(x.astype(str)))
).reset_index()


## Pull all order_id in the test set and join them to find the unpredicted orders.
all_test_orders = orders_test[['order_id']].drop_duplicates()

final_test_pred = all_test_orders.merge(
    test_pred_agg,
    on = 'order_id',
    how = 'left'
)


## Check NaN value.
final_test_pred.isna().sum()
# ## result:
#             0
# order_id	  0
# products	683

# dtype: int64


## Replace NaN value with 'None'.
final_test_pred['products'] = final_test_pred['products'].fillna('None')


## Check NaN value.
final_test_pred.isna().sum()



# --- 🏷️ Evaluate the model performance using the test_set table ---

## Use the best threshold (0.4) from y_val.
best_threshold = 0.4

## Predict the probability from feature (x_test).
y_pred_proba_test = model.predict_proba(x_test)[:, 1]

## Convert to a prediction of 0 or 1.
y_pred_test = (y_pred_proba_test >= best_threshold).astype(int)

print(y_pred_proba_test)
print(y_pred_test)
# ## result:
# [0.13850429 0.14911547 0.66471129 ... 0.14255925 0.05679411 0.13967566]
# [0 0 1 ... 0 0 0]


## Merge and filer process.

# Merge table.
test_set['y_pred'] = y_pred_test

# Filter process.
targeting_df = test_set[['user_id', 'product_id', 'y_pred']].copy()

print(targeting_df.head())
# ## result:
#    user_id  product_id  y_pred
# 0        3         248       0
# 1        3        1005       0
# 2        3        1819       1
# 3        3        7503       0
# 4        3        8021       0


## Filter y_pred == 1 only.
final_targeting_list = targeting_df[targeting_df['y_pred'] == 1].copy()


# Merge table with products to retrieve the product_id and product_name columns.
final_targeting_list = final_targeting_list.merge(
    products[['product_id', 'product_name']],
    on = 'product_id',
    how = 'left'
)

print("\n--- Final Targeting List ---")
print(final_targeting_list)
# ## result:
# --- Final Targeting List ---
#          user_id  product_id  y_pred                              product_name
# 0              3        1819       1  All Natural No Stir Creamy Almond Butter
# 1              3        9387       1                       Granny Smith Apples
# 2              3       14992       1                               Green Beans
# 3              3       16797       1                              Strawberries
# 4              3       16965       1                       Chocolate Ice Cream
# ...          ...         ...     ...                                       ...
# 1988988   206208       45007       1                          Organic Zucchini
# 1988989   206208       46069       1                              Supergreens!
# 1988990   206208       46667       1                       Organic Ginger Root
# 1988991   206208       46847       1   Quick Cooking Rolled Oats Irish Oatmeal
# 1988992   206208       47626       1                               Large Lemon

# [1988993 rows x 4 columns]



# --- 📌 Marketing Targeting List ---
# After verifying the model on the Test Set, we extract the list of customers
# predicted to reorder (Y=1) to be used for marketing campaigns.


## Filter only items where the model predicts a reorder (reordered == 1).
final_marketing_list = test_set[test_set['reordered'] == 1].copy()


## Merge table with 'products' to get 'product_name'.

final_marketing_list = final_marketing_list.merge(
    products[['product_id', 'product_name']],
    on = 'product_id',
    how = 'left'
)


## Select relevant columns to provide to the Marketing team

marketing_output = final_marketing_list[[
    'user_id',
    'product_id',
    'product_name',
    'reordered_proba'
]].sort_values(by=['user_id', 'reordered_proba'], ascending = [True, False])

print("--- Final List for Marketing team ---")
print(marketing_output.head())
# ## result:
# --- Final List for Marketing team ---
#     user_id  product_id                 product_name  reordered_proba
# 8         3       22035  Organic Whole String Cheese         0.780194
# 3         3       16797                 Strawberries         0.754814
# 10        3       24010    Wheat Gluten Free Waffles         0.736602
# 2         3       14992                  Green Beans         0.717975
# 16        3       44683             Brussels Sprouts         0.698129


## Export CSV file to send to Marketing team.
# marketing_output.to_csv('instacart_marketing_targets.csv', index=False)




# --- 📊 Create charts to show the 'Test_set' ---


# --- 🏷️ Bar Chart ---
## Count values (reordered_next) ​​to create a graph.
data_to_plot_pred = test_set['reordered'].value_counts().reset_index()

## Edit column name.
data_to_plot_pred.columns = ['Reordered', 'Count']

## Convert number to text.
data_to_plot_pred['Reordered'] = data_to_plot_pred['Reordered'].astype(str).replace(
    {'0': 'Not Reordered',
     '1': 'Reordered'}
)

print(data_to_plot_pred)
# ## result:
#        Reordered    Count
# 0  Not Reordered  2844299
# 1      Reordered  1988993


## Create a Bar Chart

## Set Figure Size (Canvas Size).
plt.figure(figsize = (6, 4))
sns.barplot(x = 'Reordered',
            y = 'Count',
            data = data_to_plot_pred)

## Customize the graph.
plt.ticklabel_format(style = 'plain',  # to close the Scientific Notation (such as 1e + 06).
                     axis = 'y')  # set up axis = y only.
plt.title('Distribution of Predicted Reordered Labels (Test Set)')
plt.xlabel('Predicted Reordered Status')  # Chart show 'the prediction' of model from Test_set.
plt.ylabel('Count of User-Product Pairs') # use data from User and Product together.
plt.show()



# --- 🏷️ Histogram Chart ---
## Analyze Predicted Probability Distribution on Test Set

## 1. Set Figure Size (Canvas Size).
plt.figure(figsize = (10, 6))

## 2. Create a Histogram chart and KDE plot.
sns.histplot(
    data = test_set,
    x = 'reordered_proba',
    bins = 50,
    kde = True,  # Show the kde (Kernel Density Estimate) is a curved line runs across the histogram.
    color = '#2ca02c'
)

## 3. Add line of Threshold 0.4.
threshold = 0.4
plt.axvline(threshold,
            color = 'red',
            linestyle = '--',
            label = f"Decision Threshold ({threshold})")
plt.legend()

## 4. Customize the graph.
plt.title('Distribution of Predicted Reorder Probability on Test Set', fontsize = 14)
plt.xlabel('Predicted Probability (P(Reorder) | X)', fontsize = 12)
plt.ylabel('Count of User-Product Pairs', fontsize = 12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()

