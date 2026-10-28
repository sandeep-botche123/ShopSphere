import os
import pandas as pd
from src.Database import create_engine_connection


# ==========================================
# LOAD DELIVERIES CSV INTO MYSQL
# ==========================================

PROJECT_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CSV_PATH = os.path.join(
    PROJECT_PATH,
    "data",
    "raw",
    "deliveries.csv"
)


# Load CSV
deliveries = pd.read_csv(CSV_PATH)

print("CSV rows:", len(deliveries))

# Convert date columns
deliveries["shipped_date"] = pd.to_datetime(
    deliveries["shipped_date"]
)

deliveries["delivered_date"] = pd.to_datetime(
    deliveries["delivered_date"],
    errors="coerce"
)

# Remove calculated column.
# It is not part of the MySQL deliveries table.
if "delivery_days" in deliveries.columns:
    deliveries = deliveries.drop(columns=["delivery_days"])


# Create database connection
engine = create_engine_connection()


# Remove the incomplete deliveries currently in MySQL
with engine.begin() as connection:
    connection.exec_driver_sql(
        "DELETE FROM deliveries"
    )

print("Existing deliveries removed.")


# Insert complete CSV data
deliveries.to_sql(
    "deliveries",
    con=engine,
    if_exists="append",
    index=False
)

engine.dispose()

print("Deliveries successfully loaded!")
print("Rows loaded:", len(deliveries))