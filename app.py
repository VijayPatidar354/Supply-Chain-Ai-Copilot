import streamlit as st
import pandas as pd
import plotly.express as px

from data_processor import load_data, generate_summary
from ai_engine import ask_ai
from utils.prompt_template import build_prompt

st.set_page_config(page_title="Supply Chain AI Copilot", layout="wide")

st.title("📦 Supply Chain AI Copilot Dashboard")

uploaded_file = st.file_uploader("Upload Orders CSV", type=["csv"])

if uploaded_file:

    df = load_data(uploaded_file)

    # ---------------- Sidebar Filters ----------------
    st.sidebar.header("Filters")

    warehouses = st.sidebar.multiselect(
        "Select Warehouse",
        options=df["warehouse"].unique(),
        default=df["warehouse"].unique()
    )

    products = st.sidebar.multiselect(
        "Select Product",
        options=df["product"].unique(),
        default=df["product"].unique()
    )

    filtered_df = df[
        (df["warehouse"].isin(warehouses)) &
        (df["product"].isin(products))
    ]

    if filtered_df.empty:
        st.warning("⚠️ No data available. Please select at least one warehouse and product from the filters.")
        st.stop()

    # ---------------- KPI Metrics ----------------
    total_orders = len(filtered_df)
    avg_delay = filtered_df["delay"].mean()

    worst_warehouse = filtered_df.groupby("warehouse")["delay"].mean().idxmax()
    fastest_product = filtered_df.groupby("product")["delay"].mean().idxmin()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", total_orders)
    col2.metric("Average Delay", f"{avg_delay:.2f} days")
    col3.metric("Worst Warehouse", worst_warehouse)
    col4.metric("Fastest Product", fastest_product)

    st.divider()

    # ---------------- Charts ----------------

    col1, col2 = st.columns(2)

    # Chart 1: Delay by Warehouse
    warehouse_delay = filtered_df.groupby("warehouse")["delay"].mean().reset_index()

    fig1 = px.bar(
        warehouse_delay,
        x="warehouse",
        y="delay",
        title="Average Delay by Warehouse",
        color="warehouse"
    )

    col1.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Delay by Product
    product_delay = filtered_df.groupby("product")["delay"].mean().reset_index()

    fig2 = px.bar(
        product_delay,
        x="product",
        y="delay",
        title="Average Delay by Product",
        color="product"
    )

    col2.plotly_chart(fig2, use_container_width=True)

    # Chart 3: Delay Distribution
    fig3 = px.histogram(
        filtered_df,
        x="delay",
        nbins=10,
        title="Shipping Delay Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ---------------- Dataset Table ----------------
    st.subheader("📋 Dataset Preview")

    st.dataframe(filtered_df, use_container_width=True)

    st.divider()

    # ---------------- AI Copilot ----------------
    st.subheader("🤖 AI Supply Chain Copilot")

    summary = generate_summary(filtered_df)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.chat_input("Ask a question about the dataset")

    if question:

        prompt = build_prompt(summary, question)

        answer = ask_ai([
            {"role": "user", "content": prompt}
        ])

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer
        })

    for chat in st.session_state.chat_history:
        st.chat_message("user").write(chat["question"])
        st.chat_message("assistant").write(chat["answer"])