import streamlit as st

st.set_page_config(page_title="Faraz Jewelry AI", page_icon="💎")

st.title("💎 Faraz Jewelry Sales Tool")

# --- SIDEBAR ---
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("Budget", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.sidebar.selectbox("Metal", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("Style", ["Simple", "Classic", "Iced Out"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Wear", "Gift", "Special Event"])

# --- THE SMARTER LOGIC ---
# We determine the best product based on Metal and Budget logic
item_name = "Silver Box Chain" # Safe fallback
image_url = "https://m.media-amazon.com/images/I/51b+I0sS+QL._AC_UY1100_.jpg"

# LOGIC TREE
if style == "Iced Out":
    item_name = "Diamond Cross Pendant"
    image_url = "https://m.media-amazon.com/images/I/61Z+2u+qLgL._AC_UY1100_.jpg"

elif metal == "Gold":
    if budget == "$5000+":
        item_name = "Solid Gold Miami Cuban Link"
        image_url = "https://m.media-amazon.com/images/I/61F9kL-xLcL._AC_UY1100_.jpg"
    else:
        item_name = "3mm Gold Rope Chain"
        image_url = "https://m.media-amazon.com/images/I/71+q+Mh-K+L._AC_UY1100_.jpg"

elif metal == "Silver":
    if budget == "$5000+":
        item_name = "Real Diamond Tennis Bracelet (White Gold)"
        image_url = "https://m.media-amazon.com/images/I/71rQ6Q01m+L._AC_UY1100_.jpg"
    else:
        item_name = "Sterling Silver Box Chain"
        image_url = "https://m.media-amazon.com/images/I/51b+I0sS+QL._AC_UY1100_.jpg"

elif metal == "White Gold" or metal == "Platinum":
    if budget == "$100":
        item_name = "White Gold Plated Chain"
        image_url = "https://m.media-amazon.com/images/I/51b+I0sS+QL._AC_UY1100_.jpg"
    else:
        item_name = "Moissanite Tennis Bracelet"
        image_url = "https://m.media-amazon.com/images/I/71w-w-q-GgL._AC_UY1100_.jpg"

elif metal == "Rose Gold":
    item_name = "Rose Gold Rope Chain"
    image_url = "https://m.media-amazon.com/images/I/61y8aK9vjLR._AC_UY1100_.jpg"

# --- DISPLAY ---
st.header("Recommended Item:")
st.success(f"**{item_name}**")
st.image(image_url, width=400)

# --- SCRIPT ---
st.write("---")
st.subheader("🗣️ Sales Script")

if occasion == "Gift":
    st.info(f"Say this: 'This {item_name} is our best-selling gift. It looks incredible in the box and fits anyone perfectly.'")
elif occasion == "Special Event":
    st.info(f"Say this: 'The {item_name} is designed to catch the light. It will definitely stand out at your event.'")
else:
    st.info(f"Say this: 'This is solid and durable. You can wear this {item_name} every single day without worrying.'")
