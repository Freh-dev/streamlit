import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# Title and Intro
st.title("Data App Assignment, on July 14th")
st.write("### Input Data and Examples")

# Load data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)


# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)
# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# ================================
# Your Additions Start Here
# ================================
st.write("## Your Additions")
st.write("### (1) Dropdown for Category")
category = st.selectbox("Choose a Category:", df["Category"].unique())

st.write("### (2) Multi-select for Sub-Category in selected Category")
subcategories = df[df["Category"] == category]["Sub-Category"].unique()
selected_subcats = st.multiselect("Choose Sub-Categories:", subcategories)

# Filtered dataframe
filtered_df = df[(df["Category"] == category) & (df["Sub-Category"].isin(selected_subcats))]

if not filtered_df.empty:
    st.write("### (3) Line chart of sales for selected Sub-Categories")
    sales_by_month_filtered = filtered_df[["Sales"]].groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month_filtered)

    # Calculate metrics
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    delta_margin = profit_margin - overall_profit_margin

    st.write("### (4) & (5) Key Metrics with Delta")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Profit Margin", f"{profit_margin:.2f}%", delta=f"{delta_margin:.2f}%")
else:
    st.warning("No data to display for the selected sub-categories.")