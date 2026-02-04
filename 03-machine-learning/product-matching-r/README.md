# 📢 Machine Learning: Market Basket Analysis (MBA)
- Market Basket Analysis (MBA) is model for matching product.
- This section explores product associations to understand customer purchasing behavior and cross-selling opportunities.

<br>


## 📜 Overview & Methodology
<br>

- **Algorithm:** Apriori (Association Rule)
- **Parameters:** Support = 0.001, Confidence = 0.6, Max Length = 3 ❗
- **Metric of Focus:** **Lift** (to identify the strongest and most meaningful associations)

- 🖥️ You can find the full script in [market-basket-analysis.r](market-basket-analysis.r).

<br>

❗ *Note:* See here for more details about the **Parameters**.
- *Support = 0.001:* 10000*0.001 = 10 (product matching behavior at least 10 times)
- *Confidence = 0.6:* Probability of the RHS item (threshold 60%) being purchased given the LHS item
- *Max Length = 3:* Maximum items per association rule (LHS + RHS)

<br>
<br>

## ⌨️ Code for the Apriori Process

The code below is the Apriori process only.

<br>

```r
apriori_rules <- apriori(transactions, parameter = list(
  support = 0.001,  
  # 10000*0.001 = 10 (product matching behavior at least 10 times)
  
  confidence = 0.6,
  # Probability of the RHS item (threshold 60%) being purchased given the LHS item
  
  maxlen = 3
  # Maximum items per association rule (LHS + RHS)
))
```

<br>
<br>











