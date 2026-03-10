import pandas as pd
import random
from datetime import datetime, timedelta

# number of rows
num_rows = 1000

warehouses = ["W1","W2","W3","W4","W5","W6","W7","W8"]

products = [
    "Laptop","Phone","Tablet","Monitor","Keyboard","Mouse",
    "Printer","Camera","Speaker","Router","Headphones",
    "Smartwatch","SSD","GPU","Microphone"
]

start_date = datetime(2024,1,1)

data = []

for i in range(1, num_rows+1):

    warehouse = random.choice(warehouses)
    product = random.choice(products)

    order_date = start_date + timedelta(days=random.randint(0,120))

    delay_days = random.randint(1,7)

    ship_date = order_date + timedelta(days=delay_days)

    data.append([
        i,
        warehouse,
        product,
        order_date.date(),
        ship_date.date()
    ])

df = pd.DataFrame(
    data,
    columns=["order_id","warehouse","product","order_date","ship_date"]
)

df.to_csv("orders_large.csv", index=False)

print("Dataset generated: orders_large.csv")