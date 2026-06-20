import streamlit as st
import team5
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

try:
    st.set_page_config(page_title="Payment", layout="wide")
except:
    pass

# ========================

# TO CHANGE THE BACKGROUND

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

img = get_base64("images/payment.jpg") 

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover; 
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# ========================

# BACK TO HOMEPAGE
if st.button("⬅ Back to Home"):
    st.session_state['payment_success'] = False  # تصفر الحالة وانت خارج
    st.switch_page("Homepage.py")
   
# ========================
 
#HEADER
st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-size:50px;
        font-family:"Times New Roman",serif;'>
            Payment
        </h1>
    """, unsafe_allow_html=True) 
st.write("---")

if 'payment_success' not in st.session_state:
    st.session_state['payment_success'] = False

#MAKING SURE USER EXISTS
user_id = st.session_state.get('user_id')



payment_method = st.radio("Choose Payment Method:", ("Visa", "Cash on Delivery"))
st.write("---")

if payment_method == "Visa":
    
    #SUBHEADER
    st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-size:30px;
        font-family:"Times New Roman",serif;'>
            Visa Details
        </h1>
    """, unsafe_allow_html=True)
    
    
    col1, col2 = st.columns(2)

    with col1:
        visa_number = st.text_input("Card Number (16 digits)", max_chars=16)
        expire_date = st.text_input("Expiry Date (MM/YY)",max_chars=4)
    with col2:
        cvv_number = st.text_input("CVV (3 digits)", max_chars=3, type="password")
        
    if st.button(":yellow[Submit Payment]") or st.session_state['payment_success']:
        errors = False
        if not st.session_state['payment_success']:
            if len(visa_number) != 16 or not visa_number.isdigit():
                st.error("Warning: Visa number must be exactly 16 digits.")
                errors = True
            if len(cvv_number) != 3 or not cvv_number.isdigit():
                st.error("Warning: CVV must be exactly 3 digits.")
                errors = True
        
        if not errors:
            st.session_state['payment_success'] = True
            st.success("Payment Successful! Your order has been placed.")
            st.balloons()

            st.write("---")
            st.write("### Rate your experience")
            sentiment = st.feedback("stars")
            if sentiment is not None:
                st.write("Thank you for rating!")
                time.sleep(2)
                st.session_state['payment_success'] = False 
                st.switch_page("Homepage.py")
                

elif payment_method == "Cash on Delivery":
    st.info("You will pay when the order arrives.")
    if st.button(":yellow[Confirm Order]"):
        st.session_state['payment_success'] = True
        st.success("Order Confirmed!")
        st.snow()
        time.sleep(2)
        st.switch_page("Homepage.py")