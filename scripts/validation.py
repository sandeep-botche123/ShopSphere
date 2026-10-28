import pandas as pd

print("=" * 60)
print("ShopSphere - FINAL DATA VALIDATION")
print("=" * 60)

# ============================================================
# LOAD GENERATED DATA
# ============================================================

import os

# Get the ShopSphere project folder
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CSV files are stored inside data/raw
RAW_DATA_PATH = os.path.join(PROJECT_PATH, "data", "raw")

customers = pd.read_csv(os.path.join(RAW_DATA_PATH, "customers.csv"))
categories = pd.read_csv(os.path.join(RAW_DATA_PATH, "categories.csv"))
products = pd.read_csv(os.path.join(RAW_DATA_PATH, "products.csv"))
orders = pd.read_csv(os.path.join(RAW_DATA_PATH, "orders.csv"))
order_items = pd.read_csv(os.path.join(RAW_DATA_PATH, "order_items.csv"))
payments = pd.read_csv(os.path.join(RAW_DATA_PATH, "payments.csv"))
deliveries = pd.read_csv(os.path.join(RAW_DATA_PATH, "deliveries.csv"))
reviews = pd.read_csv(os.path.join(RAW_DATA_PATH, "reviews.csv"))

# Convert dates
customers["signup_date"] = pd.to_datetime(customers["signup_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])
payments["payment_date"] = pd.to_datetime(payments["payment_date"])
deliveries["shipped_date"] = pd.to_datetime(deliveries["shipped_date"])
deliveries["delivered_date"] = pd.to_datetime(deliveries["delivered_date"])
reviews["review_date"] = pd.to_datetime(reviews["review_date"])


errors = []


def check(condition, message):
    if condition:
        print(f"PASS  - {message}")
    else:
        print(f"FAIL  - {message}")
        errors.append(message)


# ============================================================
# 1. ROW COUNT VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("1. ROW COUNT VALIDATION")
print("=" * 60)

check(len(customers) == 2500, "Customers = 2,500")
check(len(categories) == 5, "Categories = 5")
check(len(products) == 100, "Products = 100")
check(len(orders) == 20000, "Orders = 20,000")
check(len(order_items) >= 30000, "Order Items >= 30,000")
check(len(payments) == 20000, "Payments = 20,000")
check(len(deliveries) == 17142, "Deliveries = Delivered orders")
check(len(reviews) >= 5000, "Reviews >= 5,000")


# ============================================================
# 2. PRIMARY KEY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("2. PRIMARY KEY VALIDATION")
print("=" * 60)

check(
    customers["customer_id"].notna().all()
    and customers["customer_id"].is_unique,
    "Customer IDs are unique and non-null"
)

check(
    categories["category_id"].notna().all()
    and categories["category_id"].is_unique,
    "Category IDs are unique and non-null"
)

check(
    products["product_id"].notna().all()
    and products["product_id"].is_unique,
    "Product IDs are unique and non-null"
)

check(
    orders["order_id"].notna().all()
    and orders["order_id"].is_unique,
    "Order IDs are unique and non-null"
)

check(
    order_items["order_item_id"].notna().all()
    and order_items["order_item_id"].is_unique,
    "Order Item IDs are unique and non-null"
)

check(
    payments["payment_id"].notna().all()
    and payments["payment_id"].is_unique,
    "Payment IDs are unique and non-null"
)

check(
    deliveries["delivery_id"].notna().all()
    and deliveries["delivery_id"].is_unique,
    "Delivery IDs are unique and non-null"
)

check(
    reviews["review_id"].notna().all()
    and reviews["review_id"].is_unique,
    "Review IDs are unique and non-null"
)


# ============================================================
# 3. FOREIGN KEY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("3. FOREIGN KEY VALIDATION")
print("=" * 60)

check(
    orders["customer_id"].isin(customers["customer_id"]).all(),
    "Every order customer exists"
)

check(
    products["category_id"].isin(categories["category_id"]).all(),
    "Every product category exists"
)

check(
    order_items["order_id"].isin(orders["order_id"]).all(),
    "Every order item belongs to an order"
)

check(
    order_items["product_id"].isin(products["product_id"]).all(),
    "Every order item references an existing product"
)

check(
    payments["order_id"].isin(orders["order_id"]).all(),
    "Every payment belongs to an order"
)

check(
    deliveries["order_id"].isin(orders["order_id"]).all(),
    "Every delivery belongs to an order"
)

check(
    reviews["order_id"].isin(orders["order_id"]).all(),
    "Every review references an existing order"
)

check(
    reviews["customer_id"].isin(customers["customer_id"]).all(),
    "Every review references an existing customer"
)

check(
    reviews["product_id"].isin(products["product_id"]).all(),
    "Every review references an existing product"
)


# ============================================================
# 4. ORDER DATE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("4. ORDER DATE VALIDATION")
print("=" * 60)

check(
    orders["order_date"].between(
        pd.Timestamp("2025-01-01"),
        pd.Timestamp("2025-12-31")
    ).all(),
    "All order dates are within 2025"
)

order_customer_dates = orders.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id",
    how="left"
)

check(
    (order_customer_dates["order_date"]
     > order_customer_dates["signup_date"]).all(),
    "Orders occur after customer signup"
)
# Show orders where the order date is NOT after signup date
invalid_signup_orders = order_customer_dates[
    order_customer_dates["order_date"]
    <= order_customer_dates["signup_date"]
].copy()

if len(invalid_signup_orders) > 0:
    print("\n--- Orders with invalid signup/order dates ---")
    print(
        invalid_signup_orders[
            [
                "order_id",
                "customer_id",
                "signup_date",
                "order_date"
            ]
        ].sort_values("order_date").head(20)
    )

    print(
        f"\nTotal invalid orders: {len(invalid_signup_orders)}"
    )


# ============================================================
# 5. ORDER STATUS VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("5. ORDER STATUS VALIDATION")
print("=" * 60)

valid_order_statuses = {"Delivered", "Cancelled"}

check(
    set(orders["order_status"].unique()).issubset(valid_order_statuses),
    "Order statuses are valid"
)


# ============================================================
# 6. ORDER ITEM VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("6. ORDER ITEM VALIDATION")
print("=" * 60)

check(
    orders["order_id"].isin(order_items["order_id"]).all(),
    "Every order has at least one order item"
)

check(
    order_items["quantity"].between(1, 3).all(),
    "All quantities are between 1 and 3"
)

check(
    (order_items["selling_price"] > 0).all(),
    "All selling prices are positive"
)

check(
    order_items["discount"].between(0, 20).all(),
    "All discounts are between 0% and 20%"
)


# ============================================================
# 7. DELIVERY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("7. DELIVERY VALIDATION")
print("=" * 60)

cancelled_orders = set(
    orders.loc[
        orders["order_status"] == "Cancelled",
        "order_id"
    ]
)

delivery_orders = set(deliveries["order_id"])

check(
    len(cancelled_orders.intersection(delivery_orders)) == 0,
    "Cancelled orders have no delivery"
)

delivered_orders = set(
    orders.loc[
        orders["order_status"] == "Delivered",
        "order_id"
    ]
)

check(
    delivery_orders == delivered_orders,
    "Every delivered order has exactly one delivery"
)

check(
    (
        deliveries.loc[
            deliveries["delivery_status"] == "Delivered",
            "delivered_date"
        ].notna()
    ).all(),
    "Delivered shipments have delivered dates"
)

check(
    (
        deliveries.loc[
            deliveries["delivery_status"] == "In Transit",
            "delivered_date"
        ].isna()
    ).all(),
    "In-transit shipments have no delivered date"
)

check(
    (
        deliveries["shipped_date"]
        >= deliveries["order_id"].map(
            orders.set_index("order_id")["order_date"]
        )
    ).all(),
    "Shipment dates are on/after order dates"
)

delivered_rows = deliveries[
    deliveries["delivery_status"] == "Delivered"
].copy()

check(
    (
        delivered_rows["delivered_date"]
        >= delivered_rows["shipped_date"]
    ).all(),
    "Delivered dates are on/after shipped dates"
)


# ============================================================
# 8. PAYMENT VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("8. PAYMENT VALIDATION")
print("=" * 60)

check(
    len(payments) == len(orders),
    "Every order has exactly one payment record"
)

check(
    (
        payments["payment_date"]
        == payments["order_id"].map(
            orders.set_index("order_id")["order_date"]
        )
    ).all(),
    "Payment dates match order dates"
)

cancelled_payments = payments[
    payments["order_id"].isin(cancelled_orders)
]

check(
    (cancelled_payments["amount"] == 0).all(),
    "Cancelled orders have zero payment amount"
)

delivered_payments = payments[
    payments["order_id"].isin(delivered_orders)
]

check(
    (delivered_payments["payment_status"] == "Successful").all(),
    "Delivered orders have successful payments"
)

check(
    (payments["amount"] >= 0).all(),
    "Payment amounts are non-negative"
)


# ============================================================
# 9. REVIEW VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("9. REVIEW VALIDATION")
print("=" * 60)

check(
    reviews["rating"].between(1, 5).all(),
    "Ratings are between 1 and 5"
)

review_order_customer = reviews.merge(
    orders[["order_id", "customer_id"]],
    on="order_id",
    how="left",
    suffixes=("_review", "_order")
)

check(
    (
        review_order_customer["customer_id_review"]
        == review_order_customer["customer_id_order"]
    ).all(),
    "Review customer matches order customer"
)

check(
    reviews["order_id"].isin(
        orders.loc[
            orders["order_status"] == "Delivered",
            "order_id"
        ]
    ).all(),
    "Reviews belong only to delivered orders"
)

# Product must have been purchased in the reviewed order
review_product_check = reviews.merge(
    order_items[["order_id", "product_id"]].drop_duplicates(),
    on=["order_id", "product_id"],
    how="left",
    indicator=True
)

check(
    (review_product_check["_merge"] == "both").all(),
    "Reviewed products belong to the reviewed orders"
)

# Review date must be after delivery date
review_delivery_check = reviews.merge(
    deliveries[
        ["order_id", "delivery_status", "delivered_date"]
    ],
    on="order_id",
    how="left"
)

delivered_reviews = review_delivery_check[
    review_delivery_check["delivery_status"] == "Delivered"
].copy()

check(
    (
        delivered_reviews["review_date"]
        > delivered_reviews["delivered_date"]
    ).all(),
    "Review dates occur after delivery"
)


# ============================================================
# 10. DATA QUALITY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("10. DATA QUALITY VALIDATION")
print("=" * 60)

check(
    not customers.isna().any().any(),
    "Customers contain no missing values"
)

check(
    not categories.isna().any().any(),
    "Categories contain no missing values"
)

check(
    not products.isna().any().any(),
    "Products contain no missing values"
)

check(
    not orders.isna().any().any(),
    "Orders contain no missing values"
)

check(
    not order_items.isna().any().any(),
    "Order items contain no missing values"
)

check(
    not payments.isna().any().any(),
    "Payments contain no missing values"
)

# Deliveries intentionally have missing delivered_date
# for In Transit orders.
invalid_delivery_missing = deliveries[
    (
        deliveries["delivery_status"] == "Delivered"
    ) & (
        deliveries["delivered_date"].isna()
    )
]

check(
    len(invalid_delivery_missing) == 0,
    "Delivered shipments do not have missing delivered dates"
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 60)
print("FINAL VALIDATION RESULT")
print("=" * 60)

if len(errors) == 0:
    print("SUCCESS - ALL VALIDATION CHECKS PASSED!")
    print("ShopSphere dataset is ready to freeze.")
else:
    print(f"FAILED - {len(errors)} validation checks failed.")
    print("\nProblems found:")

    for error in errors:
        print(f"- {error}")

print("=" * 60)