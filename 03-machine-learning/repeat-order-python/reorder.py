# 📢 Data Preparation & Machine Learning
# Project: Instacart Repeat Order Prediction


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















