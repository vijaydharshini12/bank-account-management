import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🏦 Bank Account Management with Fraud Detection & Fingerprint")

# -------- SESSION STATE --------
if "balance" not in st.session_state:
    st.session_state.balance = 0.0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Simulated fingerprint ID (acts like biometric template)
if "fingerprint_id" not in st.session_state:
    st.session_state.fingerprint_id = "FP1234"   # Registered fingerprint

# -------- ACCOUNT DETAILS --------
st.subheader("👤 Account Details")
name = st.text_input("Customer Name")
account_type = st.selectbox("Account Type", ["Savings", "Current"])

# -------- BALANCE DISPLAY --------
st.subheader("💰 Current Balance")
st.info(f"₹ {st.session_state.balance:.2f}")

# -------- TRANSACTION SECTION --------
st.subheader("💳 Transaction")

amount = st.number_input("Enter Amount", min_value=0.0, step=500.0)
transaction_type = st.radio("Transaction Type", ["Deposit", "Withdraw"])

# -------- FRAUD DETECTION FUNCTION --------
def detect_fraud(amount, transaction_type, balance):
    reasons = []

    if amount > 50000:
        reasons.append("High amount transaction")

    if transaction_type == "Withdraw" and amount > balance:
        reasons.append("Withdrawal exceeds balance")

    if amount == 0:
        reasons.append("Zero amount transaction")

    return reasons

# -------- FINGERPRINT VERIFICATION --------
fingerprint_input = ""
if transaction_type == "Withdraw":
    st.subheader("🖐️ Fingerprint Verification")
    fingerprint_input = st.text_input(
        "Enter Fingerprint ID (Simulated)",
        type="password",
        help="Example: FP1234"
    )

# -------- PROCESS TRANSACTION --------
if st.button("Submit Transaction"):

    fraud_reasons = detect_fraud(amount, transaction_type, st.session_state.balance)

    # Fingerprint check for withdrawal
    if transaction_type == "Withdraw" and fingerprint_input != st.session_state.fingerprint_id:
        st.error("❌ Fingerprint verification failed!")
    
    elif fraud_reasons:
        st.error("⚠️ Fraud Alert Detected!")
        for r in fraud_reasons:
            st.warning(r)

    else:
        if transaction_type == "Deposit":
            st.session_state.balance += amount
            status = "Success"

        else:
            st.session_state.balance -= amount
            status = "Success"

        st.session_state.transactions.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Type": transaction_type,
            "Amount": amount,
            "Balance After": st.session_state.balance,
            "Status": status
        })

        st.success("Transaction completed successfully ✅")

# -------- TRANSACTION HISTORY --------
if st.session_state.transactions:
    st.subheader("📋 Transaction History")
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df)

    st.subheader("📊 Transaction Summary")
    chart_df = df.groupby("Type")["Amount"].sum()
    st.bar_chart(chart_df)
