# ==========================================
# SHOPSPHERE - SYNTHETIC DATA GENERATOR
# ==========================================

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ==========================================
# CONFIGURATION
# ==========================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)


# Number of records we want
NUM_CUSTOMERS = 2500
NUM_PRODUCTS = 100
NUM_ORDERS = 20000


# Business period
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)


print("=" * 60)
print("ShopSphere Synthetic Data Generator")
print("=" * 60)

print(f"Customers : {NUM_CUSTOMERS}")
print(f"Products  : {NUM_PRODUCTS}")
print(f"Orders    : {NUM_ORDERS}")
print(f"Period    : {START_DATE.date()} to {END_DATE.date()}")
print("=" * 60)

# ==========================================
# CATEGORY MASTER DATA
# ==========================================

categories_data = [
    ("CAT01", "Electronics"),
    ("CAT02", "Fashion"),
    ("CAT03", "Home & Kitchen"),
    ("CAT04", "Beauty"),
    ("CAT05", "Sports")
]

categories = pd.DataFrame(
    categories_data,
    columns=["category_id", "category_name"]
)


# ==========================================
# PRODUCT MASTER DATA
# ==========================================

product_templates = {
    "Electronics": [
        ("Smartphone", ["Apple", "Samsung", "OnePlus", "Xiaomi", "Realme"]),
        ("Laptop", ["Dell", "HP", "Lenovo", "Asus", "Acer"]),
        ("Headphones", ["Sony", "JBL", "Boat", "Sennheiser"]),
        ("Smartwatch", ["Apple", "Samsung", "Noise", "Fire-Boltt"]),
        ("Tablet", ["Apple", "Samsung", "Lenovo", "OnePlus"]),
        ("Bluetooth Speaker", ["JBL", "Boat", "Sony", "Marshall"]),
        ("Power Bank", ["Mi", "Ambrane", "Portronics"]),
        ("Wireless Mouse", ["Logitech", "HP", "Dell", "Lenovo"]),
    ],

    "Fashion": [
        ("T-Shirt", ["Puma", "Nike", "Adidas", "Levis", "Roadster"]),
        ("Jeans", ["Levis", "Wrangler", "Lee", "Pepe Jeans"]),
        ("Hoodie", ["Puma", "Adidas", "Nike", "HRX"]),
        ("Sneakers", ["Nike", "Adidas", "Puma", "Skechers"]),
        ("Shirt", ["Van Heusen", "Allen Solly", "Peter England"]),
        ("Jacket", ["Puma", "Nike", "Adidas", "Roadster"]),
        ("Track Pants", ["Puma", "Adidas", "HRX"]),
        ("Kurta", ["Manyavar", "Biba", "FabIndia"]),
    ],

    "Home & Kitchen": [
        ("Mixer Grinder", ["Philips", "Bajaj", "Prestige", "Sujata"]),
        ("Air Fryer", ["Philips", "Prestige", "Havells"]),
        ("Electric Kettle", ["Prestige", "Pigeon", "Philips"]),
        ("Cookware Set", ["Prestige", "Hawkins", "Wonderchef"]),
        ("Water Bottle", ["Milton", "Cello", "Borosil"]),
        ("Storage Container", ["Milton", "Cello", "Signoraware"]),
        ("Coffee Maker", ["Philips", "Morphy Richards", "Agaro"]),
        ("Induction Cooktop", ["Philips", "Prestige", "Bajaj"]),
    ],

    "Beauty": [
        ("Face Wash", ["Minimalist", "Mamaearth", "Cetaphil", "Neutrogena"]),
        ("Moisturizer", ["Cetaphil", "Minimalist", "Nivea", "Plum"]),
        ("Sunscreen", ["Minimalist", "Aqualogica", "Neutrogena", "Lakme"]),
        ("Shampoo", ["Dove", "Loreal", "Tresemme", "Head & Shoulders"]),
        ("Conditioner", ["Dove", "Loreal", "Tresemme"]),
        ("Lip Balm", ["Nivea", "Maybelline", "Vaseline"]),
        ("Serum", ["Minimalist", "The Ordinary", "Plum"]),
        ("Body Lotion", ["Nivea", "Vaseline", "Dove"]),
    ],

    "Sports": [
        ("Running Shoes", ["Nike", "Adidas", "Puma", "Asics"]),
        ("Yoga Mat", ["Boldfit", "Strauss", "Amazon Basics"]),
        ("Dumbbells", ["Kobo", "Boldfit", "Strauss"]),
        ("Cricket Bat", ["SG", "SS", "MRF", "Gray Nicolls"]),
        ("Football", ["Nivia", "Nike", "Adidas", "Puma"]),
        ("Badminton Racket", ["Yonex", "Li-Ning", "Victor"]),
        ("Resistance Bands", ["Boldfit", "Strauss", "Kobo"]),
        ("Gym Gloves", ["Boldfit", "Nike", "Adidas"]),
    ]
}
# ==========================================
# GENERATE 100 PRODUCTS
# ==========================================

products_per_category = {
    "Electronics": 25,
    "Fashion": 20,
    "Home & Kitchen": 20,
    "Beauty": 15,
    "Sports": 20
}

products_data = []
product_number = 1

for category_name, target_count in products_per_category.items():

    category_id = categories.loc[
        categories["category_name"] == category_name,
        "category_id"
    ].iloc[0]

    templates = product_templates[category_name]

    # Create enough product combinations
    combinations = []

    for product_type, brands in templates:
        for brand in brands:
            combinations.append((product_type, brand))

    # Shuffle combinations for variety
    random.shuffle(combinations)

    for i in range(target_count):

        product_type, brand = combinations[i]

        product_id = f"P{product_number:03d}"

        # ==========================================
        # REALISTIC PRODUCT PRICE RANGES
        # ==========================================

        price_ranges = {
            "Smartphone": (8000, 120000),
            "Laptop": (30000, 150000),
            "Headphones": (800, 25000),
            "Smartwatch": (1500, 30000),
            "Tablet": (10000, 60000),
            "Bluetooth Speaker": (800, 20000),
            "Power Bank": (700, 5000),
            "Wireless Mouse": (500, 5000),

            "T-Shirt": (400, 3000),
            "Jeans": (1000, 5000),
            "Hoodie": (1000, 5000),
            "Sneakers": (1500, 15000),
            "Shirt": (700, 4000),
            "Jacket": (1500, 10000),
            "Track Pants": (800, 4000),
            "Kurta": (800, 5000),

            "Mixer Grinder": (2000, 8000),
            "Air Fryer": (4000, 15000),
            "Electric Kettle": (1000, 5000),
            "Cookware Set": (1500, 10000),
            "Water Bottle": (300, 2500),
            "Storage Container": (300, 3000),
            "Coffee Maker": (3000, 15000),
            "Induction Cooktop": (1500, 6000),

            "Face Wash": (150, 1000),
            "Moisturizer": (200, 1500),
            "Sunscreen": (250, 1500),
            "Shampoo": (200, 1000),
            "Conditioner": (200, 1000),
            "Lip Balm": (100, 600),
            "Serum": (300, 2000),
            "Body Lotion": (200, 1200),

            "Running Shoes": (1500, 15000),
            "Yoga Mat": (500, 3000),
            "Dumbbells": (500, 5000),
            "Cricket Bat": (1500, 15000),
            "Football": (500, 4000),
            "Badminton Racket": (800, 10000),
            "Resistance Bands": (300, 2000),
            "Gym Gloves": (300, 2000)
        }

        # Get realistic selling-price range
        min_price, max_price = price_ranges[product_type]

        selling_price = round(
            random.uniform(min_price, max_price),
            2
        )

        # Cost price is lower than selling price
        cost_price = round(
            selling_price * random.uniform(0.60, 0.85),
            2
        )

        products_data.append([
            product_id,
            f"{brand} {product_type}",
            category_id,
            brand,
            cost_price,
            selling_price
        ])

        product_number += 1


products = pd.DataFrame(
    products_data,
    columns=[
        "product_id",
        "product_name",
        "category_id",
        "brand",
        "cost_price",
        "selling_price"
    ]
)


# ==========================================
# DISPLAY PRODUCT SUMMARY
# ==========================================

print("\n--- Category Summary ---")
print(categories)

print("\n--- Product Sample ---")
print(products.head(10))

print("\nTotal Products:", len(products))

print("\n--- Products by Category ---")

product_category_summary = (
    products
    .merge(categories, on="category_id")
    .groupby("category_name")
    .size()
)

print(product_category_summary)
# ==========================================
# CUSTOMER MASTER DATA
# ==========================================

male_names = [
    "Aarav", "Arjun", "Aditya", "Rahul", "Rohit",
    "Vikram", "Kiran", "Sandeep", "Varun", "Nikhil",
    "Akhil", "Pranav", "Karthik", "Manoj", "Rakesh"
]

female_names = [
    "Priya", "Ananya", "Sneha", "Meera", "Pooja",
    "Kavya", "Divya", "Isha", "Neha", "Anjali",
    "Aishwarya", "Swathi", "Harini", "Keerthi", "Nandini"
]

cities_data = [
    ("Hyderabad", "Telangana"),
    ("Bangalore", "Karnataka"),
    ("Chennai", "Tamil Nadu"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Visakhapatnam", "Andhra Pradesh"),
    ("Vijayawada", "Andhra Pradesh"),
    ("Kochi", "Kerala"),
    ("Kolkata", "West Bengal"),
    ("Ahmedabad", "Gujarat"),
    ("Jaipur", "Rajasthan"),
    ("Lucknow", "Uttar Pradesh"),
    ("Coimbatore", "Tamil Nadu"),
    ("Gurugram", "Haryana")
]


customers_data = []

for i in range(1, NUM_CUSTOMERS + 1):

    customer_id = f"C{i:04d}"

    # Select gender first
    gender = random.choice([
        "Male",
        "Female"
    ])

    # Select a name matching the gender
    if gender == "Male":
        name = random.choice(male_names)
    else:
        name = random.choice(female_names)

    age = random.randint(18, 60)

    city, state = random.choice(cities_data)

    signup_range = (
        END_DATE - START_DATE
    ).days

    signup_date = START_DATE + timedelta(
        days=random.randint(
            0,
            (END_DATE - START_DATE).days
        )
    )

    customers_data.append([
        customer_id,
        name,
        gender,
        age,
        city,
        state,
        signup_date.date()
    ])


customers = pd.DataFrame(
    customers_data,
    columns=[
        "customer_id",
        "customer_name",
        "gender",
        "age",
        "city",
        "state",
        "signup_date"
    ]
)
# Prevent customers from signing up on the final dataset date.
# This guarantees every customer can have an order after signup.
customers["signup_date"] = pd.to_datetime(customers["signup_date"])

customers.loc[
    customers["signup_date"] == END_DATE,
    "signup_date"
] = END_DATE - timedelta(days=1)
customers["signup_date"] = customers["signup_date"].dt.date
print("\nMaximum customer signup date:")
print(customers["signup_date"].max())

print("\nCustomers signed up on 2025-12-31:")
print(
    (pd.to_datetime(customers["signup_date"]) == END_DATE).sum()
)
# ==========================================
# CUSTOMER SUMMARY
# ==========================================

print("\n--- Customer Sample ---")
print(customers.head(10))

print("\nTotal Customers:", len(customers))

print("\n--- Customers by City ---")
print(
    customers["city"]
    .value_counts()
)

print("\n--- Gender Distribution ---")
print(
    customers["gender"]
    .value_counts()
)

# ==========================================
# ORDER DATA
# ==========================================

payment_methods = [
    "UPI",
    "Card",
    "Cash",
    "Net Banking"
]

order_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Delivered",
    "Cancelled"
]


orders_data = []

customer_ids = customers["customer_id"].tolist()

# ==========================================
# REALISTIC CUSTOMER ORDER BEHAVIOR
# ==========================================

# Assign each customer an activity weight.
# Higher weight = more likely to place an order.

# ==========================================
# REALISTIC CUSTOMER ACTIVITY LEVELS
# ==========================================

# Generate customer activity scores
customer_activity = np.random.gamma(
    shape=2.5,
    scale=1.0,
    size=len(customer_ids)
)

# Prevent extreme customer activity
customer_activity = np.clip(
    customer_activity,
    0.5,
    5.0
)

# Convert activity scores into probabilities
customer_weights = (
    customer_activity
    / customer_activity.sum()
)


for i in range(1, NUM_ORDERS + 1):

    order_id = f"O{i:05d}"

    # Select customer based on activity level
    customer_id = np.random.choice(
        customer_ids,
        p=customer_weights
    )

    # Get customer's signup date
    signup_date = customers.loc[
        customers["customer_id"] == customer_id,
        "signup_date"
    ].iloc[0]

    signup_date = pd.to_datetime(signup_date)

    # Order must happen after signup
    # ==========================================
    # REALISTIC ORDER DATE WITH SEASONALITY
    # ==========================================
    available_days = (END_DATE - signup_date).days

    if available_days > 0:
        candidate_dates = pd.date_range(
            start=signup_date + timedelta(days=1),
            end=END_DATE,
            freq="D"
        )

        date_weights = []

        for date in candidate_dates:
            month = date.month

            if month in [10, 11]:
                weight = 2.0
            elif month in [6, 7]:
                weight = 1.2
            elif month == 12:
                weight = 1.5
            else:
                weight = 1.0

            date_weights.append(weight)

        date_weights = np.array(date_weights)
        date_weights = date_weights / date_weights.sum()

        order_date = np.random.choice(
            candidate_dates,
            p=date_weights
        )

    else:
        # Customer signed up on the final day of the dataset,
        # so no valid order date exists within 2025.
        # Move the signup date earlier by one day for this edge case.
        signup_date = END_DATE - timedelta(days=1)
        order_date = END_DATE



    # Generate order status
    order_status = random.choice(order_statuses)

    # Generate payment method
    payment_method = random.choice(
        payment_methods
    )

    orders_data.append([
        order_id,
        customer_id,
        pd.Timestamp(order_date).date(),
        order_status,
        payment_method
    ])


orders = pd.DataFrame(
    orders_data,
    columns=[
        "order_id",
        "customer_id",
        "order_date",
        "order_status",
        "payment_method"
    ]
)


# ==========================================
# ORDER SUMMARY
# ==========================================

print("\n--- Order Sample ---")
print(orders.head(10))

print("\nTotal Orders:", len(orders))

print("\n--- Order Status Distribution ---")
print(
    orders["order_status"]
    .value_counts()
)

print("\n--- Payment Method Distribution ---")
print(
    orders["payment_method"]
    .value_counts()
)

print("\n--- Orders per Customer ---")
print(
    orders["customer_id"]
    .value_counts()
    .describe()
)
# ==========================================
# ORDER ITEMS
# ==========================================

order_items_data = []

order_item_number = 1

product_ids = products["product_id"].tolist()

product_price_map = products.set_index(
    "product_id"
)["selling_price"].to_dict()


for _, order in orders.iterrows():

    order_id = order["order_id"]

    # Each order contains 1 to 4 products
    num_items = random.randint(1, 4)

    # Select unique products for this order
    selected_products = random.sample(
        product_ids,
        num_items
    )

    for product_id in selected_products:

        quantity = random.randint(1, 3)

        selling_price = product_price_map[
            product_id
        ]

        # Discount between 0% and 20%
        discount = random.choice([
            0,
            5,
            10,
            15,
            20
        ])

        order_items_data.append([
            order_item_number,
            order_id,
            product_id,
            quantity,
            selling_price,
            discount
        ])

        order_item_number += 1


order_items = pd.DataFrame(
    order_items_data,
    columns=[
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "selling_price",
        "discount"
    ]
)


# ==========================================
# ORDER ITEM SUMMARY
# ==========================================

print("\n--- Order Items Sample ---")
print(order_items.head(10))

print("\nTotal Order Items:", len(order_items))

print("\n--- Quantity Statistics ---")
print(
    order_items["quantity"]
    .describe()
)

print("\n--- Discount Distribution ---")
print(
    order_items["discount"]
    .value_counts()
    .sort_index()
)

print("\n--- Items per Order ---")

items_per_order = (
    order_items
    .groupby("order_id")
    .size()
)

print(
    items_per_order.describe()
)
# ==========================================
# PAYMENT DATA
# ==========================================

payments_data = []

payment_number = 1


# Calculate order-level amount from order items
order_totals = (
    order_items
    .assign(
        net_amount=lambda df:
        df["quantity"]
        * df["selling_price"]
        * (1 - df["discount"] / 100)
    )
    .groupby("order_id")["net_amount"]
    .sum()
    .to_dict()
)


for _, order in orders.iterrows():

    order_id = order["order_id"]

    payment_id = f"PAY{payment_number:05d}"

    payment_date = order["order_date"]

    payment_method = order["payment_method"]

    amount = round(
        order_totals[order_id],
        2
    )

    # Payment status depends on order status
    if order["order_status"] == "Delivered":

        payment_status = "Successful"

    else:

        payment_status = random.choice([
            "Failed",
            "Refunded"
        ])

    # Cancelled orders do not contribute revenue
    if order["order_status"] == "Cancelled":

        amount = 0

    payments_data.append([
        payment_id,
        order_id,
        payment_date,
        payment_method,
        amount,
        payment_status
    ])

    payment_number += 1


payments = pd.DataFrame(
    payments_data,
    columns=[
        "payment_id",
        "order_id",
        "payment_date",
        "payment_method",
        "amount",
        "payment_status"
    ]
)


# ==========================================
# PAYMENT SUMMARY
# ==========================================

print("\n--- Payment Sample ---")
print(payments.head(10))

print("\nTotal Payments:", len(payments))

print("\n--- Payment Status Distribution ---")
print(
    payments["payment_status"]
    .value_counts()
)

print("\n--- Payment Method Distribution ---")
print(
    payments["payment_method"]
    .value_counts()
)

print("\n--- Successful Payment Amount ---")
print(
    payments.loc[
        payments["payment_status"] == "Successful",
        "amount"
    ].describe()
)
# ==========================================
# DELIVERY DATA
# ==========================================

deliveries_data = []

delivery_number = 1


for _, order in orders.iterrows():

    # Cancelled orders are not shipped
    if order["order_status"] == "Cancelled":
        continue

    delivery_id = f"D{delivery_number:05d}"

    order_id = order["order_id"]

    order_date = pd.to_datetime(
        order["order_date"]
    )

    # Shipment happens 1–3 days after order
    shipped_date = order_date + timedelta(
        days=random.randint(1, 3)
    )

    # Most orders are delivered
    delivery_status = random.choices(
        ["Delivered", "In Transit"],
        weights=[90, 10],
        k=1
    )[0]

    if delivery_status == "Delivered":

        delivery_days = random.randint(2, 7)

        delivered_date = (
            shipped_date
            + timedelta(days=delivery_days)
        )

    else:

        delivered_date = None

    deliveries_data.append([
        delivery_id,
        order_id,
        shipped_date.date(),
        (
            delivered_date.date()
            if delivered_date
            else None
        ),
        delivery_status
    ])

    delivery_number += 1


deliveries = pd.DataFrame(
    deliveries_data,
    columns=[
        "delivery_id",
        "order_id",
        "shipped_date",
        "delivered_date",
        "delivery_status"
    ]
)


# ==========================================
# DELIVERY SUMMARY
# ==========================================

print("\n--- Delivery Sample ---")
print(deliveries.head(10))

print("\nTotal Deliveries:", len(deliveries))

print("\n--- Delivery Status Distribution ---")
print(
    deliveries["delivery_status"]
    .value_counts()
)

# Calculate delivery duration
deliveries["shipped_date"] = pd.to_datetime(
    deliveries["shipped_date"]
)

deliveries["delivered_date"] = pd.to_datetime(
    deliveries["delivered_date"]
)

deliveries["delivery_days"] = (
    deliveries["delivered_date"]
    - deliveries["shipped_date"]
).dt.days

print("\n--- Delivery Days Statistics ---")
print(
    deliveries["delivery_days"]
    .describe()
)
# ==========================================
# REVIEWS
# ==========================================

reviews_data = []
review_number = 1

# Only orders that are actually delivered
delivered_orders = orders[
    orders["order_status"] == "Delivered"
].copy()

delivered_orders["order_date"] = pd.to_datetime(
    delivered_orders["order_date"]
)

# Only deliveries with actual Delivered status
delivered_delivery_map = (
    deliveries[
        deliveries["delivery_status"] == "Delivered"
    ]
    .set_index("order_id")["delivered_date"]
    .to_dict()
)

# Products purchased in each order
order_products_map = (
    order_items
    .groupby("order_id")["product_id"]
    .apply(list)
    .to_dict()
)

for _, order in delivered_orders.iterrows():

    order_id = order["order_id"]

    # Review only if the order was actually delivered
    if order_id not in delivered_delivery_map:
        continue

    # Not every delivered order receives a review
    if random.random() > 0.45:
        continue

    customer_id = order["customer_id"]

    available_products = order_products_map[order_id]

    product_id = random.choice(
        available_products
    )

    # Realistic rating distribution
    rating = random.choices(
        [1, 2, 3, 4, 5],
        weights=[3, 7, 15, 30, 45],
        k=1
    )[0]

    delivered_date = pd.to_datetime(
        delivered_delivery_map[order_id]
    )

    # Review submitted 1–14 days after delivery
    review_date = (
        delivered_date
        + timedelta(days=random.randint(1, 14))
    )

    review_id = f"R{review_number:05d}"

    reviews_data.append([
        review_id,
        order_id,
        customer_id,
        product_id,
        rating,
        review_date.date()
    ])

    review_number += 1

reviews = pd.DataFrame(
    reviews_data,
    columns=[
        "review_id",
        "order_id",
        "customer_id",
        "product_id",
        "rating",
        "review_date"
    ]
)
# ==========================================
# REVIEW SUMMARY
# ==========================================

print("\n--- Review Sample ---")
print(reviews.head(10))

print("\nTotal Reviews:", len(reviews))

print("\n--- Rating Distribution ---")
print(
    reviews["rating"]
    .value_counts()
    .sort_index()
)

print("\n--- Average Rating ---")
print(
    reviews["rating"].mean()
)

print("\n--- Reviews per Product ---")
print(
    reviews
    .groupby("product_id")
    .size()
    .describe()
)
# ============================================================
# EXPORT DATA TO CSV
# ============================================================

import os

RAW_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "raw"
)

os.makedirs(RAW_DATA_PATH, exist_ok=True)

customers.to_csv(
    os.path.join(RAW_DATA_PATH, "customers.csv"),
    index=False
)

categories.to_csv(
    os.path.join(RAW_DATA_PATH, "categories.csv"),
    index=False
)

products.to_csv(
    os.path.join(RAW_DATA_PATH, "products.csv"),
    index=False
)

orders.to_csv(
    os.path.join(RAW_DATA_PATH, "orders.csv"),
    index=False
)

order_items.to_csv(
    os.path.join(RAW_DATA_PATH, "order_items.csv"),
    index=False
)

payments.to_csv(
    os.path.join(RAW_DATA_PATH, "payments.csv"),
    index=False
)

deliveries.to_csv(
    os.path.join(RAW_DATA_PATH, "deliveries.csv"),
    index=False
)

reviews.to_csv(
    os.path.join(RAW_DATA_PATH, "reviews.csv"),
    index=False
)

print("\n" + "=" * 60)
print("CSV EXPORT COMPLETED")
print("=" * 60)
print(f"Files saved to: {RAW_DATA_PATH}")

print("\nExported files:")
print("- customers.csv")
print("- categories.csv")
print("- products.csv")
print("- orders.csv")
print("- order_items.csv")
print("- payments.csv")
print("- deliveries.csv")
print("- reviews.csv")