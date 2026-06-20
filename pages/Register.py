import streamlit as st
import team5
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

# TO CHANGE THE BACKGROUND

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

img = get_base64("images/logbg.jpg") 

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
#BACK TO HOMEPAGE
if st.button("⬅ Back to Home Page"):
    st.switch_page("Homepage.py")
# ========================
#HEADER
st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-size:50px;
        font-family:"Times New Roman",serif;'>
            Login & Sign Up
        </h1>
    """, unsafe_allow_html=True) 
st.divider()
# ========================

# ========================

menu = ["Login", "Sign Up"]
choice = st.radio("Choose Option", menu)

# ========================
# LOGIN FORM
# ========================
if choice == "Login":
    
    #SUBHEADER
    st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-size:30px;
        font-family:"Times New Roman",serif;margin-top:10px'>
            Login
        </h1>
    """, unsafe_allow_html=True) 
    # ========================

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(":yellow[Login]"):
        user = team5.login_check(username, password)
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
            st.error("Invalid username or password")

# ========================
# SIGN UP FORM
# ========================
else:
    
    #SUBHEADER
    st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-size:30px;
        font-family:"Times New Roman",serif;margin-top:10px'>
            Sign Up
        </h1>
    """, unsafe_allow_html=True) 
    # ========================

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button(":yellow[Sign Up]"):
        if team5.register_user(username, password, role='user'): 
            st.success("Account created successfully! Please Login now.")
        else:
            st.error("Username already exists. Try another one.")
