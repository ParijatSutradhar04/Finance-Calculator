import streamlit as st

def sip(deposit, rate, time, step_up):
    total_amount = 0
    time = time * 12
    for i in range(time):
        total_amount = (total_amount + deposit) * (1 + rate/12/100)
        if (i+1) % 12 == 0:
            deposit = deposit * (1 + step_up/100)
    return total_amount

def lumpsum(principal, rate, time):
    total_amount = principal * (1 + rate/100)**time
    return total_amount

def lumpsum_with_emi(principal, rate, emi_rate, time):
    total_amount = principal
    time = time * 12
    emi_rate = emi_rate/12/100
    rate = rate/12/100
    emi = (principal * emi_rate * (1 + emi_rate)**time) / ((1 + emi_rate)**time - 1)

    for i in range(time):
        total_amount = total_amount * (1 + rate) - emi
    return total_amount

st.title("Investment Calculator")
option = st.selectbox(
    'Choose an investment option:',
    ['SIP', 'Lumpsum', 'Lumpsum with EMI', 'SIP and Lumpsum with EMI']
)

if option == 'SIP':
    deposit = st.number_input("Monthly Deposit Amount", min_value=0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    time = st.number_input("Time Period (years)", min_value=0)
    step_up = st.number_input("Annual Step-Up Percentage (%)", min_value=0.0)
    if st.button("Calculate SIP"):
        total = sip(deposit, rate, time, step_up)
        st.write(f"The total amount after {time} years is: {total:.2f}")

elif option == 'Lumpsum':
    principal = st.number_input("Lumpsum Amount", min_value=0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    time = st.number_input("Time Period (years)", min_value=0)
    if st.button("Calculate Lumpsum"):
        total = lumpsum(principal, rate, time)
        st.write(f"The total amount after {time} years is: {total:.2f}")

elif option == 'Lumpsum with EMI':
    principal = st.number_input("Lumpsum Amount", min_value=0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    emi_rate = st.number_input("EMI Rate (%)", min_value=0.0)
    time = st.number_input("Time Period (years)", min_value=0)
    if st.button("Calculate Lumpsum with EMI"):
        total = lumpsum_with_emi(principal, rate, emi_rate, time)
        st.write(f"The total amount after {time} years is: {total:.2f}")

elif option == 'SIP and Lumpsum with EMI':
    deposit = st.number_input("Monthly Deposit Amount", min_value=0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    time = st.number_input("Time Period (years)", min_value=0)
    step_up = st.number_input("Annual Step-Up Percentage (%)", min_value=0.0)
    principal = st.number_input("Lumpsum Amount", min_value=0)
    emi_rate = st.number_input("EMI Rate (%)", min_value=0.0)
    if st.button("Calculate Combined Option"):
        total_sip = sip(deposit, rate, time, step_up)
        total_emi = lumpsum_with_emi(principal, rate, emi_rate, time)
        st.write(f"The total deposit amount is: {deposit*time*12}")
        st.write(f"The total amount after {time} years is: {total_sip + total_emi:.2f}")
