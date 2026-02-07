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
#    order_id product_id          product_name
#       <int>      <int>                <char>
# 1:        2      33120    Organic Egg Whites
# 2:        2      28985 Michigan Organic Kale
# 3:        2       9327         Garlic Powder
# 4:        2      45918        Coconut Butter
# 5:        2      30035     Natural Sweetener
# 6:        2      17794               Carrots

length(unique(df_merged$order_id))
# ## result:
# [1] 3214874



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
#    order_id                              product_name
#       <int>                                    <char>
# 1:      907             Lifesavors Mints Wint O Green
# 2:      907                                      Cola
# 3:     1662                      Organic Blackberries
# 4:     1662          Meatles  Soy Gluten-Free Grounds
# 5:     1662 Meatless & Soy Free Frozen Chik'n Tenders
# 6:     1662                                   Carrots

length(unique(df_sample$order_id))
# ## result:
# [1] 10000

## Convert data frame to transaction format
transaction_list <- split(df_sample$product_name, df_sample$order_id)

## Convert "list" to object of transaction
transactions <- as(transaction_list, "transactions")

## View the first 3 transactions
inspect(transactions[1:3])
# ## result:
#     items                                                    transactionID
# [1] {Cola,                                                                
#      Lifesavors Mints Wint O Green}                                   907 
# [2] {Bag of Organic Bananas,                                              
#      California Extra Virgin Olive Oil,                                   
#      Carrots,                                                             
#      Fresh Cauliflower,                                                   
#      Meatles  Soy Gluten-Free Grounds,                                    
#      Meatless & Soy Free Frozen Chik'n Tenders,                           
#      Organic 1% Low Fat Milk,                                             
#      Organic Blackberries,                                                
#      Organic Brown Rice,                                                  
#      Organic Extra Large Grade AA Brown Eggs,                             
#      Organic Gala Apples,                                                 
#      Organic Good Seed Bread,                                             
#      Organic Grape Tomatoes,                                              
#      Organic Hass Avocado,                                                
#      Organic Raspberries,                                                 
#      Organic Red On the Vine Tomato,                                      
#      Organic Strawberries,                                                
#      Probiotic Dairy Culture Strawberry,                                  
#      Raspberry Essence Water,                                             
#      Sparkling Mineral Water, Natural Lemon Flavor,                       
#      Total 2% with Strawberry Lowfat Greek Strained Yogurt,               
#      Unsweet Peach Water}                                             1662
# [3] {Avocado,                                                             
#      Cherubs Heavenly Salad Tomatoes,                                     
#      Chicken Tortilla Soup,                                               
#      Fresh Whole Garlic,                                                  
#      Grated Parmesan Cheese,                                              
#      Kickstart Pineapple Orange Mango,                                    
#      Light Chicken & Dumpling Soup,                                       
#      Light Chicken Corn Chowder,                                          
#      Medium Scarlet Raspberries,                                          
#      Organic Blackberries,                                                
#      Plain Greek Yogurt,                                                  
#      Ready to Serve Long Grain White Rice,                                
#      Reduced Fat Shredded Mozzarella Cheese,                              
#      Rich & Hearty Chicken & Homestyle Noodles Soup,                      
#      Rich & Hearty Creamy Roasted Chicken Wild Rice Soup,                 
#      Strawberries,                                                        
#      Sweet Potatoes,                                                      
#      Tortillas, Flour,                                                    
#      Traditional Chickarina Chicken Soup with Meatballs,                  
#      Traditional Chicken & Herb Dumplings Soup,                           
#      Traditional Chicken & Orzo with Lemon Soup,                          
#      Traditional Chicken & Wild Rice Soup,                                
#      Traditional Italian-Style Wedding Soup,                              
#      Unsweetened Vanilla Almond Milk,                                     
#      Zero Ultra Energy Drink}                                         1979


## ML: apriori process
apriori_rules <- apriori(transactions, parameter = list(
  support = 0.001,  
  # 10000*0.001 = 10 (product matching behavior at least 10 times)
  
  confidence = 0.6,
  # Probability of the RHS item (threshold 60%) being purchased given the LHS item
  
  maxlen = 3
  # Maximum items per association rule (LHS + RHS)
))


summary(apriori_rules)
# ## result:
# set of 14 rules

# rule length distribution (lhs + rhs):sizes
#  2  3 
#  1 13 

#    Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
#   2.000   3.000   3.000   2.929   3.000   3.000 

# summary of quality measures:
#     support           confidence        coverage             lift        
#  Min.   :0.001000   Min.   :0.6000   Min.   :0.001500   Min.   :  4.208  
#  1st Qu.:0.001025   1st Qu.:0.6250   1st Qu.:0.001600   1st Qu.:  4.394  
#  Median :0.001200   Median :0.6364   Median :0.001900   Median :  4.548  
#  Mean   :0.001179   Mean   :0.6411   Mean   :0.001843   Mean   : 21.419  
#  3rd Qu.:0.001300   3rd Qu.:0.6625   3rd Qu.:0.002000   3rd Qu.:  4.960  
#  Max.   :0.001400   Max.   :0.6875   Max.   :0.002200   Max.   :112.166  
#      count      
#  Min.   :10.00  
#  1st Qu.:10.25  
#  Median :12.00  
#  Mean   :11.79  
#  3rd Qu.:13.00  
#  Max.   :14.00  

# mining info:
#          data ntransactions support confidence
#  transactions         10000   0.001        0.6
# call
#  apriori(data = transactions, parameter = list(support = 0.001, confidence = 0.6, maxlen = 3))



# Sort rules by Lift
rules_sort <- sort(apriori_rules, 
                   by = "lift", 
                   decreasing = TRUE)

## Display all rules
inspect(rules_sort)
# ## result:
#      lhs                                     rhs                                             support confidence coverage       lift count
# [1]  {Coconut Sparkling Water}            => {Grapefruit Sparkling Water}                     0.0013  0.6842105   0.0019 112.165660    13
# [2]  {Non Fat Raspberry Yogurt,                                                                                                          
#       Vanilla Skyr Nonfat Yogurt}         => {Icelandic Style Skyr Blueberry Non-fat Yogurt}  0.0011  0.6875000   0.0016  98.214286    11
# [3]  {Sparkling Lemon Water,                                                                                                             
#       Sparkling Water Grapefruit}         => {Lime Sparkling Water}                           0.0014  0.6363636   0.0022  39.772727    14
# [4]  {Organic Cucumber,                                                                                                                  
#       Organic Granny Smith Apple}         => {Bag of Organic Bananas}                         0.0012  0.6000000   0.0020   5.054760    12
# [5]  {Boneless Skinless Chicken Breasts,                                                                                                 
#       Organic Hass Avocado}               => {Banana}                                         0.0010  0.6666667   0.0015   4.675082    10
# [6]  {Organic Garlic,                                                                                                                    
#       Strawberries}                       => {Banana}                                         0.0010  0.6666667   0.0015   4.675082    10
# [7]  {Honeycrisp Apple,                                                                                                                  
#       Strawberries}                       => {Banana}                                         0.0013  0.6500000   0.0020   4.558205    13
# [8]  {Green Beans,                                                                                                                       
#       Organic Avocado}                    => {Banana}                                         0.0011  0.6470588   0.0017   4.537579    11
# [9]  {Organic Avocado,                                                                                                                   
#       Seedless Red Grapes}                => {Banana}                                         0.0014  0.6363636   0.0022   4.462578    14
# [10] {Original Hummus,                                                                                                                   
#       Strawberries}                       => {Banana}                                         0.0012  0.6315789   0.0019   4.429025    12
# [11] {Boneless Skinless Chicken Breasts,                                                                                                 
#       Cucumber Kirby}                     => {Banana}                                         0.0010  0.6250000   0.0016   4.382889    10
# [12] {Honeycrisp Apple,                                                                                                                  
#       Seedless Red Grapes}                => {Banana}                                         0.0010  0.6250000   0.0016   4.382889    10
# [13] {Organic Avocado,                                                                                                                   
#       Organic Peeled Whole Baby Carrots}  => {Banana}                                         0.0013  0.6190476   0.0021   4.341147    13
# [14] {100% Whole Wheat Bread,                                                                                                            
#       Strawberries}                       => {Banana}                                         0.0012  0.6000000   0.0020   4.207574    12


# ------------------------------------------------------- #
# ## Actionable Insights: Top 5 High-Potential Rules
# ## 🔑 Focus on the highest "Lift" to identify strong product associations.
# ## Note: Extremely high lift can sometimes indicate niche items (e.g., flavored yogurts).
# ------------------------------------------------------- #


# Select only Top 5 rules to ensure clear visualization
top_5_rules <- head(rules_sort, n = 5)

## Display rules for analysis
inspect(top_5_rules)
# ## result:
#     lhs                                     rhs                                             support confidence coverage       lift count
# [1] {Coconut Sparkling Water}            => {Grapefruit Sparkling Water}                     0.0013  0.6842105   0.0019 112.165660    13
# [2] {Non Fat Raspberry Yogurt,                                                                                                          
#      Vanilla Skyr Nonfat Yogurt}         => {Icelandic Style Skyr Blueberry Non-fat Yogurt}  0.0011  0.6875000   0.0016  98.214286    11
# [3] {Sparkling Lemon Water,                                                                                                             
#      Sparkling Water Grapefruit}         => {Lime Sparkling Water}                           0.0014  0.6363636   0.0022  39.772727    14
# [4] {Organic Cucumber,                                                                                                                  
#      Organic Granny Smith Apple}         => {Bag of Organic Bananas}                         0.0012  0.6000000   0.0020   5.054760    12
# [5] {Boneless Skinless Chicken Breasts,                                                                                                 
#      Organic Hass Avocado}               => {Banana}                                         0.0010  0.6666667   0.0015   4.675082    10



# Visualization (Network Graph)
plot(top_5_rules, 
     method = "graph",
     engine = "htmlwidget")


# Convert HTML to picture
# install.packages(c("htmlwidgets", "webshot")) 
# webshot::install_phantomjs()


## Download Library
library(htmlwidgets)
library(webshot)


## Create a Interactive chart
p <- plot(top_5_rules, method = "graph", engine = "htmlwidget")


## Save chart by temporary HTML file
saveWidget(p, "rules_plot.html", selfcontained = TRUE)


## Use webshot to change from HTML file to the picture (.png or .jpg)
webshot("rules_plot.html", file = "association_rules.png", delay = 2)



# Visualization (Bar Chart)

## Create a data frame
rules_df <- as(top_5_rules, "data.frame") %>%
  select(rules, support, confidence, lift)

print(rules_df)
# ## result:
#                                                                                                      rules
# 1                                                {Coconut Sparkling Water} => {Grapefruit Sparkling Water}
# 2 {Non Fat Raspberry Yogurt,Vanilla Skyr Nonfat Yogurt} => {Icelandic Style Skyr Blueberry Non-fat Yogurt}
# 3                             {Sparkling Lemon Water,Sparkling Water Grapefruit} => {Lime Sparkling Water}
# 9                                {Organic Cucumber,Organic Granny Smith Apple} => {Bag of Organic Bananas}
# 6                                     {Boneless Skinless Chicken Breasts,Organic Hass Avocado} => {Banana}
#   support confidence       lift
# 1  0.0013  0.6842105 112.165660
# 2  0.0011  0.6875000  98.214286
# 3  0.0014  0.6363636  39.772727
# 9  0.0012  0.6000000   5.054760
# 6  0.0010  0.6666667   4.675082


## Bar Chart: Top 5 Product Rules
ggplot(rules_df, mapping = aes(x = reorder(rules, lift), 
                               y = lift,
                               fill = lift)) +
  geom_col() +
  coord_flip() +
  scale_fill_gradient(low = "#A9B5DF", high = "#2D336B") +
  labs(title = "Top 5 Strongest Product Associations",
       subtitle = "Ranked by Lift (Strength of Correlation)",
       x = "Association Rules",
       y = "Lift Value",
       caption = "Data source: InstaCart Online Grocery Basket Analysis Dataset on Kaggle") +
  theme(legend.position = "none")
  

# ------------------------------------------------------- #
# ## 💡 Business Value & Actionable Insights
# ------------------------------------------------------- #
# ## The bar chart visualizes "Lift," which measures the strength of association.
# ## - A high Lift (e.g., > 90) indicates a strong correlation between items.
# ## - For same-category items (e.g., Sparkling Water flavors), this suggests 
# ##  opportunities for 'Flavor Bundling' or 'Variety Packs'.
# ## - For different-category items (e.g., Chicken Breasts, Avocado and Banana), this shows a cross-category link between meat, vegetables, and fruit.
# ## Proposed Marketing Actions:
# ## 1. Product Bundling: Create "Healthy Meal Kits" combining meat and produce.
# ## 2. Shelf Placement: Locate high-association items near each other to 
# ##    shorten the customer journey and encourage unplanned purchases.
# ## 3. Personalized Promotion: Implement "Frequently Bought Together" 
# ##    recommendations on the mobile app or website during checkout.
# ------------------------------------------------------- #



## Export CSV for Tableau
write.csv(rules_df, "product_matching.csv", row.names = F)


