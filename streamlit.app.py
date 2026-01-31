import streamlit as st
import pandas as pd

st.title("🏦 Bank Account Management System")

# Initialize session state
if "balance" not in st.session_state:
    st.session_state.balance = 0.0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

# ----------- ACCOUNT DETAILS -----------
st.subheader("👤 Account Details")

name = st.text_input("Customer Name")
account_type = st.selectbox("Account Type", ["Savings", "Current"])

# ----------- BALANCE DISPLAY -----------
st.subheader("💰 Current Balance")
st.info(f"₹ {st.session_state.balance:.2f}")

# ----------- TRANSACTION SECTION -----------
st.subheader("💳 Transactions")

amount = st.number_input("Enter Amount", min_value=0.0, step=100.0)

col1, col2 = st.columns(2)

# Deposit
with col1:
    if st.button("Deposit"):
        st.session_state.balance += amount
        st.session_state.transactions.append(
            {"Type": "Deposit", "Amount": amount}
        )
        st.success("Amount Deposited Successfully ✅")

# Withdraw
with col2:
    if st.button("Withdraw"):
        if amount <= st.session_state.balance:
            st.session_state.balance -= amount
            st.session_state.transactions.append(
                {"Type": "Withdraw", "Amount": amount}
            )
            st.success("Amount Withdrawn Successfully ✅")
        else:
            st.error("Insufficient Balance ❌")

# ----------- TRANSACTION HISTORY -----------
if st.session_state.transactions:
    st.subheader("📋 Transaction History")
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df)

    st.subheader("📊 Deposit vs Withdrawal Chart")
    chart_df = df.groupby("Type").sum()
    st.bar_chart(chart_df)
