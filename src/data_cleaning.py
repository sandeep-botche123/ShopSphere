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


# Basic data inspection

print("\n--- Customers ---")
print(customers.head())

print("\n--- Orders ---")
print(orders.head())

print("\n--- Products ---")
print(products.head())

print("\n--- Missing Values ---")
print("Customers:")
print(customers.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())

print("\nPayments:")
print(payments.isnull().sum())

print("\nDeliveries:")
print(deliveries.isnull().sum())

print("\nReviews:")
print(reviews.isnull().sum())
print("\n--- Undelivered Orders ---")
print(
    deliveries[
        deliveries["delivered_date"].isnull()
    ]
)
# Convert date columns to datetime

customers["signup_date"] = pd.to_datetime(customers["signup_date"])

orders["order_date"] = pd.to_datetime(orders["order_date"])

payments["payment_date"] = pd.to_datetime(payments["payment_date"])

deliveries["shipped_date"] = pd.to_datetime(deliveries["shipped_date"])
deliveries["delivered_date"] = pd.to_datetime(deliveries["delivered_date"])

reviews["review_date"] = pd.to_datetime(reviews["review_date"])
print("\n--- Date Data Types ---")

print("Customers:", customers["signup_date"].dtype)
print("Orders:", orders["order_date"].dtype)
print("Payments:", payments["payment_date"].dtype)
print("Shipped:", deliveries["shipped_date"].dtype)
print("Delivered:", deliveries["delivered_date"].dtype)
print("Reviews:", reviews["review_date"].dtype)
print("\n--- Duplicate Rows ---")

print("Customers:", customers.duplicated().sum())
print("Categories:", categories.duplicated().sum())
print("Products:", products.duplicated().sum())
print("Orders:", orders.duplicated().sum())
print("Order Items:", order_items.duplicated().sum())
print("Payments:", payments.duplicated().sum())
print("Deliveries:", deliveries.duplicated().sum())
print("Reviews:", reviews.duplicated().sum())
print("\n--- Numeric Data Validation ---")

print("\nNegative Prices:")
print(products[
    (products["cost_price"] < 0) |
    (products["selling_price"] < 0)
])

print("\nInvalid Quantities:")
print(order_items[
    order_items["quantity"] <= 0
])

print("\nInvalid Discounts:")
print(order_items[
    (order_items["discount"] < 0) |
    (order_items["discount"] > 100)
])

print("\nInvalid Ratings:")
print(reviews[
    (reviews["rating"] < 1) |
    (reviews["rating"] > 5)
])

print("\n--- Referential Integrity Checks ---")

print("\nOrder Items with Invalid Orders:")
print(
    order_items[
        ~order_items["order_id"].isin(orders["order_id"])
    ]
)

print("\nOrder Items with Invalid Products:")
print(
    order_items[
        ~order_items["product_id"].isin(products["product_id"])
    ]
)

print("\nOrders with Invalid Customers:")
print(
    orders[
        ~orders["customer_id"].isin(customers["customer_id"])
    ]
)

print("\nProducts with Invalid Categories:")
print(
    products[
        ~products["category_id"].isin(categories["category_id"])
    ]
)

print("\nReviews with Invalid Products:")
print(
    reviews[
        ~reviews["product_id"].isin(products["product_id"])
    ]
)

print("\nReviews with Invalid Customers:")
print(
    reviews[
        ~reviews["customer_id"].isin(customers["customer_id"])
    ]
)