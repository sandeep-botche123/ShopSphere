from Database import load_data
import pandas as pd


# Load ShopSphere tables

customers = load_data("customers")
categories = load_data("categories")
products = load_data("products")
orders = load_data("orders")
order_items = load_data("order_items")
payments = load_data("payments")
deliveries = load_data("deliveries")
reviews = load_data("reviews")


print("All tables loaded successfully.")
# ==========================================
# CONVERT DATE COLUMNS
# ==========================================

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

payments["payment_date"] = pd.to_datetime(
    payments["payment_date"]
)

deliveries["shipped_date"] = pd.to_datetime(
    deliveries["shipped_date"]
)

deliveries["delivered_date"] = pd.to_datetime(
    deliveries["delivered_date"]
)

reviews["review_date"] = pd.to_datetime(
    reviews["review_date"]
)
# Merge order items with orders
sales = order_items.merge(
    orders[["order_id", "customer_id", "order_date", "order_status"]],
    on="order_id",
    how="left"
)

# Keep only delivered orders
delivered_sales = sales[
    sales["order_status"] == "Delivered"
].copy()


# Calculate gross revenue
delivered_sales["gross_revenue"] = (
    delivered_sales["quantity"]
    * delivered_sales["selling_price"]
)


# Calculate net revenue after discount
delivered_sales["net_revenue"] = (
    delivered_sales["gross_revenue"]
    * (1 - delivered_sales["discount"] / 100)
)


print("\n--- Delivered Sales ---")
print(delivered_sales.head())

# Basic Business KPIs

total_orders = delivered_sales["order_id"].nunique()

total_customers = delivered_sales["customer_id"].nunique()

gross_revenue = delivered_sales["gross_revenue"].sum()

net_revenue = delivered_sales["net_revenue"].sum()

total_quantity = delivered_sales["quantity"].sum()

aov = net_revenue / total_orders


print("\n--- ShopSphere KPIs ---")

print("Delivered Orders:", total_orders)

print("Unique Customers:", total_customers)

print("Gross Revenue: ₹", round(gross_revenue, 2))

print("Net Revenue: ₹", round(net_revenue, 2))

print("Total Quantity Sold:", total_quantity)

print("Average Order Value: ₹", round(aov, 2))

# ==========================================
# PRODUCT PERFORMANCE ANALYSIS
# ==========================================


# Add product information to delivered sales
product_sales = delivered_sales.merge(
    products[["product_id", "product_name", "category_id"]],
    on="product_id",
    how="left"
)


# ------------------------------------------
# 1. Product Revenue
# ------------------------------------------


product_revenue = (
    product_sales
    .groupby(["product_id", "product_name"], as_index=False)
    .agg(
        quantity_sold=("quantity", "sum"),
        gross_revenue=("gross_revenue", "sum"),
        net_revenue=("net_revenue", "sum")
    )
    .sort_values("net_revenue", ascending=False)
)


print("\n--- Product Performance ---")
print(product_revenue)

# Top 5 products by net revenue

top_5_products = product_revenue.head(5)

print("\n--- Top 5 Products by Net Revenue ---")
print(top_5_products)

# Top 5 products by quantity sold

top_5_quantity = (
    product_revenue
    .sort_values("quantity_sold", ascending=False)
    .head(5)
)


print("\n--- Top 5 Products by Quantity Sold ---")
print(top_5_quantity)

# ==========================================
# CATEGORY PERFORMANCE ANALYSIS
# ==========================================


# Add category names
category_sales = product_sales.merge(
    categories[["category_id", "category_name"]],
    on="category_id",
    how="left"
)


# Calculate category-level performance
category_performance = (
    category_sales
    .groupby("category_name", as_index=False)
    .agg(
        quantity_sold=("quantity", "sum"),
        gross_revenue=("gross_revenue", "sum"),
        net_revenue=("net_revenue", "sum")
    )
    .sort_values("net_revenue", ascending=False)
)


# Calculate revenue contribution percentage
category_performance["revenue_contribution_pct"] = (
    category_performance["net_revenue"]
    / category_performance["net_revenue"].sum()
    * 100
)


print("\n--- Category Performance ---")
print(category_performance)

# Strongest category by net revenue

strongest_category = category_performance.iloc[0]

print("\n--- Strongest Category ---")
print(strongest_category)


# Weakest category by net revenue

weakest_category = category_performance.iloc[-1]

print("\n--- Weakest Category ---")
print(weakest_category)

# ==========================================
# CATEGORY REVENUE VISUALIZATION
# ==========================================

import matplotlib.pyplot as plt


plt.figure(figsize=(8, 5))

plt.bar(
    category_performance["category_name"],
    category_performance["net_revenue"]
)

plt.title("Net Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Net Revenue (₹)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.show()

# ==========================================
# CUSTOMER PERFORMANCE ANALYSIS
# ==========================================


# Calculate customer-level performance

customer_performance = (
    delivered_sales
    .groupby("customer_id", as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum"),
        total_revenue=("net_revenue", "sum")
    )
)


# Add customer names

customer_performance = customer_performance.merge(
    customers[["customer_id", "customer_name", "city"]],
    on="customer_id",
    how="left"
)


# Sort customers by revenue

customer_performance = customer_performance.sort_values(
    "total_revenue",
    ascending=False
)
# ==========================================
# CUSTOMER REVENUE RANKING
# ==========================================

customer_performance["revenue_rank"] = (
    customer_performance["total_revenue"]
    .rank(method="dense", ascending=False)
    .astype(int)
)


print("\n--- Customer Revenue Ranking ---")
print(
    customer_performance[
        [
            "revenue_rank",
            "customer_name",
            "city",
            "total_orders",
            "total_quantity",
            "total_revenue"
        ]
    ]
)


print("\n--- Customer Performance ---")
print(customer_performance)


# ==========================================
# CUSTOMER SEGMENTATION
# ==========================================

customer_performance["customer_segment"] = pd.qcut(
    customer_performance["total_revenue"].rank(method="first"),
    q=4,
    labels=[
        "Low Value",
        "Medium Value",
        "High Value",
        "Top Value"
    ]
)

print("\n--- Customer Segmentation ---")

print(
    customer_performance[
        ["customer_name", "total_revenue", "customer_segment"]
    ]
)

segment_summary = (
    customer_performance
    .groupby("customer_segment", observed=True)
    .agg(
        customer_count=("customer_id", "nunique"),
        total_revenue=("total_revenue", "sum")
    )
    .reset_index()
)

print("\n--- Customer Segment Summary ---")
print(segment_summary)

segment_summary["revenue_contribution_pct"] = (
    segment_summary["total_revenue"]
    / segment_summary["total_revenue"].sum()
    * 100
)

print("\n--- Customer Segment Revenue Contribution ---")
print(segment_summary)


# ==========================================
# CITY PERFORMANCE ANALYSIS
# ==========================================


# Calculate city-level performance

city_performance = (
    customer_performance
    .groupby("city", as_index=False)
    .agg(
        customers=("customer_id", "nunique"),
        total_orders=("total_orders", "sum"),
        total_revenue=("total_revenue", "sum")
    )
    .sort_values("total_revenue", ascending=False)
)


# Calculate revenue contribution

city_performance["revenue_contribution_pct"] = (
    city_performance["total_revenue"]
    / city_performance["total_revenue"].sum()
    * 100
)


print("\n--- City Performance ---")
print(city_performance)

# ==========================================
# TOP REVENUE CITIES
# ==========================================

top_cities = city_performance.head(5)


print("\n--- Top Revenue Cities ---")
print(top_cities)
# ==========================================
# ORDER STATUS ANALYSIS
# ==========================================


order_status_summary = (
    orders
    .groupby("order_status")
    .agg(
        order_count=("order_id", "nunique")

    )
    .reset_index()
)# ==========================================
# CANCELLATION RATE
# ==========================================


total_all_orders = orders["order_id"].nunique()

cancelled_orders = orders[
    orders["order_status"] == "Cancelled"
]["order_id"].nunique()


cancellation_rate = (
    cancelled_orders
    / total_all_orders
    * 100
)


print("\n--- Cancellation Analysis ---")
print("Total Orders:", total_all_orders)
print("Cancelled Orders:", cancelled_orders)
print("Cancellation Rate:", round(cancellation_rate, 2), "%")

# ==========================================
# CUSTOMER CANCELLATION ANALYSIS
# ==========================================


cancelled_customer_orders = (
    orders[orders["order_status"] == "Cancelled"]
    .groupby("customer_id", as_index=False)
    .agg(
        cancelled_orders=("order_id", "nunique")
    )
)


# Add customer information

cancelled_customer_orders = cancelled_customer_orders.merge(
    customers[["customer_id", "customer_name", "city"]],
    on="customer_id",
    how="left"
)


# Sort by cancelled orders

cancelled_customer_orders = cancelled_customer_orders.sort_values(
    "cancelled_orders",
    ascending=False
)


print("\n--- Customer Cancellation Analysis ---")
print(cancelled_customer_orders)

# ==========================================
# PAYMENT METHOD PERFORMANCE
# ==========================================


payment_sales = delivered_sales.merge(
    orders[["order_id", "payment_method"]],
    on="order_id",
    how="left"
)


payment_performance = (
    payment_sales
    .groupby("payment_method", as_index=False)
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        revenue=("net_revenue", "sum")
    )
)


# Calculate AOV

payment_performance["aov"] = (
    payment_performance["revenue"]
    / payment_performance["orders"]
)


print("\n--- Payment Method Performance ---")
print(payment_performance)
# ==========================================
# PAYMENT SUCCESS RATE BY PAYMENT METHOD
# ==========================================

payment_summary = (
    payments
    .groupby("payment_method", as_index=False)
    .agg(
        total_payments=("payment_id", "nunique"),
        successful_payments=("payment_status", lambda x: (x == "Successful").sum())
    )
)

payment_summary["success_rate_pct"] = (
    payment_summary["successful_payments"]
    / payment_summary["total_payments"]
    * 100
)

print("\n--- Payment Success Rate ---")
print(payment_summary)
# ==========================================
# DELIVERY PERFORMANCE
# ==========================================

delivery_analysis = deliveries.merge(
    orders[["order_id", "customer_id", "order_status"]],
    on="order_id",
    how="left"
)

# Convert dates to datetime
delivery_analysis["shipped_date"] = pd.to_datetime(
    delivery_analysis["shipped_date"]
)

delivery_analysis["delivered_date"] = pd.to_datetime(
    delivery_analysis["delivered_date"]
)

# Calculate delivery time in days
delivery_analysis["delivery_days"] = (
    delivery_analysis["delivered_date"]
    - delivery_analysis["shipped_date"]
).dt.days

print("\n--- Delivery Performance ---")

print(
    delivery_analysis[
        [
            "order_id",
            "shipped_date",
            "delivered_date",
            "delivery_status",
            "delivery_days"
        ]
    ]
)

# Average delivery time for completed deliveries
average_delivery_time = (
    delivery_analysis.loc[
        delivery_analysis["delivery_status"] == "Delivered",
        "delivery_days"
    ].mean()
)

print(
    "\nAverage Delivery Time:",
    round(average_delivery_time, 2),
    "days"
)
# ==========================================
# SLOWEST DELIVERIES
# ==========================================

slowest_deliveries = (
    delivery_analysis[
        delivery_analysis["delivery_status"] == "Delivered"
    ]
    .sort_values("delivery_days", ascending=False)
    .head(5)
)

print("\n--- Top 5 Slowest Deliveries ---")

print(
    slowest_deliveries[
        [
            "order_id",
            "shipped_date",
            "delivered_date",
            "delivery_days"
        ]
    ]
)
# ==========================================
# DELIVERY STATUS SUMMARY
# ==========================================

delivery_status_summary = (
    deliveries
    .groupby("delivery_status", as_index=False)
    .agg(
        order_count=("order_id", "nunique")
    )
)

delivery_status_summary["percentage"] = (
    delivery_status_summary["order_count"]
    / delivery_status_summary["order_count"].sum()
    * 100
)

print("\n--- Delivery Status Summary ---")
print(delivery_status_summary)# ==========================================
# ==========================================
# REVIEW ANALYSIS
# ==========================================

review_analysis = reviews.merge(
    products[["product_id", "product_name", "category_id"]],
    on="product_id",
    how="left"
)

review_analysis = review_analysis.merge(
    categories[["category_id", "category_name"]],
    on="category_id",
    how="left"
)

# Average rating for each product
product_ratings = (
    review_analysis
    .groupby(
        ["product_id", "product_name"],
        as_index=False
    )
    .agg(
        average_rating=("rating", "mean"),
        review_count=("review_id", "nunique")
    )
    .sort_values("average_rating", ascending=False)
)

print("\n--- Product Ratings ---")
print(product_ratings)

# Top 5 highest-rated products
top_rated_products = (
    product_ratings
    .head(5)
)

print("\n--- Top 5 Highest-Rated Products ---")
print(top_rated_products)

# Average rating by category
category_ratings = (
    review_analysis
    .groupby("category_name", as_index=False)
    .agg(
        average_rating=("rating", "mean"),
        review_count=("review_id", "nunique")
    )
    .sort_values("average_rating", ascending=False)
)

print("\n--- Category Ratings ---")
print(category_ratings)

# Products with rating below 3.5
low_rated_products = product_ratings[
    product_ratings["average_rating"] < 3.5
]

print("\n--- Products With Rating Below 3.5 ---")
print(low_rated_products)

# ==========================================
# REVENUE VS PRODUCT RATING
# ==========================================

product_revenue_rating = product_revenue.merge(
    product_ratings[
        [
            "product_id",
            "product_name",
            "average_rating",
            "review_count"
        ]
    ],
    on="product_id",
    how="left",
    suffixes=("", "_rating")
)

# Keep one product name column
if "product_name_rating" in product_revenue_rating.columns:
    product_revenue_rating = product_revenue_rating.drop(
        columns=["product_name_rating"]
    )

product_revenue_rating = product_revenue_rating[
    [
        "product_id",
        "product_name",
        "quantity_sold",
        "net_revenue",
        "average_rating",
        "review_count"
    ]
].sort_values(
    "net_revenue",
    ascending=False
)

# Classify products based on revenue and rating
product_revenue_rating["business_category"] = "Other"

product_revenue_rating.loc[
    (product_revenue_rating["net_revenue"] >= 10000) &
    (product_revenue_rating["average_rating"] >= 4.0),
    "business_category"
] = "Promote"

product_revenue_rating.loc[
    (product_revenue_rating["net_revenue"] >= 10000) &
    (product_revenue_rating["average_rating"] < 3.5),
    "business_category"
] = "Investigate"

product_revenue_rating.loc[
    (product_revenue_rating["net_revenue"] < 10000) &
    (product_revenue_rating["average_rating"] >= 4.0),
    "business_category"
] = "Growth Opportunity"

print("\n--- Revenue vs Product Rating ---")
print(product_revenue_rating)

print("\n--- Products to Promote ---")
print(
    product_revenue_rating[
        product_revenue_rating["business_category"] == "Promote"
    ]
)

print("\n--- Products to Investigate ---")
print(
    product_revenue_rating[
        product_revenue_rating["business_category"] == "Investigate"
    ]
)

print("\n--- Growth Opportunities ---")
print(
    product_revenue_rating[
        product_revenue_rating["business_category"] == "Growth Opportunity"
    ]
)


# ==========================================
# REPEAT CUSTOMER ANALYSIS
# ==========================================

repeat_customers = (
    delivered_sales
    .groupby("customer_id", as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("net_revenue", "sum")
    )
)

repeat_customers = repeat_customers[
    repeat_customers["total_orders"] > 1
]

repeat_customers = repeat_customers.merge(
    customers[
        [
            "customer_id",
            "customer_name",
            "city"
        ]
    ],
    on="customer_id",
    how="left"
)

repeat_customers = repeat_customers.sort_values(
    "total_revenue",
    ascending=False
)

print("\n--- Repeat Customers ---")
print(repeat_customers)

# ==========================================
# REPEAT CUSTOMER RATE
# ==========================================

total_delivered_customers = delivered_sales[
    "customer_id"
].nunique()

number_of_repeat_customers = repeat_customers[
    "customer_id"
].nunique()

repeat_customer_rate = (
    number_of_repeat_customers
    / total_delivered_customers
    * 100
)

print(
    "\nRepeat Customer Rate:",
    round(repeat_customer_rate, 2),
    "%"
)

# ==========================================
# CUSTOMER FIRST & LATEST PURCHASE
# ==========================================

customer_purchase_dates = (
    delivered_sales
    .groupby("customer_id", as_index=False)
    .agg(
        first_order_date=("order_date", "min"),
        latest_order_date=("order_date", "max")
    )
)

# Make sure both columns are datetime

customer_purchase_dates["first_order_date"] = pd.to_datetime(
    customer_purchase_dates["first_order_date"]
)

customer_purchase_dates["latest_order_date"] = pd.to_datetime(
    customer_purchase_dates["latest_order_date"]
)

# Calculate number of days between first and latest order

customer_purchase_dates["days_between_orders"] = (
    customer_purchase_dates["latest_order_date"]
    - customer_purchase_dates["first_order_date"]
).dt.days

# Add customer details

customer_purchase_dates = customer_purchase_dates.merge(
    customers[
        [
            "customer_id",
            "customer_name",
            "city"
        ]
    ],
    on="customer_id",
    how="left"
)

print("\n--- Customer Purchase Timeline ---")

print(
    customer_purchase_dates[
        [
            "customer_id",
            "customer_name",
            "city",
            "first_order_date",
            "latest_order_date",
            "days_between_orders"
        ]
    ]
)

# ==========================================
# MONTHLY SALES TREND
# ==========================================

delivered_sales["month"] = (
    delivered_sales["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    delivered_sales
    .groupby("month", as_index=False)
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        quantity_sold=("quantity", "sum"),
        net_revenue=("net_revenue", "sum")
    )
    .sort_values("month")
)

print("\n--- Monthly Sales Trend ---")

print(monthly_sales)

print("\n--- Monthly Revenue Validation ---")

print(
    "Monthly revenue total:",
    round(monthly_sales["net_revenue"].sum(), 2)
)

print(
    "Overall net revenue:",
    round(net_revenue, 2)
)

print(
    "Difference:",
    round(monthly_sales["net_revenue"].sum() - net_revenue, 2)
)


# ==========================================
# DAILY SALES ANALYSIS
# ==========================================

daily_sales = (
    delivered_sales
    .groupby("order_date", as_index=False)
    .agg(
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique"),
        quantity_sold=("quantity", "sum"),
        net_revenue=("net_revenue", "sum")
    )
    .sort_values("order_date")
)

print("\n--- Daily Sales Analysis ---")

print(daily_sales)

# ==========================================
# HIGHEST REVENUE DATE
# ==========================================

highest_revenue_day = daily_sales.loc[
    daily_sales["net_revenue"].idxmax()
]

print("\n--- Highest Revenue Date ---")
print(highest_revenue_day)

# ==========================================
# RUNNING / CUMULATIVE REVENUE
# ==========================================

daily_sales["cumulative_revenue"] = (
    daily_sales["net_revenue"].cumsum()
)

print("\n--- Running Revenue ---")
print(
    daily_sales[
        ["order_date", "net_revenue", "cumulative_revenue"]
    ]
)
# ==========================================
# ORDER STATUS ANALYSIS
# ==========================================

order_status_analysis = (
    orders
    .groupby("order_status")
    .agg(
        order_count=("order_id", "nunique")
    )
    .reset_index()
)

order_status_analysis["percentage"] = (
    order_status_analysis["order_count"]
    / order_status_analysis["order_count"].sum()
    * 100
)

print("\n--- Order Status Analysis ---")
print(order_status_analysis)

# ==========================================
# CANCELLATION RATE BY CITY
# ==========================================

city_cancellation = (
    orders
    .merge(
        customers[["customer_id", "city"]],
        on="customer_id",
        how="left"
    )
    .groupby("city", as_index=False)
    .agg(
        total_orders=("order_id", "nunique"),
        cancelled_orders=("order_status", lambda x: (x == "Cancelled").sum())
    )
)

city_cancellation["cancellation_rate_pct"] = (
    city_cancellation["cancelled_orders"]
    / city_cancellation["total_orders"]
    * 100
)

city_cancellation = city_cancellation.sort_values(
    "cancellation_rate_pct",
    ascending=False
)

print("\n--- Cancellation Rate by City ---")
print(city_cancellation)

# ==========================================
# PRODUCT PROFITABILITY
# ==========================================

product_profitability = (
    delivered_sales
    .groupby("product_id", as_index=False)
    .agg(
        quantity_sold=("quantity", "sum"),
        net_revenue=("net_revenue", "sum")
    )
)

product_profitability = product_profitability.merge(
    products[
        ["product_id", "product_name", "cost_price"]
    ],
    on="product_id",
    how="left"
)

product_profitability["total_cost"] = (
    product_profitability["quantity_sold"]
    * product_profitability["cost_price"]
)

product_profitability["profit"] = (
    product_profitability["net_revenue"]
    - product_profitability["total_cost"]
)

product_profitability["profit_margin_pct"] = (
    product_profitability["profit"]
    / product_profitability["net_revenue"]
    * 100
)

product_profitability = product_profitability.sort_values(
    "profit",
    ascending=False
)

print("\n--- Product Profitability ---")
print(product_profitability)

# ==========================================
# CATEGORY PROFITABILITY
# ==========================================

category_sales = delivered_sales.merge(
    products[
        ["product_id", "category_id", "cost_price"]
    ],
    on="product_id",
    how="left"
)

# Calculate cost for each sold item
category_sales["total_cost"] = (
    category_sales["quantity"]
    * category_sales["cost_price"]
)

# Aggregate category performance
category_profitability = (
    category_sales
    .groupby("category_id", as_index=False)
    .agg(
        quantity_sold=("quantity", "sum"),
        net_revenue=("net_revenue", "sum"),
        total_cost=("total_cost", "sum")
    )
)

# Calculate profit
category_profitability["profit"] = (
    category_profitability["net_revenue"]
    - category_profitability["total_cost"]
)

# Calculate profit margin
category_profitability["profit_margin_pct"] = (
    category_profitability["profit"]
    / category_profitability["net_revenue"]
    * 100
)

# Add category name
category_profitability = category_profitability.merge(
    categories,
    on="category_id",
    how="left"
)

# Sort by profit
category_profitability = category_profitability.sort_values(
    "profit",
    ascending=False
)

print("\n--- Category Profitability ---")
print(category_profitability)

from pathlib import Path

# Create the processed-data folder path
project_root = Path(__file__).resolve().parent.parent
processed_folder = project_root / "data" / "processed"
processed_folder.mkdir(parents=True, exist_ok=True)

# Analysis results to export
analysis_results = {
    "monthly_sales": "monthly_sales",
    "daily_sales": "daily_sales",
    "running_revenue": "running_revenue",
    "product_performance": "product_revenue",
    "category_performance": "category_performance",
    "customer_performance": "customer_performance",
    "city_performance": "city_performance",
    "product_ratings": "product_ratings",
    "category_ratings": "category_ratings",
    "product_revenue_rating": "product_revenue_rating",
    "product_profitability": "product_profitability",
    "category_profitability": "category_profitability",
    "delivery_status_summary": "delivery_status_summary",
}

# Save available DataFrames as CSV files
for file_name, variable_name in analysis_results.items():
    df = globals().get(variable_name)

    if isinstance(df, pd.DataFrame):
        df.to_csv(
            processed_folder / f"{file_name}.csv",
            index=False
        )
        print(f"Saved: {file_name}.csv")
    else:
        print(f"Skipped: {variable_name} (DataFrame not found)")

print(f"\nProcessed files location: {processed_folder}")
