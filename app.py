import streamlit as st
import pandas as pd
from Bank import Bank

# PAGE CONFIG
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)

bank = Bank()

# TITLE
st.title("🏦 Bank Management System")
st.markdown("---")

# SIDEBAR MENU
menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Check Balance",
        "Account Details",
        "Update Account",
        "Delete Account",
        "Transaction History"
    ]
)

# CREATE ACCOUNT
if menu == "Create Account":

    st.header("Create New Account")

    name = st.text_input("Full Name")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        step=1
    )

    email = st.text_input("Email Address")

    pin = st.text_input(
        "4 Digit PIN",
        type="password"
    )

    if st.button("Create Account"):

        status, message = bank.create_account(
            name,
            age,
            email,
            pin
        )

        if status:
            st.success(message)

        else:
            st.error(message)

# DEPOSIT MONEY
elif menu == "Deposit Money":

    st.header("Deposit Money")

    account_no = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    amount = st.number_input(
        "Amount",
        min_value=1.0,
        step=1.0
    )

    if st.button("Deposit"):

        status, message = bank.deposit(
            account_no,
            pin,
            amount
        )

        if status:
            st.success(message)

        else:
            st.error(message)

# WITHDRAW MONEY
elif menu == "Withdraw Money":

    st.header("Withdraw Money")

    account_no = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    amount = st.number_input(
        "Amount",
        min_value=1.0,
        step=1.0
    )

    if st.button("Withdraw"):

        status, message = bank.withdraw(
            account_no,
            pin,
            amount
        )

        if status:
            st.success(message)

        else:
            st.error(message)

# CHECK BALANCE
elif menu == "Check Balance":

    st.header("Check Account Balance")

    account_no = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    if st.button("Check Balance"):

        status, balance = bank.check_balance(
            account_no,
            pin
        )

        if status:

            st.success(
                f"Current Balance: ₹{balance}"
            )

        else:
            st.error(balance)

# ACCOUNT DETAILS
elif menu == "Account Details":

    st.header("Account Details")

    account_no = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    if st.button("Show Details"):

        status, data = bank.account_details(
            account_no,
            pin
        )

        if status:

            st.subheader(
                "Customer Information"
            )

            st.write(
                f"**Name:** {data['Name']}"
            )

            st.write(
                f"**Age:** {data['Age']}"
            )

            st.write(
                f"**Email:** {data['Email']}"
            )

            st.write(
                f"**Account Number:** {data['AccountNo']}"
            )

            st.write(
                f"**Balance:** ₹{data['Balance']}"
            )

        else:
            st.error(data)

# UPDATE ACCOUNT
elif menu == "Update Account":

    st.header("Update Account Information")

    account_no = st.text_input(
        "Account Number"
    )

    current_pin = st.text_input(
        "Current PIN",
        type="password"
    )

    new_name = st.text_input(
        "New Name (Optional)"
    )

    new_email = st.text_input(
        "New Email (Optional)"
    )

    new_pin = st.text_input(
        "New PIN (Optional)",
        type="password"
    )

    if st.button("Update Account"):

        status, message = bank.update_account(
            account_no,
            current_pin,
            new_name if new_name else None,
            new_email if new_email else None,
            new_pin if new_pin else None
        )

        if status:
            st.success(message)

        else:
            st.error(message)

# DELETE ACCOUNT
elif menu == "Delete Account":

    st.header("Delete Account")

    st.warning(
        "This action cannot be undone."
    )

    account_no = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    confirm = st.checkbox(
        "I confirm account deletion"
    )

    if st.button("Delete Account"):

        if not confirm:

            st.warning(
                "Please confirm deletion."
            )

        else:

            status, message = bank.delete_account(
                account_no,
                pin
            )

            if status:
                st.success(message)

            else:
                st.error(message)

# TRANSACTION HISTORY
elif menu == "Transaction History":

    st.header("Transaction History")

    account_no = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    if st.button("View Transactions"):

        status, data = bank.get_transactions(
            account_no,
            pin
        )

        if status:

            if len(data) == 0:

                st.info(
                    "No transactions found."
                )

            else:

                df = pd.DataFrame(data)

                st.dataframe(
                    df,
                    use_container_width=True
                )

        else:
            st.error(data)