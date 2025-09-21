import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# --- Configuration ---
FILE_NAME = "data.json"

# --- Functions for Data Persistence ---

def load_data():
    """Loads transaction data from data.json or returns an empty list if the file doesn't exist."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
                # Ensure the loaded data is a list; otherwise, return an empty list.
                if isinstance(data, list):
                    return data
                else:
                    st.warning("Add some transactions to view. Initializing with an empty list.")
                    return []
        except json.JSONDecodeError:
            st.error("There was a problem reading your data file. It may be corrupted or in the wrong format.")
            return []
    return []

def save_data(data):
    """Saves transaction data to data.json."""
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# --- App Layout and Logic ---

def main():
    st.set_page_config(
        page_title="Financial Tracker",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject custom CSS to increase font size
    st.markdown("""
        <style>
        .stApp {
            font-size: 1.1rem;
        }
        .st-emotion-cache-1g8p9z { /* Target for metric labels */
            font-size: 1.2rem;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("💸 Financial Tracker")

    # Load data from the file
    if 'transactions' not in st.session_state:
        st.session_state.transactions = load_data()

    # Create a DataFrame from the transactions list, ensuring columns exist even if the list is empty
    df = pd.DataFrame(st.session_state.transactions, columns=["id", "title", "amount", "type", "date", "category", "notes"])
    
    # --- Sidebar for Adding Transactions ---
    with st.sidebar:
        st.header("Add a new transaction")
        with st.form("transaction_form", clear_on_submit=True):
            title = st.text_input("Title", placeholder="e.g., Paycheck, Groceries")
            amount = st.number_input("Amount ($)", min_value=0.01, format="%f")
            date = st.date_input("Date")
            type = st.selectbox("Type", ["income", "expense", "deduction"])
            category = st.text_input("Category", placeholder="e.g., Salary, Food, Rent")
            notes = st.text_area("Notes", placeholder="Add a short description...")

            submitted = st.form_submit_button("Add Transaction")
            if submitted:
                if title and amount:
                    new_transaction = {
                        "id": len(st.session_state.transactions) + 1,
                        "title": title,
                        "amount": float(amount),
                        "date": date.isoformat(),
                        "type": type,
                        "category": category,
                        "notes": notes
                    }
                    st.session_state.transactions.append(new_transaction)
                    save_data(st.session_state.transactions)
                    st.success("Transaction added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a title and amount.")

    # --- Main Dashboard ---
    st.header("Dashboard")

    # Check if data.json is empty and display a message
    if not st.session_state.transactions:
        st.info("Add a transaction to get started. Data file is currently empty.")
    else:
        # Get unique months from the data for filtering
        df['date'] = pd.to_datetime(df['date'])
        unique_months = df['date'].dt.strftime('%B %Y').unique().tolist()
        unique_months.sort(key=lambda x: pd.to_datetime(x, format='%B %Y'))
        all_months_option = 'All Months'
        unique_months.insert(0, all_months_option)

        # Filter section in the main dashboard
        st.subheader("Filter and Share")
        selected_month_label = st.selectbox(
            "Select a Month to Filter",
            options=unique_months,
            index=0
        )
        
        # Filter the DataFrame based on the selected month
        if selected_month_label != all_months_option:
            filtered_df = df[df['date'].dt.strftime('%B %Y') == selected_month_label]
        else:
            filtered_df = df

        st.markdown("---")
        
        # Calculate totals from the filtered data
        total_income = filtered_df[filtered_df['type'] == 'income']['amount'].sum() if not filtered_df.empty else 0
        total_expenses = filtered_df[filtered_df['type'] == 'expense']['amount'].sum() if not filtered_df.empty else 0
        total_deductions = filtered_df[filtered_df['type'] == 'deduction']['amount'].sum() if not filtered_df.empty else 0
        remaining_balance = total_income - total_expenses - total_deductions

        # Metrics section
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Income", value=f"${total_income:,.2f}")
        with col2:
            st.metric(label="Total Expenses", value=f"${total_expenses:,.2f}")
        with col3:
            st.metric(label="Total Deductions", value=f"${total_deductions:,.2f}")
        with col4:
            st.metric(label="Remaining Balance", value=f"${remaining_balance:,.2f}")

        st.markdown("---")

        # --- Charts Section ---
        st.header("Visualizations")
        if not filtered_df.empty:
            # Horizontal Bar Chart: Income vs (Expenses + Deductions)
            df_summary = pd.DataFrame({
                'Category': ['Income', 'Expenses + Deductions'],
                'Amount': [total_income, total_expenses + total_deductions]
            })
            fig1 = px.bar(
                df_summary,
                y='Category',
                x='Amount',
                orientation='h',
                title='Income vs. Expenses + Deductions',
                color='Category',
                color_discrete_map={'Income': '#10B981', 'Expenses + Deductions': '#EF4444'}
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Pie Chart: Expenses Breakdown
            expense_df = filtered_df[filtered_df['type'] == 'expense'].groupby('category')['amount'].sum().reset_index()
            fig2 = px.pie(
                expense_df,
                values='amount',
                names='category',
                title='Expenses Breakdown by Category'
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Vertical Bar Chart: Income vs Expenses vs Deductions
            df_totals = pd.DataFrame({
                'Category': ['Income', 'Expenses', 'Deductions'],
                'Amount': [total_income, total_expenses, total_deductions]
            })
            fig3 = px.bar(
                df_totals,
                x='Category',
                y='Amount',
                title='Income vs. Expenses vs. Deductions',
                color='Category',
                color_discrete_map={'Income': '#2563EB', 'Expenses': '#B91C1C', 'Deductions': '#F59E0B'}
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info(f"No transactions found for {selected_month_label}.")


        st.markdown("---")

        # --- Download All Transactions as CSV ---
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download {selected_month_label} Data",
            data=csv_data,
            file_name=f'financial_transactions_{selected_month_label}.csv',
            mime='text/csv',
        )
    
        st.markdown("---")
    
        # --- Separate Transaction Histories ---
        st.header("Income Transactions")
        income_df = filtered_df[filtered_df['type'] == 'income']
        if not income_df.empty:
            st.dataframe(income_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        else:
            st.info("No income transactions to display for this period.")

        st.header("Expense Transactions")
        expense_df = filtered_df[filtered_df['type'] == 'expense']
        if not expense_df.empty:
            st.dataframe(expense_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        else:
            st.info("No expense transactions to display for this period.")
    
        st.header("Deduction Transactions")
        deduction_df = filtered_df[filtered_df['type'] == 'deduction']
        if not deduction_df.empty:
            st.dataframe(deduction_df.drop(columns=['id']), use_container_width=True, hide_index=True)
        else:
            st.info("No deduction transactions to display for this period.")


if __name__ == "__main__":
    main()
