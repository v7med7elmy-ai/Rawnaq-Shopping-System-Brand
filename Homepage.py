import streamlit as st
import db_manager
import sqlite3 
import base64
import time


# FONT STYLE
def apply_custom_style():
    st.markdown("""
        <style>
        h1, h2, h3, h4, h5, h6, p, button {
            font-family: "Times New Roman", serif;
            text-shadow: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
apply_custom_style()
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

#CHANGING SIDEBAR COLOR
st.markdown("""
<style>
  div[data-testid="stSidebarContent"] {
    background-color: #675543 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================

# --- Helper Function for Base64 Encoding ---
def img_to_base64(image_path):
    """Converts a local image file to a Base64 string for direct embedding in HTML/CSS."""
    try:
        if image_path.lower().endswith(('.png', '.gif')):
            mime_type = 'image/png'
        elif image_path.lower().endswith(('.jpeg', '.jpg')):
            mime_type = 'image/jpeg'
        else:
            mime_type = 'image/jpeg' 
            
        with open(image_path, "rb") as img_file:
            base64_string = base64.b64encode(img_file.read()).decode()
            return f"data:{mime_type};base64,{base64_string}"
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error converting image {image_path}: {e}")
        return None
# ------------------------------------------

st.set_page_config(page_title="Fashion Brand", layout="wide")


def set_bg_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .product-img {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .product-card {{
            padding: 12px;
            border-radius: 16px;
            background: rgba(0,0,0,0.45);
            backdrop-filter: blur(6px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            transition: 0.2s;
        }}
        .product-card:hover {{
            transform: scale(1.03);
            box-shadow: 0 6px 18px rgba(0,0,0,0.6);
        }}

        h1, h2, h3, h4, p, span, div {{
            text-shadow: 2px 2px 4px #000000;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Image not included in path: {image_path} ")

set_bg_image('images/Cream_bg.png')

# ==========================

def init_data_fix():
    try:
        import init_db
    except:
        pass

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Men')")
        cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (2, 'Women')")
        conn.commit()
    except:
        pass

    existing_products = db_manager.get_all_products()
    if not existing_products:
        db_manager.add_product("Vintage Jacket", 1, "M", "Beige", 500.0, 10, "images/jacket2.jpg") 
        db_manager.add_product("Classic Pants", 1, "32", "Khaki", 600.0, 15, "images/pants.jpg")
        db_manager.add_product("Grey Sweater", 2, "M", "Grey", 750.0, 8, "images/sweater.jpg")
        db_manager.add_product("Brown Bag", 2, "OneSize", "Brown", 450.0, 20, "images/bag.jpg")

    conn.close()

init_data_fix()

# ==========================================

# Initializing Session State 
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'selected_cat_id' not in st.session_state:
    st.session_state['selected_cat_id'] = None
if 'selected_product' not in st.session_state:
    st.session_state['selected_product'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None 
if 'checkout_status' not in st.session_state: 
    st.session_state['checkout_status'] = 'idle'


def go_to(page_name):
    st.session_state['page'] = page_name
    st.rerun()

def logout_user():
    st.session_state['user_id'] = None 
    st.session_state['page'] = 'home'
    st.toast("Logged out successfully!")
    st.rerun()

def login_user_simulated(user_id=1):
    st.switch_page("Register.py")

# ==========================================

def render_home():
    # BRAND NAME
    st.markdown("""
        <h1 style='text-align:center;color:#4E342E;font-size:60px;
        font-family:"Times New Roman",serif;'>
            RAWNAQ
        </h1>
        <h4 style='text-align: center; font-size: 16px; color: #291C0E;
        font-family:"Times New Roman",serif'>
            Style for Men & Women
        </h4>
    """, unsafe_allow_html=True)    

    st.divider()
    
# =============================
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(" **MEN COLLECTION**", width="stretch"):
            st.session_state['selected_cat_id'] = 1
            go_to('category')
    with col2:
        if st.button("**WOMEN COLLECTION**", width="stretch"):
            st.session_state['selected_cat_id'] = 2
            go_to('category')

    st.write("")
# =============================

    st.image("images\home1.jpg")

# =============================

def render_category():
    
    
    
    # =====================
    cat_id = st.session_state['selected_cat_id']
    cat_name = "Men" if cat_id == 1 else "Women"

    if st.button("**⬅ Home**"):
        go_to('home')

    st.title(f"{cat_name} Section")
    
    #SHOW ALL PRODUCTS OF THE CATEGORY
    all_products = db_manager.get_all_products() 
    base_products = [p for p in all_products if p['category_id'] == cat_id]

    if not base_products:
        st.warning("**No products yet !**")
        return
    
    
    #FILTERS
    with st.expander(" :yellow[**Filter & Search**] ", expanded=False):
        c_filter1, c_filter2 = st.columns(2)
        #CATEGORY FILTER
        with c_filter1:
            filter_options = ["All", "Jacket", "Pants", "Sweater", "Bag"]
            selected_type = st.selectbox(":yellow[**Select product**]", filter_options)

        # PRICE FILTER
        with c_filter2:
            
            prices = [p['salary'] for p in base_products]
            if prices:
                min_p, max_p = int(min(prices)), int(max(prices))
                # Adjust range if min and max are the same
                if min_p == max_p: 
                    min_p = max(0, min_p - 100)
                    max_p = max_p + 100
                    
                price_range = st.slider(" :yellow[**Price Range (EGP)**]", min_p, max_p, (min_p, max_p))
            else:
                price_range = (0, 10000)

    final_products = []
    for p in base_products:
        if not (price_range[0] <= p['salary'] <= price_range[1]):
            continue
        
        if selected_type != "All":
            if selected_type.lower() not in p['name'].lower():
                continue
            
        final_products.append(p)


    if not final_products:
        st.info(f"There is no {selected_type} in here yet. ")
    else:
        st.caption(f"There is {len(final_products)} product-s available.")
        
        cols = st.columns(4)
        for i, product in enumerate(final_products):
            with cols[i % 4]:
                st.markdown("<div class='product-card'>", unsafe_allow_html=True)

                image_data_url = img_to_base64(product['image'])
                if image_data_url:
                    st.markdown(f"<img src='{image_data_url}' class='product-img'/>", unsafe_allow_html=True)
                else:
                    st.write("❌ No Image") 

                st.subheader(product['name'])
                st.write(f"{product['salary']} EGP**")
                
                # Fetch stock dynamically
                stock = product.get('stock', 0)
                st.write(f"Stock: {stock}")

                if stock and stock > 0:
                    if st.button("**Add 🛒**", key=f"add_{product['id']}", width="stretch"):
                        user_id = st.session_state.get('user_id') 
                        if user_id:
                            db_manager.add_to_cart(user_id, product['id'], 1)
                            st.toast("**ADDED TO CART! 🛒**")
                        else:
                            st.warning("**LOG IN FIRST!**")
                            time.sleep(2)
                            st.switch_page("pages/Register.py")
                else:
                    st.button("**Sold Out**", disabled=True, width="stretch")

                if st.button("**Details 📄**", key=f"view_{product['id']}", width="stretch"):
                    st.session_state['selected_product'] = product
                    go_to('product')

                st.markdown("</div>", unsafe_allow_html=True)
                
def render_product():
    
    
    
    if st.button(":yellow[**⬅ Back**]"):
        go_to('category')

    product = st.session_state['selected_product']
    if not product:
        return

    # Use data from session state for simplicity
    stock = product.get('stock', 0) 

    c1, c2 = st.columns([1, 1])
    with c1:
        image_data_url = img_to_base64(product['image'])
        if image_data_url:
            st.markdown(
                f"<img src='{image_data_url}' class='product-img'/>",
                unsafe_allow_html=True
            )
        else:
            st.error("Product image failed to load.")

    with c2:
        st.title(product['name'])
        st.subheader(f"{product['salary']} EGP")
        
        st.write(f"Stock: {stock}")
        st.divider()

        desc = f"""
        - Color: {product['color']}
        - Size: {product['size']}
        - Premium Material
        """
        st.info(desc)

        size = st.selectbox(":yellow[**Choose Size**]", ["S", "M", "L", "XL", "XXL", "One Size"])
        
        # Limit quantity to available stock
        max_qty = int(stock) if isinstance(stock, int) else 10
        qty = st.number_input(":yellow[**Quantity**]", 1, max_qty, 1)

        if stock and stock > 0:
            if st.button("**Add to Cart**"):
                user_id = st.session_state.get('user_id') 
                if user_id:
                    db_manager.add_to_cart(user_id, product['id'], qty)
                    st.success(f"Added {qty} item(s) to cart!")
                    time.sleep(1)
                    st.rerun() 
                else:
                    st.warning("**Please log in to add items to your cart.**")
        else:
            st.button("**Sold Out**", disabled=True, width="stretch")


def render_cart():
    
    if st.button(":yellow[**⬅ Back to Shopping**]"):
        st.session_state['checkout_status'] = 'idle'
        go_to('home')
        
    user_id = st.session_state.get('user_id')
    
    #HEADER
    st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-size:50px;
        font-family:"Times New Roman",serif;'>
            My Cart
        </h1>
    """, unsafe_allow_html=True) 
    st.write("---")

    # ========================
    
    # --- 1. HANDLE POST-CHECKOUT SUCCESS ---
    if st.session_state['checkout_status'] == 'success':
        st.success("**🎉 Your order has been placed!**")
        time.sleep(1) 
        
        # After delay, redirect to home page and reset status
        st.session_state['checkout_status'] = 'idle'
        go_to('home')
        return

    # --- 2. HANDLE CHECKOUT PENDING (The state showing "Redirecting...") ---
    if st.session_state['checkout_status'] == 'pending_redirect':
        st.info("**🎉 Your order has been placed!**") 
        
        time.sleep(1) 
        
        # *** CRITICAL CHANGE: Use the transactional function ***
        if user_id:
            # This calls the function that updates stock AND clears the cart
            if db_manager.process_order_and_update_stock(user_id):
                st.session_state['checkout_status'] = 'success'
            else:
                # Stock error or DB transaction failure
                st.error("**Error processing order. Check stock levels or user login status and try again.**")
                st.session_state['checkout_status'] = 'idle' # Go back to idle state
        else:
            st.error("**User ID not found. Cannot process order.**")
            st.session_state['checkout_status'] = 'idle'
        
        # Trigger the rerun to render the 'success' or error state
        st.rerun()
        return

    if not user_id:
        st.info("**You must be logged in to view your cart.**")
        return

    items = db_manager.view_cart(user_id)

    if not items:
        st.info("**Your cart is empty.**")
        return

    total = 0

    # Display Cart Items
    for item in items:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
            with c1:
                image_data_url = img_to_base64(item['image'])
                if image_data_url:
                    st.markdown(
                        f"<img src='{image_data_url}' width='80'/>",
                        unsafe_allow_html=True
                    )
                else:
                    st.write("No Image")

            with c2:
                st.subheader(f":yellow[{item['name']}]")
                st.caption(f"**Qty: {item['quantity']}**")
                
                if item.get('stock', 0) < item['quantity']:
                    st.error(f"⚠ Stock Warning: Only {item.get('stock', 0)} available!")

            with c3:
                item_total = item['salary'] * item['quantity']
                total += item_total
                st.write(f"**{item_total} EGP**")

            with c4:
                if st.button(":yellow[**Remove ❌**]", key=f"del_{item['cart_item_id']}"): 
                    db_manager.remove_from_cart(item['cart_item_id'])
                    st.rerun()

    st.divider()
    st.subheader(f":orange[**Total: {total} EGP**]")
    
    if st.button(":yellow[**Checkout**]"):
        st.session_state['checkout_status'] = 'pending_redirect'
        st.session_state['payment_success'] = False  
        st.switch_page("pages/Payment.py")

        
# ========================
# Profile Page 
# ========================

def render_profile():
    
    if st.button(":yellow[**⬅ Home**]"):
        go_to('home')
       
    # ========================
    #SUBHEADER
    st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-family:"Times New Roman",serif;'>
            My Profile
        </h1>
    """, unsafe_allow_html=True) 
    # ========================
    #SUBHEADER
    st.markdown("""
        <h5 style='text-align:left;color:#4E342E;font-family:"Times New Roman",serif;'>
            Manage your personal details and security settings.
        </h5>
    """, unsafe_allow_html=True) 
    
    st.divider()
    # ========================
    
    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error("You are not logged in.")
        return

    current_user_data = db_manager.get_user_by_id(user_id)
    
    if not current_user_data:
        st.error("User not found in database.")
        return
    
    # ========================
    #SUBHEADER
    st.markdown("""
        <h2 style='text-align:left;color:#4B3D33;font-family:"Times New Roman",serif;'>
            Personal Details
        </h2>
    """, unsafe_allow_html=True) 
    
    # ========================   
    st.markdown(f":orange[**Current Name:**] **{current_user_data['username']}**")

    if 'role' in current_user_data:
        st.markdown(f":orange[**Role:**] **{current_user_data['role']}**")
    
    # ========================
    #SUBHEADER
    st.markdown("""
        <h3 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
            Update Name
        </h3>
    """, unsafe_allow_html=True) 
    
    # ======================== 
    
    #USERNAME CHANGING
    with st.form("update_name_form"):
        new_name = st.text_input(":orange[**New Name**]", value=current_user_data['username'])
        
        if st.form_submit_button(":yellow[**Update Name**]"):
            if new_name and new_name != current_user_data['username']:

                if db_manager.update_username(user_id, new_name):
                    st.success(f"Name updated successfully to: {new_name}")
                    time.sleep(1) 
                    st.rerun()    
                else:
                    st.error("Username already exists, please choose another one.")
            elif new_name == current_user_data['username']:
                st.warning("No changes made to the name.")
            
    st.divider()
    
    # ========================
    #SUBHEADER
    st.markdown("""
        <h2 style='text-align:left;color:#4B3D33;font-family:"Times New Roman",serif;'>
            Security
        </h2>
    """, unsafe_allow_html=True) 
    
    # ======================== 

    masked_pass = "*" * len(str(current_user_data['password']))
    st.markdown(f":orange[**Current Password:**] {masked_pass}")
    
    # ========================
    #SUBHEADER
    st.markdown("""
        <h3 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
            Change Password
        </h3>
    """, unsafe_allow_html=True) 
    
    # ======================== 
    
    #PASSWORD CHANGING
    with st.form("change_password_form"):
        current_password_input = st.text_input(":orange[**Current Password**]", type="password")
        new_password = st.text_input(":orange[**New Password**]", type="password")
        confirm_password = st.text_input(":orange[**Confirm New Password**]", type="password")
        
        if st.form_submit_button(":yellow[**Change Password**]"):
            
            if current_password_input != current_user_data['password']:
                st.error("**Incorrect Current Password!**")
                
            elif new_password != confirm_password:
                st.error("**New Password and Confirmation Password do not match.**")
                
            elif len(new_password) < 4: 
                st.error("**Password must be at least 4 characters.**")
                
            else:
                db_manager.update_password(user_id, new_password)
                st.success("**Password changed successfully!**")
                time.sleep(1)
                st.rerun()

    st.divider()
    
    if st.button(":orange[**➡ Logout**]", width="stretch"):
        logout_user()

# =====================
##  About Us Page 
# =====================

def render_about():
    
    # Back button
    if st.button(":orange[**⬅ Home**]"):
        go_to('home') 
        
    #HEADER
    st.markdown("""
        <h1 style='text-align:left;color:#4E342E;font-family:"Times New Roman",serif;'>
            About RAWNAQ
        </h1>
    """, unsafe_allow_html=True) 
    st.divider()
    # ========================
    
    #HEADER
    st.markdown("""
        <h3 style='text-align:left;color:#533E32;font-family:"Times New Roman",serif;'>
            Our Story and Vision
        </h3>
    """, unsafe_allow_html=True) 
    # ========================
    
    #SUBHEADER
    st.markdown("""
    <h6 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
        RAWNAQ BRAND was founded on the principle of providing high-quality, stylish fashion that is accessible to everyone. 
        We believe that clothing is more than just fabric—it's a form of self-expression.
    </h6>
    """, unsafe_allow_html=True) 
    # ========================
    
    #HEADER
    st.markdown("""
        <h3 style='text-align:left;color:#533E32;font-family:"Times New Roman",serif;'>
            Quality and Materials
        </h3>
    """, unsafe_allow_html=True) 
    # ========================
    
    #SUBHEADER
    st.markdown("""
    <h6 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
        We are committed to sustainability and ethical sourcing. All our garments are crafted 
        from premium materials, including organic cotton and recycled fibers, ensuring durability and comfort.
    </h6>
    """, unsafe_allow_html=True) 
    # ========================
    st.divider()
    # ========================

    col_contact1, col_contact2 = st.columns(2)
    
    with col_contact1:
            
        #SUBHEADER
        st.markdown("""
        <h2 style='text-align:left;color:#533E32;font-family:"Times New Roman",serif;'>
            📍Contact Info
        </h2>
        """, unsafe_allow_html=True) 
        # ========================
    
        st.markdown(":orange[**📞 Phone:**] **+20 1022826895**") 
        st.markdown(":orange[**🏢 Address:**] **Cairo, Egypt**")
        st.markdown(":orange[**📧 Email:**] **rawnaq@gmail.com**")
        
    with col_contact2:
            
        #SUBHEADER
        st.markdown("""
        <h2 style='text-align:left;color:#533E32;font-family:"Times New Roman",serif;'>
            📱 Social Media
        </h2>
        """, unsafe_allow_html=True) 
        # ========================
        
        st.link_button(":yellow[**📸 Instagram**]", "https://www.instagram.com/rawnaq_shop28")
        st.link_button(":yellow[**🎵 TikTok**]", "https://www.tiktok.com/@rawnaq_shop_")
    
    st.divider()
    
    # ========================
    #SUBHEADER
    st.markdown("""
    <h2 style='text-align:left;color:#533E32;font-family:"Times New Roman",serif;'>
        👥 Development Teams
    </h2>
    """, unsafe_allow_html=True) 
    # ========================
    main_col1, main_col2 = st.columns(2)
    
    # ==========================
    
    with main_col1:
        
        
        t3_boys, t3_girls = st.columns(2)
        
        # 1. Boys Column
        with t3_boys:
            st.markdown(":orange[**Boys staff**]")
            st.markdown("""
            <h6 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
                <ul>
                    <li>Ahmed Helmy</li>
                    <li>Ammar Yasser</li>
                    <li>Abdelrhman Ashraf</li>
                    <li>Ahmed Saber</li>
                    <li>Ahmed Mohammad</li>
                </ul>
            </h6>
            """, unsafe_allow_html=True)

        # 2. Girls Column
        with t3_girls:
            st.markdown(":orange[**Girls staff**]")
            st.markdown("""
            <h6 style='text-align:left;color:#675543;font-family:"Times New Roman",serif;'>
                <ul>
                    <li>Rokaya Alaa </li>
                    <li>Mariam Osama</li>
                    <li>Maya Seraj</li>
                    <li>Lynah Adel</li>
                    <li>Walaa Magdy</li>
                </ul>
            </h6>
            """, unsafe_allow_html=True)

# =================================

# Sidebar
with st.sidebar:

    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=100)
    
    st.divider()
    
    #HEADER
    st.markdown("""
        <h1 style='text-align:left;color:blanchedalmond;font-family:"Times New Roman",serif;'>
            Menu
        </h1>
    """, unsafe_allow_html=True) 
    
    # ========================
    
    if st.button("**Home Page**"):
        go_to('home')

    user_is_logged_in = st.session_state.get('user_id') is not None

    if user_is_logged_in:
        # LOGGED IN VIEW
        if st.button(" **My Profile**"):
            go_to('profile')

        cart_count = 0
        try:
            cart_count = len(db_manager.view_cart(st.session_state['user_id']))
        except Exception as e:
            pass 
            
        if st.button(f"**🛒 My Cart ({cart_count})**"):
            go_to('cart')
            
        st.divider()
        if st.button("**➡ Logout**", width="stretch"):
            logout_user()

    else:
        # LOGGED OUT VIEW
        if st.button("**Login / Sign Up**", width="stretch"):
            st.switch_page("pages/Register.py")
            
    st.divider()

    if st.button(" **About Us**"):
        go_to('about')   

# =================================

# Page routing
if st.session_state['page'] == 'home':
    render_home()
elif st.session_state['page'] == 'category':
    render_category()
elif st.session_state['page'] == 'product':
    render_product()
elif st.session_state['page'] == 'cart':
    render_cart()
elif st.session_state['page'] == 'profile': 
    render_profile()
elif st.session_state['page'] == 'about':
    render_about()