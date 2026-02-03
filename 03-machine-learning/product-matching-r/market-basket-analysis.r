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


length(unique(df_sample$order_id))
# ## result:
[1] 10000


## Convert data frame to transaction format
transaction_list <- split(df_sample$product_name, df_sample$order_id)

## Convert "list" to object of transaction
transactions <- as(transaction_list, "transactions")

## View the first 5 transactions
inspect(transactions[1:5])
# ## result:
items                                                    transactionID
[1] {Cola,                                                                
     Lifesavors Mints Wint O Green}                                   907 
[2] {Bag of Organic Bananas,                                              
     California Extra Virgin Olive Oil,                                   
     Carrots,                                                             
     Fresh Cauliflower,                                                   
     Meatles  Soy Gluten-Free Grounds,                                    
     Meatless & Soy Free Frozen Chik'n Tenders,                           
     Organic 1% Low Fat Milk,                                             
     Organic Blackberries,                                                
     Organic Brown Rice,                                                  
     Organic Extra Large Grade AA Brown Eggs,                             
     Organic Gala Apples,                                                 
     Organic Good Seed Bread,                                             
     Organic Grape Tomatoes,                                              
     Organic Hass Avocado,                                                
     Organic Raspberries,                                                 
     Organic Red On the Vine Tomato,                                      
     Organic Strawberries,                                                
     Probiotic Dairy Culture Strawberry,                                  
     Raspberry Essence Water,                                             
     Sparkling Mineral Water, Natural Lemon Flavor,                       
     Total 2% with Strawberry Lowfat Greek Strained Yogurt,               
     Unsweet Peach Water}                                             1662
[3] {Avocado,                                                             
     Cherubs Heavenly Salad Tomatoes,                                     
     Chicken Tortilla Soup,                                               
     Fresh Whole Garlic,                                                  
     Grated Parmesan Cheese,                                              
     Kickstart Pineapple Orange Mango,                                    
     Light Chicken & Dumpling Soup,                                       
     Light Chicken Corn Chowder,                                          
     Medium Scarlet Raspberries,                                          
     Organic Blackberries,                                                
     Plain Greek Yogurt,                                                  
     Ready to Serve Long Grain White Rice,                                
     Reduced Fat Shredded Mozzarella Cheese,                              
     Rich & Hearty Chicken & Homestyle Noodles Soup,                      
     Rich & Hearty Creamy Roasted Chicken Wild Rice Soup,                 
     Strawberries,                                                        
     Sweet Potatoes,                                                      
     Tortillas, Flour,                                                    
     Traditional Chickarina Chicken Soup with Meatballs,                  
     Traditional Chicken & Herb Dumplings Soup,                           
     Traditional Chicken & Orzo with Lemon Soup,                          
     Traditional Chicken & Wild Rice Soup,                                
     Traditional Italian-Style Wedding Soup,                              
     Unsweetened Vanilla Almond Milk,                                     
     Zero Ultra Energy Drink}                                         1979
[4] {Natural Alpine Spring Water,                                         
     Peach Pear Flavored Sparkling Water,                                 
     Sparkling Water Grapefruit}                                      2327
[5] {Fancy Bamboo Shoots,                                                 
     Less Salt Soy Sauce,                                                 
     Organic Ginger Root}                                             2673






