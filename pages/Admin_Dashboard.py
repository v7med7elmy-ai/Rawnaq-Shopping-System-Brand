import streamlit as st
import pandas as pd
from PIL import Image
import time
import db_manager 
import sys
import os
import base64  #FOR BACKGROUND

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

try:
    st.set_page_config(page_title="Admin Dashboard", layout="wide")
except:
    pass

# ========================

#  Security Check
if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.warning("⛔ Access Denied! You are not an admin.")
    if st.button("Go to Login"):
        st.switch_page("pages/Register.py")
    st.stop() 

# ========================

IMAGE_DIR = "product_images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def save_uploaded_file(uploaded_file, product_name):
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        timestamp = int(time.time())
        safe_name = "".join([c for c in product_name if c.isalpha() or c.isdigit()]).rstrip()
        file_path = os.path.join(IMAGE_DIR, f"{safe_name}_{timestamp}.{file_extension}")
        img = Image.open(uploaded_file)
        img.save(file_path)
        return file_path
    return None
# ====================================

# ========================
# ADMIN PAGE
# ========================
def admin_page():
    #HEADER
    st.markdown("""
        <h1 style='text-align:left;color:#4E342E;
        font-family:"Times New Roman",serif;'>
            Admin Dashboard
        </h1>
    """, unsafe_allow_html=True) 

    st.divider()    
    # ========================

    action = st.sidebar.radio(
        ":yellow[**Choose Operation:**]",
        ["View All Products", "Add New Product", "Edit Product", "Delete Product"]
    )
    
    CATEGORY_MAP = {"Men": 1, "Women": 2}
    
    # ====================================
    # 1. VIEW PRODUCTS
    # ====================================
    
    if action == "View All Products":

        #SUBHEADER
        st.markdown("""
        <h2 style='text-align:left;color:#675543;
        font-family:"Times New Roman",serif;'>
            Current Products
        </h2>
        """, unsafe_allow_html=True) 
        # ========================
    
        products = db_manager.get_all_products()
        if products:
            df = pd.DataFrame(products)
            if not df.empty:
                id_to_name = {v: k for k, v in CATEGORY_MAP.items()}
                if 'category_id' in df.columns:
                    df['category_name'] = df['category_id'].map(id_to_name)
                cols_to_show = ['id', 'name', 'salary', 'stock', 'size', 'color']
                if 'category_name' in df.columns: cols_to_show.append('category_name')
                st.dataframe(df[cols_to_show], width='stretch')
                
                st.write("---")
                
                # ========================
                #SUBHEADER
                st.markdown("""
                <h2 style='text-align:left;color:#675543;
                font-family:"Times New Roman",serif;'>
                    Products Gallery
                </h2>
                """, unsafe_allow_html=True) 
                # ========================
                
                cols = st.columns(4)
                for index, row in df.iterrows():
                    with cols[index % 4]:
                        if row.get('image') and os.path.exists(row['image']):
                            st.image(row['image'], caption=f"{row['name']} - {row['salary']} EGP")
                        else:
                            st.info(f"No Image: {row['name']}")
        else:
            st.info("**The database is currently empty.** ")
    
    # ====================================
    # 2. ADD PRODUCT
    # ====================================

    elif action == "Add New Product":
        
        # ========================
                #SUBHEADER
        st.markdown("""
                <h2 style='text-align:left;color:#675543;
                font-family:"Times New Roman",serif;'>
                    Add New Product
                </h2>
         """, unsafe_allow_html=True) 
        # ========================

        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("**Product Name**")
                selected_cat_name = st.selectbox("**Category**", list(CATEGORY_MAP.keys()))
                salary = st.number_input("**Price (EGP)**", min_value=1.0, step=10.0)
            with col2:
                size = st.selectbox("**Size**", ["S", "M", "L", "XL", "One Size"])
                color = st.text_input("**Color**", "Black")
                stock = st.number_input("**Stock Quantity**", min_value=1, step=1)
                
            # ========================
            #SUBHEADER
            st.markdown("""
                <h2 style='text-align:left;color:#675543;
                font-family:"Times New Roman",serif;'>
                    Product Image
                </h2>
            """, unsafe_allow_html=True) 
            # ========================
            
            uploaded_file = st.file_uploader(":yellow[**Upload Image**]", type=["png", "jpg", "jpeg"])
            submitted = st.form_submit_button(":yellow[**Save Product**]")
            
            if submitted:
                if name and salary and stock and uploaded_file:
                    
                    final_category_id = CATEGORY_MAP[selected_cat_name]
                    image_path = save_uploaded_file(uploaded_file, name)
                    try:
                        db_manager.add_product(name, final_category_id, size, color, salary, stock, image_path)
                        st.success(f"**✅ Product '{name}' added successfully!**")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"**Error: {e}**")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.warning("**⚠ Please fill all fields.**")
                    time.sleep(1)
                    st.rerun()

    # ====================================
    # 3. EDIT PRODUCT
    # ====================================
    
    elif action == "Edit Product":
        # ========================
        #SUBHEADER
        st.markdown("""
            <h2 style='text-align:left;color:#675543;
            font-family:"Times New Roman",serif;'>
                Edit Product Details
            </h2>
        """, unsafe_allow_html=True) 
        # ========================
    
        products = db_manager.get_all_products()
        if products:
            
            product_options = {f"{p['name']} (ID: {p['id']})": p for p in products}
            selected_option = st.selectbox(":yellow[**Select Product**]", list(product_options.keys()))
            selected_product = product_options[selected_option]
            
            with st.form("edit_form"):
                new_name = st.text_input("**Name**", value=selected_product['name'])
                new_salary = st.number_input("**Price**", value=float(selected_product['salary']))
                new_stock = st.number_input("**Stock**", value=int(selected_product['stock']))
                
                if st.form_submit_button(":yellow[**Update Product**]"):
                    db_manager.edit_product(selected_product['id'], new_name, new_salary, new_stock)  
                    st.success("**✅ Product updated successfully!**")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("**No products available.**")
            
    # ====================================
    # 4. DELETE PRODUCT
    # ====================================
    
    elif action == "Delete Product":
        # ========================
        #SUBHEADER
        st.markdown("""
            <h2 style='text-align:left;color:#675543;
            font-family:"Times New Roman",serif;'>
                Delete Product
            </h2>
        """, unsafe_allow_html=True) 
        # ========================
            
        products = db_manager.get_all_products()
        if products:
            product_dict = {f"{p['name']} (ID: {p['id']})": p['id'] for p in products}
            selected_name = st.selectbox(":yellow[**Select Product**]", list(product_dict.keys()))
            if st.button(":yellow[**Permanently Delete**]"):
                product_id = product_dict[selected_name]
                db_manager.delete_product(product_id)
                st.success("**✅ Product deleted.**")
                time.sleep(1)
                st.rerun()
        else:
            st.info("**No products to delete.**")
            
    # ========================
    # LOGOUT BUTTON
    
    st.sidebar.write("---")

    if st.sidebar.button(":yellow[**Logout**]"):
        st.session_state.clear() 
        st.switch_page("pages/Register.py") 

    # ========================
            
# ====================================

if __name__ == "__main__":
    admin_page()