import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and Intro
st.title("Data App Assignment – Superstore Sales Analysis")
st.write("### Input Data and Initial Visualizations")

# Load and clean data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date", "Ship_Date"])
df.columns = df.columns.str.strip()

# Display raw data
st.dataframe(df)

# Raw bar chart
st.write("#### Raw Sales by Category (Unaggregated)")
st.bar_chart(df, x="Category", y="Sales")

# Aggregated sales by Category
st.write("#### Aggregated Sales by Category")
aggregated = df.groupby("Category", as_index=False).sum(numeric_only=True)
st.dataframe(aggregated)
st.bar_chart(aggregated, x="Category", y="Sales", color="#04f")

# Monthly sales trend (all data)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)
sales_by_month = df[["Sales"]].groupby(pd.Grouper(freq="M")).sum()
st.write("#### Monthly Sales Trend")
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

# ================================
# Interactive Dashboard Section
# ================================
st.write("## Interactive Dashboard")
st.write("""
Use the dropdowns below to explore specific product Categories and Sub-Categories.
View monthly sales trends and key performance metrics for your selections.
""")

# Dropdown: Category
category = st.selectbox("Choose a Category:", df["Category"].unique())

# Multi-select: Sub-Category
subcategories = df[df["Category"] == category]["Sub_Category"].unique()
selected_subcats = st.multiselect("Choose Sub-Categories:", subcategories)

# Filtered data
filtered_df = df[(df["Category"] == category) & (df["Sub_Category"].isin(selected_subcats))]

if not filtered_df.empty:
    # Monthly trend for selected sub-categories
    st.write(f"### Monthly Sales Trend for Selected Sub-Categories in {category}")
    sales_by_month_filtered = filtered_df[["Sales"]].groupby(pd.Grouper(freq="M")).sum()
    st.line_chart(sales_by_month_filtered)

    # Key metrics
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    delta_margin = profit_margin - overall_profit_margin

    st.write("### Key Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin", f"{profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")

else:
    st.warning("No sales data found for the selected sub-categories. Try selecting different options.")

# Optional: Reset and replot full monthly sales trend
df = df.reset_index()
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)
sales_by_month = df[["Sales"]].groupby(pd.Grouper(freq="M")).sum()
st.write("#### Monthly Sales Trend (All Categories)")
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")
