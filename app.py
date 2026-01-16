import streamlit as st
from PIL import Image
import os
import requests
from io import BytesIO

# ---------------------------------------------------------
# 1. SETUP & CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Grand Jewelers Sales Tool", page_icon="💎", layout="wide")

# Custom CSS for that "Luxury" feel
st.markdown("""
    <style>
    .stApp {background-color: #ffffff;}
    div[data-testid="stVerticalBlock"] {gap: 1rem;}
    .css-1y4p8pa {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. THE "WORLD BEST PICTURES" VAULT (Internet Backups)
# ---------------------------------------------------------
# If local files are missing, the app uses these HD links automatically.
LUXURY_LINKS = {
    # ROPE CHAINS
    "rope_chain_yellow": "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=800&q=80",
    "rope_chain_white": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&q=80",
    "rope_chain_rose": "https://images.unsplash.com/photo-1599643477877-530eb83d70d2?w=800&q=80",
    
    # CUBAN LINKS
    "cuban_chain_yellow": "https://images.unsplash.com/photo-1600607686527-6fb886090705?w=800&q=80",
    "cuban_chain_white": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&q=80",
    "cuban_chain_rose": "https://images.unsplash.com/photo-1599643477877-530eb83d70d2?w=800&q=80",

    # FIGARO
    "figaro_chain_yellow": "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800&q=80",
    
    # TENNIS BRACELETS
    "tennis_bracelet_white": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&q=80",
    "tennis_bracelet_yellow": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&q=80",

    # STUDS
    "diamond_studs_white": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&q=80",
    
    # NEW ITEMS (From the other AI's suggestion)
    "herringbone_chain": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&q=80", # Sleek look
    "box_chain": "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=800&q=80", # Classic look
    "iced_chain": "https://images.unsplash.com/photo-1599643478518-17488fbbcd75?w=800&q=80",
}

# ---------------------------------------------------------
# 3. THE "HYBRID" IMAGE LOADER (Smart Search)
# ---------------------------------------------------------
def load_image(base_name, metal_slug):
    # 1. Construct target filenames
    specific_file = f"{base_name}_{metal_slug}.jpg"
    generic_file = f"{base_name}.jpg"
    
    # 2. Check Local Files (In every possible folder to fix your bug)
    possible_paths = [
        f"assets/assets/{specific_file}", # Fixes your double folder issue
        f"assets/{specific_file}",
        specific_file,
        f"assets/assets/{generic_file}",
        f"assets/{generic_file}",
        generic_file
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return Image.open(path), "Local File Found ✅"

    # 3. If Local fails, use Internet (Luxury Link Vault)
    # Try specific metal first, then generic
    url_key_specific = f"{base_name}_{metal_slug}"
    url_key_generic = base_name
    
    url = LUXURY_LINKS.get(url_key_specific, LUXURY_LINKS.get(url_key_generic))
    
    if url:
        return url, "Web Image Loaded 🌐"
        
    # 4. Total Failure Fallback
    return "https://placehold.co/800x600?text=No+Image", "Missing"

# ---------------------------------------------------------
# 4. APP LOGIC
# ---------------------------------------------------------
st.title("💎 Grand Jewelers Sales Tool")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### Customer Details")
    budget = st.selectbox("Budget", ["Under $300", "$300 - $1,000", "$1,000 - $3,000", "$3,000 - $5,000", "$5,000+"])
    metal = st.selectbox("Metal Preference", ["Yellow Gold", "White Gold", "Rose Gold", "Silver", "Platinum"])
    style = st.selectbox("Style", ["Simple", "Classic", "Trendy", "Iced Out", "Luxury"])
    occasion = st.selectbox("Occasion", ["Daily Wear", "Gift", "Wedding/Engagement", "Party/Club"])
    
    st.divider()
    st.caption(f"**Selection:** {budget} | {metal} | {style}")

# --- RECOMMENDATION ENGINE ---
# This converts the text "Yellow Gold" into "yellow" for the code
metal_code = "yellow"
if "White" in metal or "Silver" in metal or "Platinum" in metal: metal_code = "white"
elif "Rose" in metal: metal_code = "rose"

# Logic Rules
if budget == "Under $300":
    if style == "Simple":
        product = "Box Chain"
        file_key = "box_chain"
        desc = "A strong, classic box chain. Perfect for daily wear."
    else:
        product = "Figaro Chain"
        file_key = "figaro_chain"
        desc = "Italian classic. Gives a great look for the price."

elif budget == "$300 - $1,000":
    if style == "Iced Out" or occasion == "Party/Club":
        product = "Iced Cuban Link"
        file_key = "iced_chain"
        desc = "Maximum shine. Lab diamonds that hit the light perfectly."
    else:
        product = "Rope Chain"
        file_key = "rope_chain"
        desc = "Our #1 Best Seller. Diamond-cut finish sparkles without stones."

elif budget == "$1,000 - $3,000":
    if style == "Trendy":
        product = "Miami Cuban Link"
        file_key = "cuban_chain"
        desc = "The heavy hitter. Solid feel, lays flat on the chest."
    else:
        product = "Herringbone Chain"
        file_key = "herringbone_chain"
        desc = "Liquid gold. Moves like silk on the skin."

elif budget == "$3,000 - $5,000" or budget == "$5,000+":
    if occasion == "Wedding/Engagement" or occasion == "Gift":
        product = "Diamond Studs (2ct)"
        file_key = "diamond_studs"
        desc = "Certified VS Diamonds. The ultimate forever gift."
    else:
        product = "Tennis Bracelet"
        file_key = "tennis_bracelet"
        desc = "The definition of luxury. Diamonds all the way around."

# --- DISPLAY RESULT ---
with col2:
    st.subheader("Recommended Item")
    st.markdown(f"## ✨ {product}")
    
    # LOAD IMAGE (Auto-detects Local vs Web)
    image_data, source_type = load_image(file_key, metal_code)
    
    if isinstance(image_data, str): # It's a URL
        st.image(image_data, use_container_width=True)
    else: # It's a local file
        st.image(image_data, use_container_width=True)
        
    st.caption(f"Status: {source_type}")
    
    st.markdown("### 🗣️ Sales Script")
    st.info(f"**Say this:** \"{desc}\"")
    
    st.markdown("### ✅ Why it fits")
    st.write(f"Matches the **{budget}** budget and **{style}** style preference perfectly in **{metal}**.")
