import streamlit as st
import db_manager
import base64
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

#LINKING
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

#CHANGING BACKGROUND

# Load image as base64
with open("images/logbg.jpg", "rb") as f:
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
#BACK TO HOMEPAGE
if st.button(":yellow[**⬅ Home**]"):
    st.switch_page("Homepage.py")
# ========================
#HEADER
st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-family:"Times New Roman",serif;'>
            Login & Sign Up
        </h1>
    """, unsafe_allow_html=True) 
st.divider()
# ========================

menu = ["Login", "Sign Up"]
choice = st.radio(":yellow[**Choose Option**]", menu)

# ========================
# LOGIN FORM
# ========================
if choice == "Login":
    
    #SUBHEADER
    st.markdown("""
        <h2 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
            Login
        </h2>
    """, unsafe_allow_html=True) 
    # ========================

    username = st.text_input("**Username**")
    password = st.text_input("**Password**", type="password")

    if st.button(":yellow[**Login**]"):
        user = db_manager.login_check(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = user['id']
            st.session_state['username'] = user['username']
            st.session_state['role'] = user['role']
            
            st.success(f"Welcome {user['username']}!")
            
            if user['role'] == "admin":
                st.switch_page("pages/Admin_Dashboard.py")  
                st.rerun() 
            else:
                st.switch_page("Homepage.py") 
                st.rerun()
        else:
            st.error("**Invalid username or password**")

# ========================
# SIGN UP FORM
# ========================
else:
    
    #SUBHEADER
    st.markdown("""
        <h2 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
            Sign Up
        </h2>
    """, unsafe_allow_html=True) 
    # ========================

    username = st.text_input("**New Username**")
    password = st.text_input("**New Password**", type="password")

    if st.button(":yellow[**Sign Up**]"):
        if db_manager.register_user(username, password, role='user'): 
            st.success("**Account created successfully! Please Login now.**")
        else:
            st.error("**Username already exists. Try another one.**")
