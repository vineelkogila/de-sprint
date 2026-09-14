import csv

file_path = "data/orders.csv"

valid_records = []
invalid_records = []

with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            order_id = int(row["order_id"])
            customer_id = row["customer_id"]
            product = row["product"]
            quantity = int(row["quantity"])
            unit_price = float(row["unit_price"])
            order_date = row["order_date"]

            if order_id <= 0:
                raise ValueError("Order ID must be positive")

            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            if unit_price <= 0:
                raise ValueError("Unit price must be positive")

            valid_records.append({
                "order_id": order_id,
                "customer_id": customer_id,
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "order_date": order_date
            })

        except ValueError as error:
            invalid_records.append({
                "row": row,
                "error": str(error)
            })


print(f"Valid records: {len(valid_records)}")
print(f"Invalid records: {len(invalid_records)}")

print("\nInvalid records:")

for record in invalid_records:
    print(record)