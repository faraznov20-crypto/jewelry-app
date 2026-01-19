"""
Grand Jewelers Pentagon City - Sales Tool
UPDATED: Works with existing images + smart fallbacks for Silver/Platinum
"""

import streamlit as st
from pathlib import Path
from PIL import Image

# ---------------------------------------------------------
# 1) PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(
    page_title="Grand Jewelers Pentagon City — Sales Tool",
    page_icon="💎",
    layout="wide"
)

st.title("💎 Grand Jewelers Pentagon City — Sales Tool")
st.markdown("**Professional Product Recommendations**")
st.divider()

# ---------------------------------------------------------
# 2) ASSETS FOLDER (handles assets/ and assets/assets/)
# ---------------------------------------------------------
def get_assets_dir() -> Path:
    """Find assets folder (handles nested assets/assets mistake)"""
    base = Path(__file__).parent
    a = base / "assets"
    b = base / "assets" / "assets"
    
    # Create assets if doesn't exist
    a.mkdir(exist_ok=True)
    
    # Prefer assets/ unless it's empty and assets/assets has files
    if any(a.glob("*.*")):
        return a
    if b.exists() and any(b.glob("*.*")):
        return b
    return a

ASSETS_DIR = get_assets_dir()

# ---------------------------------------------------------
# 3) METAL NAMES WITH SMART FALLBACKS
# ---------------------------------------------------------
METAL_SLUG = {
    "Yellow Gold": "yellow_gold",
    "White Gold": "white_gold",
    "Rose Gold": "rose_gold",
    "Silver": "silver",
    "Platinum": "platinum",
}

# Smart fallback: Silver and Platinum use white_gold images if not available
METAL_FALLBACK = {
    "silver": "white_gold",      # Silver shows white gold if no silver image
    "platinum": "white_gold",    # Platinum shows white gold if no platinum image
}

SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]

# ---------------------------------------------------------
# 4) SMART IMAGE FINDER (with metal fallbacks)
# ---------------------------------------------------------
def find_image(product_key: str, metal_label: str) -> tuple[Path | None, str]:
    """
    Find product image with smart fallback system:
    1. Try {product_key}_{metal}.jpg (exact match)
    2. If Silver/Platinum: Try white_gold version
    3. Try {product_key}.jpg (generic fallback)
    4. Return None if nothing found
    
    Returns: (path, source_description)
    """
    metal_slug = METAL_SLUG.get(metal_label, metal_label.lower().replace(" ", "_"))
    
    candidates = []
    
    # Priority 1: Exact metal-specific image
    for ext in SUPPORTED_EXTENSIONS:
        path = ASSETS_DIR / f"{product_key}_{metal_slug}{ext}"
        if path.exists():
            return path, f"Exact match: {metal_label}"
    
    # Priority 2: Smart fallback for Silver/Platinum → use White Gold
    if metal_slug in METAL_FALLBACK:
        fallback_metal = METAL_FALLBACK[metal_slug]
        for ext in SUPPORTED_EXTENSIONS:
            path = ASSETS_DIR / f"{product_key}_{fallback_metal}{ext}"
            if path.exists():
                return path, f"Using White Gold for {metal_label}"
    
    # Priority 3: Generic product image (no metal suffix)
    for ext in SUPPORTED_EXTENSIONS:
        path = ASSETS_DIR / f"{product_key}{ext}"
        if path.exists():
            return path, "Generic image (no metal)"
    
    return None, "Not found"

# ---------------------------------------------------------
# 5) DISPLAY IMAGE WITH STATUS
# ---------------------------------------------------------
def show_product_image(product_key: str, product_title: str, metal_label: str):
    """Display product image or show what's needed"""
    metal_slug = METAL_SLUG[metal_label]
    perfect_filename = f"{product_key}_{metal_slug}.jpg"
    
    image_path, source = find_image(product_key, metal_label)
    
    if image_path:
        # Image found - display it
        try:
            img = Image.open(image_path)
            st.image(img, caption=f"{metal_label} {product_title}", use_container_width=True)
            
            if "Exact match" in source:
                st.success(f"✅ Perfect! Using: `{image_path.name}`")
            elif "White Gold" in source:
                st.info(f"ℹ️ {source} (showing `{image_path.name}`)")
            else:
                st.warning(f"⚠️ Generic image: `{image_path.name}` (upload `{perfect_filename}` for better match)")
                
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        # Image missing - show instructions
        st.error("❌ **No Image Found**")
        
        st.markdown(f"**Upload ONE of these files to `{ASSETS_DIR.name}/`:**")
        st.code(f"🥇 Best: {perfect_filename}", language="text")
        
        # Show fallback options
        if metal_slug in METAL_FALLBACK:
            fallback = METAL_FALLBACK[metal_slug]
            st.code(f"🥈 OK: {product_key}_{fallback}.jpg (will auto-use for {metal_label})", language="text")
        
        st.code(f"🥉 Minimum: {product_key}.jpg", language="text")

# ---------------------------------------------------------
# 6) PRODUCT CATALOG
# ---------------------------------------------------------
PRODUCTS = {
    "figaro_chain": {
        "title": "3.5mm Figaro Chain",
        "price": "$250-$450",
        "script": "Italian classic — simple pattern, always in style.",
        "why": "Perfect for customers wanting timeless simplicity. Figaro has been a staple for 50+ years.",
        "upsell": "Offer a free clasp upgrade or cleaning kit to close today.",
    },
    "rope_chain": {
        "title": "3mm Rope Chain",
        "price": "$350-$650",
        "script": "Best seller — durable and catches light beautifully.",
        "why": "Rope chains reflect light from every angle and hide scratches better than other styles.",
        "upsell": "Add a small pendant (cross, initial, or coin medallion).",
    },
    "cuban_link": {
        "title": "4mm Cuban Link Chain",
        "price": "$600-$1,200",
        "script": "The ultimate statement chain — sits flat and looks expensive.",
        "why": "Lays flat against chest, looks premium, works daily or for nights out.",
        "upsell": "Bundle with matching Cuban bracelet (15% off set).",
    },
    "iced_chain": {
        "title": "Iced Out Cuban Chain",
        "price": "$1,500-$3,500",
        "script": "This is the statement piece — maximum shine for party nights.",
        "why": "For customers who want to stand out. Full CZ or lab diamond coverage.",
        "upsell": "Add matching iced bracelet for complete set.",
    },
    "tennis_bracelet": {
        "title": "Diamond Tennis Bracelet",
        "price": "$2,000-$6,000",
        "script": "Quiet luxury — sparkle without shouting. This says 'I've made it' with class.",
        "why": "High-budget customers love tennis bracelets for daily luxury. Timeless investment piece.",
        "upsell": "Add diamond studs for matching daily luxury set.",
    },
    "diamond_studs": {
        "title": "Diamond Stud Earrings (1.0 ct tw)",
        "price": "$800-$2,500",
        "script": "Studs are the #1 forever piece — goes with everything, every day.",
        "why": "For simple daily wear, studs are unbeatable: clean, classic, always appropriate.",
        "upsell": "Bundle: studs + chain = complete set (small discount available).",
    },
    "herringbone_chain": {
        "title": "5mm Herringbone Chain",
        "price": "$450-$900",
        "script": "Sleek and sophisticated — lays perfectly flat with unique woven texture.",
        "why": "Great for customers who want something different. Very comfortable to wear.",
        "upsell": "Suggest matching herringbone bracelet for coordinated look.",
    },
    "box_chain": {
        "title": "2.5mm Box Chain",
        "price": "$200-$400",
        "script": "Simple, strong, and affordable — perfect for pendants and everyday wear.",
        "why": "Box chains are incredibly durable and ideal for holding pendants without twisting.",
        "upsell": "Add any pendant from our collection — this chain holds them perfectly.",
    },
}

# ---------------------------------------------------------
# 7) RECOMMENDATION ENGINE
# ---------------------------------------------------------
def recommend(budget: str, metal: str, style: str, occasion: str) -> str:
    """
    Simple, reliable recommendation logic
    Returns product_key
    """
    # Style-based (strongest signal)
    if style == "Iced Out":
        return "iced_chain"
    
    # Budget-based
    if budget == "$5,000+":
        return "tennis_bracelet"
    
    if budget == "$2,500-$5,000":
        if occasion in ["Gift", "Anniversary"]:
            return "diamond_studs"
        return "iced_chain"
    
    if budget == "$1,000-$2,500":
        if occasion in ["Gift", "Anniversary"]:
            return "diamond_studs"
        return "cuban_link"
    
    if budget == "$500-$1,000":
        if occasion == "Party/Club":
            return "cuban_link"
        return "rope_chain"
    
    if budget == "$300-$500":
        return "figaro_chain"
    
    # Under $300
    return "box_chain"

# ---------------------------------------------------------
# 8) USER INTERFACE
# ---------------------------------------------------------

# Left column: Inputs
left_col, right_col = st.columns([1, 2], gap="large")

with left_col:
    st.markdown("### 📋 Customer Profile")
    
    budget = st.selectbox(
        "💰 Budget Range",
        ["Under $300", "$300-$500", "$500-$1,000", "$1,000-$2,500", "$2,500-$5,000", "$5,000+"],
        help="Customer's stated or estimated budget"
    )
    
    metal = st.selectbox(
        "🔶 Metal Preference",
        ["Yellow Gold", "White Gold", "Rose Gold", "Silver", "Platinum"],
        help="Preferred metal color/type"
    )
    
    style = st.selectbox(
        "✨ Style Preference",
        ["Simple", "Classic", "Trendy", "Iced Out", "Luxury"],
        help="Customer's style personality"
    )
    
    occasion = st.selectbox(
        "🎯 Occasion",
        ["Daily Wear", "Gift", "Anniversary", "Party/Club", "Business/Formal"],
        help="What's the jewelry for?"
    )
    
    st.divider()
    
    # Summary
    st.markdown("**Current Selection:**")
    st.caption(f"💰 {budget}")
    st.caption(f"🔶 {metal}")
    st.caption(f"✨ {style}")
    st.caption(f"🎯 {occasion}")

# Get recommendation
product_key = recommend(budget, metal, style, occasion)
product = PRODUCTS[product_key]

# Right column: Recommendation
with right_col:
    st.markdown("## 🎁 Recommended Product")
    st.success(f"**{product['title']}**")
    st.caption(f"💵 Price Range: **{product['price']}**")
    st.write("")
    
    # Display image
    show_product_image(product_key, product['title'], metal)
    
    st.divider()
    
    # Sales information
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🗣️ Sales Script")
        st.info(f'**Say this:**\n\n"{product["script"]}"')
    
    with col_b:
        st.markdown("### ✅ Why This Works")
        st.success(product["why"])
    
    st.markdown("### 🔥 Upsell Strategy")
    st.warning(f"**Add-on opportunity:** {product['upsell']}")

# ---------------------------------------------------------
# 9) IMAGE UPLOAD GUIDE (expandable)
# ---------------------------------------------------------
st.divider()

with st.expander("📸 What Images Do I Need? (Smart Guide)"):
    st.markdown(f"### Current Status: Upload to `{ASSETS_DIR.name}/`")
    st.write("")
    
    # Check what exists
    st.markdown("#### ✅ Your Current Images:")
    
    found_images = []
    for file in ASSETS_DIR.glob("*.*"):
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            found_images.append(file.name)
    
    if found_images:
        for img in sorted(found_images):
            st.text(f"✓ {img}")
    else:
        st.warning("No images found yet!")
    
    st.markdown("---")
    st.markdown("#### 💡 Smart Image System:")
    st.write("")
    
    st.info("""
    **How it works:**
    - If you have `rope_chain_yellow_gold.jpg` → Shows for Yellow Gold ✅
    - If you select Silver but only have `rope_chain_white_gold.jpg` → Shows White Gold image ✅
    - If you select Platinum but only have `rope_chain_white_gold.jpg` → Shows White Gold image ✅
    - If you only have `rope_chain.jpg` → Shows for all metals ✅
    """)
    
    st.markdown("#### 📋 Upload Priority:")
    
    st.markdown("**🥇 You Already Have (from screenshots):**")
    st.code("""
rope_chain_yellow_gold.jpg
cuban_link_yellow_gold.jpg
tennis_bracelet_yellow_gold.jpg
... (and more yellow gold)
    """, language="text")
    
    st.markdown("**🥈 To Add Now (for Rose Gold):**")
    st.code("""
rope_chain_rose_gold.jpg
cuban_link_rose_gold.jpg
figaro_chain_rose_gold.jpg
tennis_bracelet_rose_gold.jpg
diamond_studs_rose_gold.jpg
herringbone_chain_rose_gold.jpg
box_chain_rose_gold.jpg
iced_chain_rose_gold.jpg
    """, language="text")
    
    st.markdown("**🥉 Optional (White Gold covers Silver + Platinum):**")
    st.code("""
rope_chain_white_gold.jpg  ← Will show for Silver & Platinum too!
cuban_link_white_gold.jpg  ← Will show for Silver & Platinum too!
... (same for all products)
    """, language="text")
    
    st.success("""
    **💡 Smart Tip:** 
    You don't need separate Silver and Platinum images! 
    Just upload White Gold versions and they'll automatically show for Silver/Platinum selections.
    """)

# Footer
st.divider()
st.caption("💎 Grand Jewelers Pentagon City | Sales Tool | Smart metal fallback system enabled")
