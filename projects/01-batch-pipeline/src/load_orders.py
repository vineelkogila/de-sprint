import csv
import os
from decimal import Decimal

import psycopg
from dotenv import load_dotenv

load_dotenv()

#file_path = "data/orders.csv"
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent / "data" / "orders.csv"

valid_records = []
invalid_records = []

# 1. Extract
with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:

        # 2. Transform + Validate
        try:
            order_id = int(row["order_id"])
            customer_id = row["customer_id"]
            product = row["product"]
            quantity = int(row["quantity"])
            unit_price = Decimal(row["unit_price"])
            #unit_price = float(row["unit_price"])
            order_date = row["order_date"]

            if order_id <= 0:
                raise ValueError("Order ID must be positive")

            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            if unit_price <= 0:
                raise ValueError("Unit price must be positive")

            valid_records.append(
                (
                    order_id,
                    customer_id,
                    product,
                    quantity,
                    unit_price,
                    order_date
                )
            )

        except ValueError as error:
            invalid_records.append(
                {
                    "row": row,
                    "error": str(error)
                }
            )


# 3. Load
connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cursor = connection.cursor()

for record in valid_records:
    cursor.execute(
        """
        INSERT INTO orders
        (order_id, customer_id, product, quantity, unit_price, order_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
        """,
        record
    )

connection.commit()

cursor.close()
connection.close()


print(f"Valid records: {len(valid_records)}")
print(f"Invalid records: {len(invalid_records)}")

for record in invalid_records:
    print(record)