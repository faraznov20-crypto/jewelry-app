import streamlit as st

st.set_page_config(page_title="Faraz Jewelry", page_icon="💎")
st.title("💎 Faraz Jewelry Sales Tool")

# --- 1. INPUTS ---
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("Budget", ["$100", "$500", "$1000", "$5000+"])
metal = st.sidebar.selectbox("Metal Preference", ["Silver", "Gold", "Rose Gold", "White Gold"])
style = st.sidebar.selectbox("Style", ["Simple", "Iced Out"])

# --- 2. STRICT LOGIC (One Rule Wins) ---
# We use a single chain of IF/ELIF. The first one that is true WINS.

# RULE A: High Budget -> Real Diamonds
if budget == "$5000+":
    item_name = "Real Diamond Tennis Bracelet"
    image_url = "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=500"
    desc = "This is a VVS Diamond piece. Pure luxury."

# RULE B: Iced Out Style -> Diamond Cross
elif style == "Iced Out":
    item_name = "Diamond Cross Pendant"
    image_url = "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=500"
    desc = "This pendant shines from across the room."

# RULE C: Gold Metal -> Gold Rope Chain
elif metal == "Gold" or metal == "Rose Gold":
    item_name = "Solid Gold Rope Chain"
    image_url = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=500"
    desc = "Our best-selling gold chain. Classic and heavy."

# RULE D: Silver/White Metal (Default) -> Silver Chain
else:
    item_name = "Sterling Silver Box Chain"
    # Using a clear silver chain image
    image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=500"
    desc = "A durable silver chain for daily wear."

# --- 3. SHOW RESULT ---
st.header("Recommended Item:")
st.success(f"**{item_name}**")
st.image(image_url, width=400)
st.info(f"🗣️ Say this: '{desc}'")
