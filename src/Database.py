from sqlalchemy import create_engine, URL
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_config(key, default=None):
    value = os.getenv(key)

    if value:
        return value

    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default

# ==========================================
# CREATE MYSQL DATABASE CONNECTION
# ==========================================

def create_engine_connection():
    connection_url = URL.create(
        drivername="mysql+mysqlconnector",
        username=get_db_config("DB_USER"),
        password=get_db_config("DB_PASSWORD"),
        host=get_db_config("DB_HOST"),
        port=int(get_db_config("DB_PORT", 4000)),
        database=get_db_config("DB_NAME")
    )

    engine = create_engine(connection_url)
    return engine



# ==========================================
# LOAD DATA FROM MYSQL TABLE
# ==========================================

def load_data(table_name):

    engine = create_engine_connection()

    query = f"SELECT * FROM `{table_name}`"

    df = pd.read_sql(query, engine)

    engine.dispose()

    return df


# ==========================================
# TEST DATABASE CONNECTION
# ==========================================

if __name__ == "__main__":

    customers = load_data("customers")
    categories = load_data("categories")
    products = load_data("products")
    orders = load_data("orders")
    order_items = load_data("order_items")
    payments = load_data("payments")
    deliveries = load_data("deliveries")
    reviews = load_data("reviews")

    print("\n--- Table Shapes ---")

    print("Customers:", customers.shape)
    print("Categories:", categories.shape)
    print("Products:", products.shape)
    print("Orders:", orders.shape)
    print("Order Items:", order_items.shape)
    print("Payments:", payments.shape)
    print("Deliveries:", deliveries.shape)
    print("Reviews:", reviews.shape)