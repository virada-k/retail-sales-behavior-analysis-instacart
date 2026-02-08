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
# Since the dataset is large, it is hosted on Google Drive.
# You can replace the path below with your local file path.
# df = pd.read_csv('instacart_data.csv')

## Store 'orders' in a Dataframe.
orders = pd.read_csv('orders.csv',
                     usecols=['order_id', 'user_id', 'eval_set', 'order_number', 'days_since_prior_order'])

print(orders.head())
