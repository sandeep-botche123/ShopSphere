import pandas as pd
import streamlit as st
import sys
from pathlib import Path
from sqlalchemy import text
from datetime import date

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.Database import create_engine_connection
try:
    engine = create_engine_connection()

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    st.success("Successfully connected to ShopSphere MySQL database!")

except Exception as e:
    st.error(f"Database connection failed: {e}")

st.set_page_config(
    page_title="ShopSphere Analytics",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 ShopSphere Analytics")
st.subheader("E-commerce Sales Analytics Dashboard")

st.success("Welcome to ShopSphere!")


# ==============================
# KPI CALCULATIONS
# ==============================

# 1. Net Revenue
query = """
SELECT
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS net_revenue
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered';
"""

revenue_df = pd.read_sql(query, engine)
net_revenue = revenue_df["net_revenue"].iloc[0]


# 2. Delivered Orders
query = """
SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE order_status = 'Delivered';
"""

orders_df = pd.read_sql(query, engine)
delivered_orders = orders_df["delivered_orders"].iloc[0]


# 3. Average Order Value
aov = net_revenue / delivered_orders


# 4. Delivered Customers
customer_query = """
SELECT COUNT(DISTINCT customer_id) AS delivered_customers
FROM orders
WHERE order_status = 'Delivered';
"""

customer_df = pd.read_sql(customer_query, engine)
delivered_customers = customer_df["delivered_customers"].iloc[0]


# 5. Cancellation Rate
cancellation_query = """
SELECT
    COUNT(CASE WHEN order_status = 'Cancelled' THEN 1 END) * 100.0
    / COUNT(*) AS cancellation_rate
FROM orders;
"""

cancellation_df = pd.read_sql(cancellation_query, engine)
cancellation_rate = cancellation_df["cancellation_rate"].iloc[0]


# ==============================
# DISPLAY KPIs IN COLUMNS
# ==============================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Net Revenue", f"₹{net_revenue / 10000000:.2f} Cr")

with col2:
    st.metric("Delivered Orders", f"{delivered_orders:,}")

with col3:
    st.metric("Average Order Value", f"₹{aov:,.2f}")

with col4:
    st.metric("Delivered Customers", f"{delivered_customers:,}")

with col5:
    st.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")


# ==================================
# MONTHLY REVENUE TREND
# ==================================

st.subheader("Monthly Revenue Trend")

monthly_query = """
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS monthly_revenue
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;
"""

monthly_df = pd.read_sql(monthly_query, engine)

st.line_chart(
    monthly_df,
    x="month",
    y="monthly_revenue"
)


# ==================================
# TOP 10 PRODUCTS BY REVENUE
# ==================================

st.subheader("Top 10 Products by Revenue")

product_query = """
SELECT
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
INNER JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
ORDER BY net_revenue DESC
LIMIT 10;
"""

product_df = pd.read_sql(product_query, engine)

st.bar_chart(
    product_df,
    x="product_name",
    y="net_revenue",
    horizontal=True
)



# ==================================
# REVENUE BY CITY
# ==================================

st.subheader("Revenue by City")

city_query = """
SELECT
    c.city,
    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
INNER JOIN customers AS c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.city
ORDER BY net_revenue DESC;
"""

city_df = pd.read_sql(city_query, engine)

st.bar_chart(
    city_df,
    x="city",
    y="net_revenue"
)


# Delivery Status Distribution

status_query = """
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
"""

status_df = pd.read_sql(status_query, engine)

st.subheader("Order Status Distribution")

st.bar_chart(
    status_df.set_index("order_status")
)


# Top 10 Products by Profit

profit_query = """
SELECT
    p.product_name,
    SUM(
        oi.quantity * (
            oi.selling_price * (1 - oi.discount / 100)
            - p.cost_price
        )
    ) AS total_profit
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
INNER JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_name
ORDER BY total_profit DESC
LIMIT 10;
"""

profit_df = pd.read_sql(profit_query, engine)

st.subheader("Top 10 Products by Profit")

st.bar_chart(
    profit_df.set_index("product_name")
)
# Profit by Category

category_profit_query = """
SELECT
    c.category_name,
    SUM(
        oi.quantity * (
            oi.selling_price * (1 - oi.discount / 100)
            - p.cost_price
        )
    ) AS total_profit
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
INNER JOIN products AS p
    ON oi.product_id = p.product_id
INNER JOIN categories AS c
    ON p.category_id = c.category_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_name
ORDER BY total_profit DESC;
"""

category_profit_df = pd.read_sql(category_profit_query, engine)

st.subheader("Profit by Category")

st.bar_chart(
    category_profit_df.set_index("category_name")
)

# Monthly Revenue Trend with Date Filter

st.subheader("Interactive Monthly Revenue Trend")

date_range = st.date_input(
    "Select Date Range",
    value=(date(2025, 1, 1), date(2025, 12, 31))
)

if len(date_range) == 2:

    start_date, end_date = date_range

    monthly_revenue_query = """
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(
            oi.quantity * oi.selling_price *
            (1 - oi.discount / 100)
        ) AS monthly_revenue
    FROM order_items AS oi
    INNER JOIN orders AS o
        ON oi.order_id = o.order_id
    WHERE o.order_status = 'Delivered'
      AND o.order_date >= :start_date
      AND o.order_date < DATE_ADD(:end_date, INTERVAL 1 DAY)
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
    ORDER BY month;
    """

    monthly_df = pd.read_sql(
        text(monthly_revenue_query),
        engine,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )

    if not monthly_df.empty:
        monthly_df["month"] = pd.to_datetime(monthly_df["month"])

        st.line_chart(
            monthly_df.set_index("month")["monthly_revenue"]
        )
    else:
        st.warning("No revenue data available for this date range.")

# Interactive Category Filter

st.subheader("Explore Products by Category")

category_df = pd.read_sql(
    "SELECT category_name FROM categories ORDER BY category_name",
    engine
)
category_options = ["All Categories"] + category_df["category_name"].tolist()
selected_category = st.selectbox(
    "Select Product Category",
    category_options
)
category_product_query = """
SELECT
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
INNER JOIN products AS p
    ON oi.product_id = p.product_id
INNER JOIN categories AS c
    ON p.category_id = c.category_id
WHERE o.order_status = 'Delivered'
  AND (
      :category = 'All Categories'
      OR c.category_name = :category
  )
GROUP BY p.product_name
ORDER BY net_revenue DESC
LIMIT 10;
"""

category_product_df = pd.read_sql(
    text(category_product_query),
    engine,
    params={"category": selected_category}
)

st.bar_chart(
    category_product_df.set_index("product_name")
)


# ==================================
# COMBINED CITY + CATEGORY FILTER
# ==================================

st.subheader("Explore Products by City & Category")

# Fetch available cities
city_df = pd.read_sql(
    text("""
        SELECT DISTINCT city
        FROM customers
        WHERE city IS NOT NULL
        ORDER BY city
    """),
    engine
)

city_options = ["All Cities"] + city_df["city"].tolist()

# Fetch available categories
category_df = pd.read_sql(
    text("""
        SELECT category_name
        FROM categories
        ORDER BY category_name
    """),
    engine
)

category_options = ["All Categories"] + category_df["category_name"].tolist()

# Display filters side by side
col1, col2 = st.columns(2)

with col1:
    selected_city = st.selectbox(
        "Select City",
        city_options,
        key="combined_city"
    )

with col2:
    selected_category = st.selectbox(
        "Select Category",
        category_options,
        key="combined_category"
    )

# Fetch filtered product revenue
combined_query = """
SELECT
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue
FROM order_items AS oi
INNER JOIN orders AS o
    ON oi.order_id = o.order_id
INNER JOIN products AS p
    ON oi.product_id = p.product_id
INNER JOIN categories AS c
    ON p.category_id = c.category_id
INNER JOIN customers AS cu
    ON o.customer_id = cu.customer_id
WHERE o.order_status = 'Delivered'
    AND (
        :city = 'All Cities'
        OR cu.city = :city
    )
    AND (
        :category = 'All Categories'
        OR c.category_name = :category
    )
GROUP BY p.product_id, p.product_name
ORDER BY net_revenue DESC
LIMIT 10;
"""

combined_df = pd.read_sql(
    text(combined_query),
    engine,
    params={
        "city": selected_city,
        "category": selected_category
    }
)

if not combined_df.empty:
    st.bar_chart(
        combined_df.set_index("product_name")
    )
else:
    st.warning("No products found for the selected filters.")



# ==================================
# TOP 10 CUSTOMERS BY REVENUE
# ==================================

st.subheader("Top 10 Customers by Revenue")

# Fetch Top 10 Customers
customer_query = """
SELECT
    cu.customer_id,
    cu.customer_name,
    CONCAT(
        cu.customer_name,
        ' (',
        cu.customer_id,
        ')'
    ) AS customer_label,
    cu.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue

FROM customers AS cu

INNER JOIN orders AS o
    ON cu.customer_id = o.customer_id

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

WHERE o.order_status = 'Delivered'

GROUP BY
    cu.customer_id,
    cu.customer_name,
    cu.city

ORDER BY net_revenue DESC

LIMIT 10;
"""

# Execute SQL Query
customer_df = pd.read_sql(
    text(customer_query),
    engine
)

# Display Customer Revenue Chart
st.bar_chart(
    customer_df.set_index("customer_label")["net_revenue"],
    horizontal=True
)

# Display Customer Details
st.dataframe(
    customer_df[
        [
            "customer_id",
            "customer_name",
            "city",
            "total_orders",
            "net_revenue"
        ]
    ],
    hide_index=True
)


# ==================================
# CUSTOMER REVENUE CONTRIBUTION
# ==================================

st.subheader("Customer Revenue Contribution")

# Total revenue from all delivered orders
total_revenue_query = """
SELECT
    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS total_revenue
FROM orders AS o
INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered';
"""

total_revenue_df = pd.read_sql(
    text(total_revenue_query),
    engine
)

total_revenue = total_revenue_df["total_revenue"].iloc[0]

# Revenue generated by Top 10 customers
top10_revenue = customer_df["net_revenue"].sum()

# Revenue generated by remaining customers
remaining_revenue = total_revenue - top10_revenue

# Calculate contribution percentages
top10_percentage = (
    top10_revenue / total_revenue * 100
    if total_revenue else 0
)

remaining_percentage = (
    remaining_revenue / total_revenue * 100
    if total_revenue else 0
)

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Top 10 Customers Revenue",
        f"₹{top10_revenue / 10000000:.2f} Cr"
    )

with col2:
    st.metric(
        "Top 10 Revenue Contribution",
        f"{top10_percentage:.2f}%"
    )

with col3:
    st.metric(
        "Remaining Customers Contribution",
        f"{remaining_percentage:.2f}%"
    )

# Display revenue contribution chart
contribution_df = pd.DataFrame({
    "Customer Group": [
        "Top 10 Customers",
        "Remaining Customers"
    ],
    "Revenue": [
        top10_revenue,
        remaining_revenue
    ]
})

st.bar_chart(
    contribution_df.set_index("Customer Group")
)

# ==================================
# MONTHLY PROFIT TREND
# ==================================

st.subheader("Monthly Profit Trend")

monthly_profit_query = """
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(
        oi.quantity *
        (
            oi.selling_price * (1 - oi.discount / 100)
            - p.cost_price
        )
    ) AS total_profit

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN products AS p
    ON oi.product_id = p.product_id

WHERE o.order_status = 'Delivered'

GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')

ORDER BY month;
"""

monthly_profit_df = pd.read_sql(
    text(monthly_profit_query),
    engine
)

# Display Monthly Profit Chart
st.line_chart(
    monthly_profit_df.set_index("month")["total_profit"]
)

# Display Monthly Profit Details
st.dataframe(
    monthly_profit_df,
    hide_index=True
)


# ==================================
# REPEAT VS ONE-TIME CUSTOMERS
# ==================================

st.subheader("Repeat vs One-Time Customers")

customer_type_query = """
SELECT
    CASE
        WHEN order_count = 1 THEN 'One-Time Customers'
        ELSE 'Repeat Customers'
    END AS customer_type,
    COUNT(*) AS customer_count
FROM (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM orders AS o
    WHERE o.order_status = 'Delivered'
    GROUP BY o.customer_id
) AS customer_orders
GROUP BY customer_type;
"""

customer_type_df = pd.read_sql(
    text(customer_type_query),
    engine
)

# Calculate total customers
total_customers = customer_type_df["customer_count"].sum()

# Calculate percentages
customer_type_df["percentage"] = (
    customer_type_df["customer_count"] /
    total_customers * 100
)

# Display metrics
one_time = customer_type_df.loc[
    customer_type_df["customer_type"] == "One-Time Customers",
    "customer_count"
].sum()

repeat = customer_type_df.loc[
    customer_type_df["customer_type"] == "Repeat Customers",
    "customer_count"
].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Customers", f"{total_customers:,}")

with col2:
    st.metric("One-Time Customers", f"{one_time:,}")

with col3:
    st.metric("Repeat Customers", f"{repeat:,}")

# Display customer distribution chart
st.bar_chart(
    customer_type_df.set_index("customer_type")["customer_count"]
)

# Display detailed table
st.dataframe(
    customer_type_df,
    hide_index=True
)

# ==================================
# CUSTOMER RETENTION ANALYSIS
# ==================================

st.subheader("Customer Retention Analysis")

retention_query = """
WITH customer_activity AS (
    SELECT DISTINCT
        customer_id,
        DATE_FORMAT(order_date, '%Y-%m') AS purchase_month
    FROM orders
    WHERE order_status = 'Delivered'
),

first_purchase AS (
    SELECT
        customer_id,
        MIN(purchase_month) AS first_month
    FROM customer_activity
    GROUP BY customer_id
),

monthly_retention AS (
    SELECT
        fp.first_month,
        COUNT(DISTINCT fp.customer_id) AS total_customers,
        COUNT(DISTINCT CASE
            WHEN ca.purchase_month > fp.first_month
            THEN fp.customer_id
        END) AS retained_customers
    FROM first_purchase AS fp
    LEFT JOIN customer_activity AS ca
        ON fp.customer_id = ca.customer_id
    GROUP BY fp.first_month
)

SELECT
    first_month,
    total_customers,
    retained_customers,
    ROUND(
        retained_customers * 100.0 /
        NULLIF(total_customers, 0),
        2
    ) AS retention_rate
FROM monthly_retention
ORDER BY first_month;
"""

retention_df = pd.read_sql(
    text(retention_query),
    engine
)

# Display retention table
st.dataframe(
    retention_df,
    hide_index=True
)

# Display retention rate chart
st.line_chart(
    retention_df.set_index("first_month")["retention_rate"]
)


# ==================================
# DISCOUNT IMPACT ANALYSIS
# ==================================

st.subheader("Discount Impact Analysis")

discount_query = """
SELECT
    CASE
        WHEN oi.discount = 0 THEN 'No Discount'
        ELSE 'Discounted Orders'
    END AS discount_type,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(AVG(oi.discount), 2) AS average_discount,

    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue,

    SUM(
        oi.quantity *
        (
            oi.selling_price * (1 - oi.discount / 100)
            - p.cost_price
        )
    ) AS total_profit

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN products AS p
    ON oi.product_id = p.product_id

WHERE o.order_status = 'Delivered'

GROUP BY discount_type

ORDER BY discount_type;
"""

discount_df = pd.read_sql(
    text(discount_query),
    engine
)

# Display discount analysis table
st.dataframe(
    discount_df,
    hide_index=True
)

# Revenue comparison
st.subheader("Revenue by Discount Type")

st.bar_chart(
    discount_df.set_index("discount_type")["net_revenue"]
)

# Profit comparison
st.subheader("Profit by Discount Type")

st.bar_chart(
    discount_df.set_index("discount_type")["total_profit"]
)


# ==================================
# CITY PERFORMANCE ANALYSIS
# ==================================

st.subheader("Best & Worst Performing Cities")

city_performance_query = """
SELECT
    cu.city,
    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue,

    SUM(
        oi.quantity *
        (
            oi.selling_price * (1 - oi.discount / 100)
            - p.cost_price
        )
    ) AS total_profit

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN products AS p
    ON oi.product_id = p.product_id

INNER JOIN customers AS cu
    ON o.customer_id = cu.customer_id

WHERE o.order_status = 'Delivered'

GROUP BY cu.city
ORDER BY net_revenue DESC;
"""

city_performance_df = pd.read_sql(
    text(city_performance_query),
    engine
)

# Highest and lowest revenue cities
best_city = city_performance_df.iloc[0]
worst_city = city_performance_df.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Highest Revenue City",
        best_city["city"],
        f"₹{best_city['net_revenue'] / 10000000:.2f} Cr"
    )

with col2:
    st.metric(
        "Lowest Revenue City",
        worst_city["city"],
        f"₹{worst_city['net_revenue'] / 10000000:.2f} Cr"
    )

# Revenue chart
st.subheader("Revenue by City")

st.bar_chart(
    city_performance_df.set_index("city")["net_revenue"],
    horizontal=True
)

# Profit chart
st.subheader("Profit by City")

st.bar_chart(
    city_performance_df.set_index("city")["total_profit"],
    horizontal=True
)

# Detailed table
st.dataframe(
    city_performance_df,
    hide_index=True
)


# ==================================
# CITY-WISE PROFIT MARGIN ANALYSIS
# ==================================

st.subheader("City-wise Profit Margin Analysis")

# Calculate profit margin
city_performance_df["profit_margin"] = (
    city_performance_df["total_profit"]
    / city_performance_df["net_revenue"]
    * 100
)

# Sort cities by profit margin
margin_df = city_performance_df.sort_values(
    by="profit_margin",
    ascending=False
)

# Highest and lowest profit margin cities
best_margin_city = margin_df.iloc[0]
lowest_margin_city = margin_df.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Highest Profit Margin",
        best_margin_city["city"],
        f"{best_margin_city['profit_margin']:.2f}%"
    )

with col2:
    st.metric(
        "Lowest Profit Margin",
        lowest_margin_city["city"],
        f"{lowest_margin_city['profit_margin']:.2f}%"
    )

# Profit margin chart
st.subheader("Profit Margin by City")

st.bar_chart(
    margin_df.set_index("city")["profit_margin"],
    horizontal=True
)

# Detailed table
st.dataframe(
    margin_df[
        ["city", "net_revenue", "total_profit", "profit_margin"]
    ],
    hide_index=True
)


# ==================================
# PRODUCT SALES PERFORMANCE
# ==================================

st.subheader("Product Sales Performance Comparison")

product_performance_query = """
SELECT
    p.product_name,

    SUM(oi.quantity) AS units_sold,

    COUNT(DISTINCT o.order_id) AS total_orders,

    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue,

    SUM(
        oi.quantity *
        (
            oi.selling_price * (1 - oi.discount / 100)
            - p.cost_price
        )
    ) AS total_profit

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN products AS p
    ON oi.product_id = p.product_id

WHERE o.order_status = 'Delivered'

GROUP BY p.product_id, p.product_name

ORDER BY net_revenue DESC;
"""

product_performance_df = pd.read_sql(
    text(product_performance_query),
    engine
)

# Calculate profit margin
product_performance_df["profit_margin"] = (
    product_performance_df["total_profit"]
    / product_performance_df["net_revenue"]
    * 100
)

# Top 10 products by revenue
st.subheader("Top 10 Products by Revenue")

st.bar_chart(
    product_performance_df
    .head(10)
    .set_index("product_name")["net_revenue"],
    horizontal=True
)

# Top 10 products by profit
st.subheader("Top 10 Products by Profit")

top_profit_products = product_performance_df.sort_values(
    by="total_profit",
    ascending=False
).head(10)

st.bar_chart(
    top_profit_products.set_index("product_name")["total_profit"],
    horizontal=True
)

# Complete product performance table
st.subheader("Product Performance Details")

st.dataframe(
    product_performance_df,
    hide_index=True
)


# ==================================
# MONTHLY REVENUE VS PROFIT
# ==================================

st.subheader("Monthly Revenue vs Profit Comparison")

monthly_comparison_query = """
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,

    SUM(
        oi.quantity * oi.selling_price *
        (1 - oi.discount / 100)
    ) AS net_revenue,

    SUM(
        oi.quantity *
        (
            oi.selling_price * (1 - oi.discount / 100)
            - p.cost_price
        )
    ) AS total_profit

FROM orders AS o

INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id

INNER JOIN products AS p
    ON oi.product_id = p.product_id

WHERE o.order_status = 'Delivered'

GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')

ORDER BY month;
"""

monthly_comparison_df = pd.read_sql(
    text(monthly_comparison_query),
    engine
)

# Display comparison chart
st.line_chart(
    monthly_comparison_df.set_index("month")[
        ["net_revenue", "total_profit"]
    ]
)

# Display monthly comparison table
st.dataframe(
    monthly_comparison_df,
    hide_index=True
)
