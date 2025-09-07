import streamlit as st
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000"

def add_update_tab():
    # Date input
    selected_date = st.date_input(
        "Enter Date:",
        datetime(2024, 8, 1),
        label_visibility="collapsed"
    )
    date_str = selected_date.strftime('%Y-%m-%d')

    # Fetch existing expenses with proper error handling
    try:
        response = requests.get(f"{API_URL}/expenses/{date_str}", timeout=5)
        response.raise_for_status()  # raises HTTPError for bad status
        # Only parse JSON if content exists
        if response.content.strip():
            existing_expenses = response.json()
        else:
            existing_expenses = []
            st.warning("No expenses found for this date.")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Expense form
    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Categories")
        with col3:
            st.subheader("Notes")

        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    label="Amount:",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes",
                    value=notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input,
            })

        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            try:
                post_response = requests.post(
                    f"{API_URL}/expenses/{date_str}",
                    json=filtered_expenses,
                    timeout=5
                )
                post_response.raise_for_status()
                st.success("Expenses updated successfully")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error while posting data: {e}")
