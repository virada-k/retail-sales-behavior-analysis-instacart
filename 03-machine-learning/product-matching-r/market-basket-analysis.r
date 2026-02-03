# Download package
library(data.table)
library(dplyr)
library(arules)
library(arulesViz)
library(ggplot2)


# Download data
op_prior <- fread("order_products__prior.csv",
                  select = c("order_id", "product_id"))

products <- fread("products.csv",
                  select = c("product_id", "product_name"))


# Merge data
df_merged <- op_prior %>%
  left_join(products, by = "product_id")


## Check overall data
head(df_merged)
# ## result:
   order_id product_id          product_name
      <int>      <int>                <char>
1:        2      33120    Organic Egg Whites
2:        2      28985 Michigan Organic Kale
3:        2       9327         Garlic Powder
4:        2      45918        Coconut Butter
5:        2      30035     Natural Sweetener
6:        2      17794               Carrots

length(unique(df_merged$order_id))
# ## result:
[1] 3214874



# Convert the data to "sampling"

all_order_id <- unique(df_merged$order_id)

set.seed(93)
n <- 10000
sample_order_id <- sample(all_order_id, size = n, replace = FALSE)

df_sample <- df_merged %>%
  filter(order_id %in% sample_order_id) %>%
  select(order_id, product_name)


head(df_sample)
# ## result:
   order_id                              product_name
      <int>                                    <char>
1:      907             Lifesavors Mints Wint O Green
2:      907                                      Cola
3:     1662                      Organic Blackberries
4:     1662          Meatles  Soy Gluten-Free Grounds
5:     1662 Meatless & Soy Free Frozen Chik'n Tenders
6:     1662                                   Carrots

