# 🛒 Retail Sales & Consumer Behavior Analysis (Instacart Dataset)
Customer behavior analysis and reorder prediction using SQL, R, Python and Tableau.

<br>

## Table of Contents

1. [Business Problem](#business-problem)

2. [Project Roadmap](#project-roadmap)

3. [Key Business Findings & Recommendation](#key-business-findings-&-recommendation)

4. [Tech Stack](#tech-stack)

5. [Navigate](#navigate)

6. [Data Source](#data-source)

<br>

## <h2 id="business-problem">⚠️ 1. Business Problem</h2>
"How can we increase sales while reducing marketing costs?"

Therefore, this project was created to respond the following:
- **Strategic Insights:** What types of customer purchasing behavior are likely to lead to service cancellation?
- **Retention:** How can we encourage customers to 'reorder' items they've already made?
- **"Cross-Selling Strategy:** Which product combinations frequently appear together to optimize promotional bundling and layout?


<br>

## <h2 id="project-roadmap">🗺️ 2. Project Roadmap</h2>

**1. Data Sourcing:** Select this dataset from the "Instacart Online Grocery Basket Analysis" on Kaggle.

**2. Data Modeling & Schema Design (dbdiagram.io):** Designed an ER Diagram to establish a clear architectural overview of the relational database.

**3. Strategic Business Insights (SQL):** Performed exploratory data analysis (EDA) to identify core purchasing patterns and trends within the large-scale dataset.

**4. Customer Segmentation (R):** Segmented customers based on purchasing behavior using the K-means clustering algorithm.

**5. Market Basket Analysis (R):** Identified product associations and frequent itemsets using the Apriori Algorithm to incress the cross-selling opportunities.

**6. Predictive Modeling (Python):** ฺBuilt a Logistic Regression model to predict the probability that customers will reorder products.

**7. Strategy Recommendation:** Summarise the analysis results into actionable 'Target Lists' to support the Marketing team’s precision targeting.

**8. Interactive Dashboard & Storytelling (Tableau):** Designed a comprehensive dashboard to visualize key performance indicators (KPIs), customer trends, and predictive insights, enabling data-driven business decisions.

<br>


## <h2 id="key-business-findings-&-recommendation">💡 3. Key Business Findings & Recommendation</h2>
Below are the strategic insights derived from our SQL and Machine Learning analysis:

### 1. High-Precision Targeting Opportunity
**Finding:** Our Predictive Model identified **1.99 million high-potential User-Product pairs** with a high probability of reordering.

**Recommendation:** Move away from "one-size-fits-all" marketing (e.g., stop sending random coupons to customers). By using this **Targeted Marketing List**, we can deliver **Personalized Coupons** and Minimize Marketing Spend.

<br>

### 2. Cross-Selling & UX Optimization (Basket Insights)
**Finding:** Market Basket Analysis reveals a strong preference for **One-Stop Shopping**. Customers tend to purchase multiple items within the same category or a variety of complementary products (e.g., Chicken, Avocado, and Bananas) in a single transaction. This behavior suggests that buyers prioritize **order consolidation** to reduce shipping costs and maximize time efficiency.

**Recommendation:** Implement **Digital Shelving Strategies** by intelligently grouping frequently co-purchased items within the app interface to reduce "search friction." Additionally, **Bundle Promotions** should be based on Association Rules to increase Average Order Value (AOV) by catering to the customer's desire for a seamless, all-in-one shopping experience.

<br>

### 3. Operational Load Balancing (Peak vs. Off-Peak Strategy)
**Finding:** Order volumes surge during **Sunday and Monday (9 AM – 5 PM)**, leading to potential delivery bottlenecks. In contrast, **Tuesday to Saturday**—specifically **late-night (11 PM – 12 AM) and early-morning (6 AM)**—show higher **available delivery slots**.

**Recommendation:**

  - **Peak:** Prioritize **Logistics & Staffing Optimization** and **Stock Management** to ensure timely, accurate fulfillment and minimize stock shortages.
                
  - **Off-Peak:** Launch **Flash Sales Promotion** to incentivize customers to **pre-book** during low-traffic windows. This effectively "shapes" demand to fill available capacity and reduces operational strain during major peaks.

<br>

### 4. Lifecycle-Aware Retention Strategy
**Finding:** Many "At-Risk" or "Lost" customers may simply follow a **Monthly Bulk Purchase Cycle** (aligning with payday or product life cycles). Their high Recency (30+ days) does not always indicate churn but rather a predictable shopping pattern.

**Recommendation:** Align re-engagement campaigns with the customer's **Individual Purchase Cycle**. For bulk buyers, trigger **"Cycle-Based Promotions"** during the month-end period to capture their next major restock order.

<br>

## <h2 id="tech-stack">⚙️ 4. Tech Stack</h2>

<br>

| **Category** | **Tools & Techniques** |
| :--- | :--- |
| **Data Processing** | ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Statistical Modeling (Descriptive/Diagnostic)** | ![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white) |
| **Machine Learning (Predictive)** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Visualization** | ![R](https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white) ![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white) |


<br>

## <h2 id="navigate">🔗 5. Navigate</h2>

<br>

[00-er-diagram](00-er-diagram) - Simulating associations between folders to make it easy to see the overiew.

[01-sql-database-simulation](01-sql-database-simulation) - Schema and data simulation.

[02-sql-business-queries](02-sql-business-queries) - Business Insights with SQL

[03-machine-learning](03-machine-learning) - Advanced Analytics & Model (R & Python)

04-data-visualization() - สรุปผลด้วย Dashboards และสถิติเชิงลึก

Key Insights (TL;DR): สรุปสิ่งที่น่าตื่นเต้นที่สุด 3 ข้อ (เช่น ช่วงเวลาทองคือ 9 am - 4 pm, อัตราการซื้อซ้ำของสินค้าเป็นปัจจัยหลักใน ML)

Tech Stack: โลโก้หรือชื่อเครื่องมือที่ใช้ (SQL, R, Python, Google Sheets)

<br>

## <h2 id="data-source">ℹ️ 6. Data Source</h2>
The dataset used in this project is from the Instacart Online Grocery Basket Analysis Dataset on Kaggle.

For more information, please visit [InstaCart Dataset](https://www.kaggle.com/datasets/yasserh/instacart-online-grocery-basket-analysis-dataset/data)
