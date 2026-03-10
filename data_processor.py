import pandas as pd


def load_data(file):

    df = pd.read_csv(file)

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])

    df["delay"] = (df["ship_date"] - df["order_date"]).dt.days

    return df


def generate_summary(df):

    avg_delay_warehouse = df.groupby("warehouse")["delay"].mean()
    avg_delay_product = df.groupby("product")["delay"].mean()

    fastest_product = avg_delay_product.idxmin()
    slowest_product = avg_delay_product.idxmax()

    worst_warehouse = avg_delay_warehouse.idxmax()

    delayed_orders = df[df["delay"] > 3]

    summary = f"""
Average delay per warehouse:
{avg_delay_warehouse.to_dict()}

Average delay per product:
{avg_delay_product.to_dict()}

Warehouse with highest delay:
{worst_warehouse}

Product with highest delay:
{slowest_product}

Fastest shipping product:
{fastest_product}

Orders delayed more than 3 days:
{len(delayed_orders)}
"""

    return summary


def calculate_health_score(df):

    avg_delay = df["delay"].mean()

    score = max(0, 100 - (avg_delay * 15))

    return round(score, 2)