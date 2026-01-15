import streamlit as st
from PIL import Image
import os

# ---------------------------------------------------------
# 1. SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Grand Jewelers Sales Tool", page_icon="💎", layout="wide")

# ---------------------------------------------------------
# 2. THE "LUXURY MATRIX" (Specific Links for Every Color)
# ---------------------------------------------------------
def show_luxury_image(product_name, metal_color):
    # We combine the metal and product to find the PERFECT match
    search_key = f"{metal_color} {product_name}"
    
    # THE VAULT: Hand-picked high-quality images for specific metals
    # These are internet links so they ALWAYS look good and correct.
    matrix = {
        # --- ROPE CHAINS ---
        "Yellow Gold Rope Chain": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800",
        "Silver Rope Chain": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800", # Clean Silver
        "White Gold Rope Chain": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800", # Looks like Silver
        "Rose Gold Rope Chain": "https://images.unsplash.com/photo-1599643477877-530eb83d70d2?w=800", # Pink/Warm tone

        # --- FIGARO CHAINS ---
        "Yellow Gold Figaro Chain": "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800",
        "Silver Figaro Chain": "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800?grayscale", # Trick to make it look silver
        "White Gold Figaro Chain": "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800?grayscale",
        "Rose Gold Figaro Chain": "https://images.unsplash.com/photo-1599643477877-530eb83d70d2?w=800", 

        # --- CUBAN LINKS ---
        "Yellow Gold Cuban Link": "https://images.unsplash.com/photo-1600607686527-6fb886090705?w=800",
        "Silver Cuban Link": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800",
        "White Gold Cuban Link": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800",
        "Rose Gold Cuban Link": "https://images.unsplash.com/photo-1599643477877-530eb83d70d2?w=800",

        # --- TENNIS BRACELETS ---
        "Yellow Gold Tennis Bracelet": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800",
        "Silver Tennis Bracelet": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800", # Diamonds look good on silver
        "White Gold Tennis Bracelet": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800",
        "Rose Gold Tennis Bracelet": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800",
        
        # --- STUDS ---
        "Yellow Gold Diamond Studs": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800",
        "Silver Diamond Studs": "https://images.unsplash.com/photo-1630019852942-f89202989a51?w=800",
        "White Gold Diamond Studs": "https://images.unsplash.com/photo-1630019852942-f89202989a51?w=800",
        "Rose Gold Diamond Studs": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800",
    }
    
    # Try to find the exact match. If we can't, default to a high-quality fallback.
    default_image = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800"
    image_url = matrix.get(search_key, default_image)
    
    st.image(image_url, caption=f"Showing: {search_key}", use_container_width=True)

# ---------------------------------------------------------
# 3. SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("💎 Grand Jewelers")
st.sidebar.header("Customer Details")

budget = st.sidebar.selectbox("Budget", ["Under $300", "$300 - $1000", "$1000 - $2500", "$2500 - $5000", "$5000+"])
metal = st.sidebar.selectbox("Metal", ["Yellow Gold", "Silver", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("Style", ["Simple", "Classic", "Trendy", "Iced Out", "Luxury"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Wear", "Gift", "Party/Club", "Wedding/Engagement", "Business/Formal"])

# ---------------------------------------------------------
# 4. LOGIC ENGINE
# ---------------------------------------------------------
product_name = "Rope Chain" # Default Safe Choice
price = "$450"
script = "This is our best seller. It catches the light perfectly."

# --- RULE 1: BUDGET / STUDENT ---
if budget == "Under $300":
    product_name = "Figaro Chain"
    price = "$180 - $280"
    script = "Italian classic. The flat links make it look wider and more expensive than it is."

# --- RULE 2: GIFT ---
elif occasion == "Gift" or occasion == "Wedding/Engagement":
    product_name = "Diamond Studs"
    price = "$250 - $900"
    script = "The #1 gift. Timeless. She will wear these every single day."

# --- RULE 3: ICED OUT / PARTY ---
elif style == "Iced Out" or style == "Trendy":
    product_name = "Cuban Link"
    price = "$850+"
    script = "The ultimate statement. It sits flat on the neck and commands respect."

# --- RULE 4: HIGH BUDGET / LUXURY ---
elif budget == "$2500 - $5000" or budget == "$5000+":
    product_name = "Tennis Bracelet"
    price = "$2,500+"
    script = "Pure luxury. Every inch is covered in diamonds. A true investment piece."

# ---------------------------------------------------------
# 5. DISPLAY
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown(f"### Customer wants: **{metal}**")
    st.markdown("---")
    st.header("Recommended:")
    st.subheader(f"✨ {metal} {product_name}")
    st.write(f"**Est. Price:** {price}")
    
    st.info(f"🗣️ **SAY THIS:** '{script}'")

with col2:
    # PASS THE METAL COLOR TO THE LOADER
    show_luxury_image(product_name, metal)
