import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Define the path to your CSV file
csv_file_path = "finance_data.csv"

# Check if the CSV file exists, if not, create an empty one with the appropriate columns
if not os.path.exists(csv_file_path):
    df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])
    df.to_csv(csv_file_path, index=False)
    df["Date"] = pd.to_datetime(df["Date"]) 




df = pd.read_csv(csv_file_path)

# Define categories
default_expense_categories = ["Food", "Clothings", "Fruits", "Transportation", "Home"]
default_income_categories = ["Coupons", "Salary"]

# Create form for adding new entries
st.title("Personal Finance Dashboard")

st.header("Add New Entry")
entry_type = st.selectbox("Select type:", ["Income", "Expense"])
categories = default_income_categories if entry_type == "Income" else default_expense_categories
category = st.selectbox("Select category:", categories + ["Add New Category"])
amount = st.number_input("Enter amount:", min_value=0.0, step=10.0)
date = st.date_input("Select date:", value=datetime.now().date())

if category == "Add New Category":
    new_category = st.text_input("Enter new category:")
    if st.button("Add Category"):
        if new_category:
            categories.append(new_category)
            st.success(f"New category '{new_category}' added!")
        else:
            st.error("Please enter a category name.")
else:
    if st.button("Add Entry"):
        if amount > 0:
            new_entry = pd.DataFrame({
                "Date": [date],
                "Type": [entry_type],
                "Category": [category],
                "Amount": [amount]
            })
            new_entry.to_csv(csv_file_path, mode='a', header=False, index=False)
            st.success(f"{entry_type} of ${amount:.2f} for {category} added successfully!")
        else:
            st.error("Please enter a valid amount.")

# Display data
st.subheader("Dashboard")
filter_month = st.selectbox("Select Month:", sorted(df["Date"].str[:7].unique(), reverse=True))
filtered_df = df[df["Date"].str.startswith(filter_month)]

# Summary
total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
total_expenses = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
remaining_balance = total_income - total_expenses

st.write(f"Total Income: ${total_income:.2f}")
st.write(f"Total Expenses: ${total_expenses:.2f}")
st.write(f"Remaining Balance: ${remaining_balance:.2f}")

# Visualization
st.subheader("Expense and Income Distribution")
expense_data = filtered_df[filtered_df["Type"] == "Expense"]
income_data = filtered_df[filtered_df["Type"] == "Income"]

if not expense_data.empty:
    st.subheader("Expense Distribution by Category")
    expense_summary = expense_data.groupby("Category").sum().reset_index()
    st.bar_chart(expense_summary.set_index("Category")["Amount"])

if not income_data.empty:
    st.subheader("Income Distribution by Category")
    income_summary = income_data.groupby("Category").sum().reset_index()
    st.bar_chart(income_summary.set_index("Category")["Amount"])

# Option to view all entries
if st.checkbox("View All Entries"):
    st.write(df)











