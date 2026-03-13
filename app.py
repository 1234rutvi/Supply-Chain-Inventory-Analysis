import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Supply Chain Analytics Dashboard", layout="wide")

st.title("📦 Supply Chain & Inventory Analytics Dashboard")

# Upload dataset
uploaded_file = st.sidebar.file_uploader("Upload Supply Chain CSV", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Sidebar Filters
    st.sidebar.header("Filters")

    product_filter = st.sidebar.multiselect(
        "Product Type",
        df["Product type"].unique(),
        default=df["Product type"].unique()
    )

    supplier_filter = st.sidebar.multiselect(
        "Supplier",
        df["Supplier name"].unique(),
        default=df["Supplier name"].unique()
    )

    carrier_filter = st.sidebar.multiselect(
        "Shipping Carrier",
        df["Shipping carriers"].unique(),
        default=df["Shipping carriers"].unique()
    )

    location_filter = st.sidebar.multiselect(
        "Location",
        df["Location"].unique(),
        default=df["Location"].unique()
    )

    # Apply Filters
    filtered_df = df[
        (df["Product type"].isin(product_filter)) &
        (df["Supplier name"].isin(supplier_filter)) &
        (df["Shipping carriers"].isin(carrier_filter)) &
        (df["Location"].isin(location_filter))
    ]

    filtered_df = filtered_df.copy()

    # KPI Cards
    total_revenue = filtered_df["Revenue generated"].sum()
    total_products_sold = filtered_df["Number of products sold"].sum()
    avg_stock = filtered_df["Stock levels"].mean()

    filtered_df["Stock Risk"] = filtered_df["Stock levels"] < filtered_df["Order quantities"]
    stock_risk_count = filtered_df["Stock Risk"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("📦 Products Sold", int(total_products_sold))
    col3.metric("📊 Avg Stock Level", int(avg_stock))
    col4.metric("⚠ Stock Risk Products", int(stock_risk_count))

    st.markdown("---")

    # Top Selling Products
    st.subheader("Top Selling Products")

    top_products = (
        filtered_df.groupby("Product type")["Number of products sold"]
        .sum()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots()
    top_products.plot(kind="bar", ax=ax1)

    plt.xlabel("Product Type")
    plt.ylabel("Products Sold")

    st.pyplot(fig1)

    # Revenue by Product
    st.subheader("Revenue Distribution")

    revenue = filtered_df.groupby("Product type")["Revenue generated"].sum()

    fig2, ax2 = plt.subplots()
    revenue.plot(kind="pie", autopct="%1.1f%%", ax=ax2)

    st.pyplot(fig2)

    # Supplier Lead Time
    st.subheader("Supplier Lead Time Analysis")

    supplier_perf = filtered_df.groupby("Supplier name")["Lead times"].mean()

    fig3, ax3 = plt.subplots()
    supplier_perf.plot(kind="bar", ax=ax3)

    plt.ylabel("Average Lead Time")

    st.pyplot(fig3)

    # Shipping Carrier Performance
    st.subheader("Shipping Carrier Performance")

    shipping_perf = filtered_df.groupby("Shipping carriers")["Shipping times"].mean()

    fig4, ax4 = plt.subplots()
    shipping_perf.plot(kind="bar", ax=ax4)

    plt.ylabel("Shipping Time")

    st.pyplot(fig4)

    # Trend Analysis
    st.subheader("Revenue Trend Over Time")

    if "Order Date" in filtered_df.columns:

        filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])

        trend_data = filtered_df.groupby("Order Date")["Revenue generated"].sum()

        fig5, ax5 = plt.subplots()
        trend_data.plot(ax=ax5)

        plt.ylabel("Revenue")

        st.pyplot(fig5)

    # Stock Risk Table
    st.subheader("⚠ Products with Stock Risk")

    risk_products = filtered_df[filtered_df["Stock Risk"] == True]

    st.dataframe(risk_products[["Product type","Stock levels","Order quantities"]])

else:
    st.info("Upload a supply chain dataset to start analysis.")
