import streamlit as st
import db_manager
import base64
import time
import sys
import os

# FONT STYLE
def apply_custom_style():
    st.markdown("""
        <style>
        h1, h2, h3, h4, h5, h6, p, button {
            font-family: "Times New Roman", serif;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_style()

# ========================
# LINKING
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
# ========================

#CHANGING SIDEBAR COLOR
st.markdown("""
<style>
  div[data-testid="stSidebarContent"] {
    background-color: #675543 !important;
}
</style>
""", unsafe_allow_html=True)

# ========================

# BUTTONS DESIGN
st.markdown("""
    <style>
    div.stButton > button:first-child {
    background-color: #4E342E;
    color: white;
    }
    div.stButton > button:hover {
    background-color: #675543;
    color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
# ========================
try:
    st.set_page_config(page_title="Payment", layout="wide")
except:
    pass
# ========================

#CHANGING BACKGROUND

# Load image as base64
with open("images/payment.jpg", "rb") as f:
    img = base64.b64encode(f.read()).decode()

# Apply background
st.markdown(f"""
    <style>
        .stApp {{
            background: url("data:image/png;base64,{img}") no-repeat center center fixed;
            background-size: cover;
        }}
    </style>
""", unsafe_allow_html=True)

# ========================
 
#HEADER
st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-size:50px;
        font-family:"Times New Roman",serif;'>
            Payment
        </h1>
    """, unsafe_allow_html=True) 
st.write("---")

# ========================
if 'payment_success' not in st.session_state:
    st.session_state['payment_success'] = False

# ========================
#MAKING SURE USER EXISTS
user_id = st.session_state.get('user_id')

# ========================

payment_method = st.radio(":yellow[**Choose Payment Method:**]", ("Visa", "Cash on Delivery"))
st.write("---")

if payment_method == "Visa":
    col1, col2 = st.columns(2)
    with col1:
        visa_number = st.text_input("**Card Number (16 digits)**", max_chars=16)
        expire_date = st.text_input("**Expiry Date (MM/YY)**", max_chars=4)
    with col2:
        cvv_number = st.text_input("**CVV (3 digits)**", max_chars=3, type="password")

    # Submit button
    if st.button(":yellow[**Submit Payment**]") and not st.session_state['payment_success']:
        errors = False

        if len(visa_number) != 16 or not visa_number.isdigit():
            st.error("**Warning: Visa number must be exactly 16 digits.**")
            errors = True
        if len(cvv_number) != 3 or not cvv_number.isdigit():
            st.error("**Warning: CVV must be exactly 3 digits.**")
            errors = True
        if len(expire_date) != 4 or not expire_date.isdigit():
            st.error("**Warning: Expire Date must be exactly 4 digits.**")
            errors = True

        if not errors:
            st.session_state['payment_success'] = True
            st.success("**Payment Successful! Your order has been placed.**")
            st.balloons()

    # ========================
    # Feedback (outside button!)
    # ========================
    if st.session_state['payment_success']:
        st.write("---")
         
        #SUBHEADER
        st.markdown("""
        <h3 style='text-align:left;color:#675543;
        font-family:"Times New Roman",serif;'>
            Rate your experience
        </h3>
        """, unsafe_allow_html=True) 

        sentiment = st.feedback("stars")
        if sentiment is not None:
            st.session_state["sentiment"] = sentiment

# ========================

# Redirect if feedback exists
if st.session_state.get("sentiment") is not None:
    st.write("**Thank you for rating!**")
    time.sleep(2)
    # reset states
    st.session_state['payment_success'] = False
    st.session_state['sentiment'] = None
    st.switch_page("Homepage.py")
    
    
# ====================================

# ========================
#     CASH ON DELIVERY
# ========================   
    
elif payment_method == "Cash on Delivery":
    st.info("**You will pay when the order arrives.**")
    if st.button(":yellow[**Confirm Order**]"):
        st.session_state['payment_success'] = True
        st.success("**Order Confirmed!**")
        st.snow()
        time.sleep(2)
        st.switch_page("Homepage.py")