import pandas as pd

# Expected processing time 
EXPECTED_PROCESSING_TIME = 3


def load_data(file):

    df = pd.read_csv(file)

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])

    # Actual order processing time
    df["processing_time"] = (df["ship_date"] - df["order_date"]).dt.days

    # Shipping delay compared to expected processing time
    df["delay"] = df["processing_time"] - EXPECTED_PROCESSING_TIME

    return df


def generate_summary(df):

    avg_delay_warehouse = df.groupby("warehouse")["delay"].mean()
    avg_delay_product = df.groupby("product")["delay"].mean()

    avg_processing_warehouse = df.groupby("warehouse")["processing_time"].mean()
    avg_processing_product = df.groupby("product")["processing_time"].mean()

    fastest_product = avg_processing_product.idxmin()
    slowest_product = avg_processing_product.idxmax()

    worst_warehouse = avg_delay_warehouse.idxmax()

    delayed_orders = df[df["delay"] > 0]

    avg_processing_time = df["processing_time"].mean()

    summary = f"""
Average delay per warehouse:
{avg_delay_warehouse.to_dict()}

Average delay per product:
{avg_delay_product.to_dict()}

Average processing time per warehouse:
{avg_processing_warehouse.to_dict()}

Average processing time per product:
{avg_processing_product.to_dict()}

Warehouse with highest delay:
{worst_warehouse}

Product with highest processing time:
{slowest_product}

Fastest processing product:
{fastest_product}

Average order processing time:
{avg_processing_time:.2f} days

Orders delayed beyond expected processing time:
{len(delayed_orders)}
"""

    return summary


def calculate_health_score(df):

    avg_delay = df["delay"].mean()

    score = max(0, 100 - (avg_delay * 15))

    return round(score, 2)