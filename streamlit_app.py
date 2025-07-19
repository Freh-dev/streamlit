import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# Title and Intro
st.title("Data App Assignment – Superstore Sales Analysis")
st.write("### Input Data and Initial Visualizations")

# Load data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Initial bar chart (raw)
st.write("#### Raw Sales by Category (Unaggregated)")
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart
st.write("#### Aggregated Sales by Category")
aggregated = df.groupby("Category", as_index=False).sum()
st.dataframe(aggregated)
st.bar_chart(aggregated, x="Category", y="Sales", color="#04f")

# Convert date and group by month
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

# Monthly sales trend
sales_by_month = df[["Sales"]].groupby(pd.Grouper(freq='M')).sum()
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

# 1. Dropdown for Category
category = st.selectbox("Choose a Category:", df["Category"].unique())

# 2. Multi-select for Sub-Category in selected Category
subcategories = df[df["Category"] == category]["Sub-Category"].unique()
selected_subcats = st.multiselect("Choose Sub-Categories:", subcategories)

# Filtered data
filtered_df = df[(df["Category"] == category) & (df["Sub-Category"].isin(selected_subcats))]

if not filtered_df.empty:
    # 3. Line chart of sales for selected Sub-Categories
    st.write(f"### Monthly Sales Trend for Selected Sub-Categories in {category}")
    sales_by_month_filtered = filtered_df[["Sales"]].groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month_filtered)

    # 4. Key Metrics
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

    # 5. Delta from overall profit margin
    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    delta_margin = profit_margin - overall_profit_margin

    st.write("### Key Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin", f"{profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")

else:
    st.warning("No sales data found for the selected sub-categories. Try selecting different options.")
# ================================
# Continue with the Original Monthly Sales Logic
# ================================
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

sales_by_month = df[["Sales"]].groupby(pd.Grouper(freq='M')).sum()
st.write("#### Monthly Sales Trend (All Categories)")
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")
