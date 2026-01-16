import streamlit as st
from pathlib import Path
from PIL import Image

# ---------------------------------------------------------
# 1) SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Grand Jewelers Pentagon City — Sales Tool", page_icon="💎", layout="wide")
st.title("💎 Grand Jewelers Pentagon City — Sales Tool")

# ---------------------------------------------------------
# 2) ASSETS (handles assets/ and assets/assets/)
# ---------------------------------------------------------
def get_assets_dir() -> Path:
    base = Path(__file__).parent
    a = base / "assets"
    b = base / "assets" / "assets"
    a.mkdir(exist_ok=True)
    # Prefer assets/ unless it's empty and assets/assets has files
    if any(a.glob("*.*")):
        return a
    if b.exists() and any(b.glob("*.*")):
        return b
    return a

ASSETS_DIR = get_assets_dir()

# ---------------------------------------------------------
# 3) SMART MATCH IMAGE LOADER (THE OWNERSHIP UPGRADE)
# ---------------------------------------------------------
METAL_SLUG = {
    "Yellow Gold": "yellow_gold",
    "White Gold": "white_gold",
    "Rose Gold": "rose_gold",
    "Silver": "silver",
    "Platinum": "platinum",
}

EXTS = [".jpg", ".jpeg", ".png", ".webp"]

def find_image(product_key: str, metal_label: str) -> Path | None:
    metal = METAL_SLUG.get(metal_label, metal_label.lower().replace(" ", "_"))
    candidates = []

    # 1) Perfect match: product_metal.ext
    for ext in EXTS:
        candidates.append(ASSETS_DIR / f"{product_key}_{metal}{ext}")

    # 2) Fallback: product.ext
    for ext in EXTS:
        candidates.append(ASSETS_DIR / f"{product_key}{ext}")

    # 3) Also check repo root, just in case
    base = Path(__file__).parent
    for ext in EXTS:
        candidates.append(base / f"{product_key}_{metal}{ext}")
        candidates.append(base / f"{product_key}{ext}")

    for p in candidates:
        if p.exists():
            return p
    return None

def show_exact_image(product_key: str, product_title: str, metal_label: str):
    wanted = f"{product_key}_{METAL_SLUG[metal_label]}.jpg"
    p = find_image(product_key, metal_label)

    if p:
        st.image(Image.open(p), caption=f"{metal_label} {product_title}", use_container_width=True)
        st.success(f"✅ Using: {p.name}")
    else:
        st.warning(f"⚠️ MISSING PHOTO: Upload **{wanted}** into `{ASSETS_DIR.name}/`")
        st.info("Tip: You can also upload a fallback like `product.jpg` (example: `rope_chain.jpg`).")

# ---------------------------------------------------------
# 4) PRODUCT CATALOG (keys MUST match filenames)
# ---------------------------------------------------------
PRODUCTS = {
    "figaro_chain": {
        "title": "Figaro Chain",
        "script": "Italian classic. Simple pattern, always in style.",
    },
    "rope_chain": {
        "title": "Rope Chain",
        "script": "Best-seller. Durable and shines like crazy under light.",
    },
    "cuban_link": {
        "title": "Cuban Link",
        "script": "The ultimate statement chain. Sits flat and looks expensive.",
    },
    "tennis_bracelet": {
        "title": "Tennis Bracelet",
        "script": "Pure luxury. Diamonds all the way around — timeless.",
    },
    "diamond_studs": {
        "title": "Diamond Studs",
        "script": "The #1 gift. Matches everything and never goes out of style.",
    },
}

# ---------------------------------------------------------
# 5) SIDEBAR INPUTS
# ---------------------------------------------------------
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("Budget", ["Under $300", "$300 - $1000", "$1000+", "$5000+"])
metal = st.sidebar.selectbox("Metal", ["Yellow Gold", "White Gold", "Silver", "Rose Gold", "Platinum"])
style = st.sidebar.selectbox("Style", ["Simple", "Classic", "Iced Out"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Wear", "Gift", "Special Event"])

# ---------------------------------------------------------
# 6) RECOMMENDATION LOGIC (simple + reliable)
# ---------------------------------------------------------
product_key = "rope_chain"

if budget == "Under $300":
    product_key = "figaro_chain"
elif occasion == "Gift" and budget == "Under $300":
    product_key = "diamond_studs"
elif style == "Iced Out":
    product_key = "cuban_link"
elif budget in ["$1000+", "$5000+"]:
    product_key = "tennis_bracelet"

product = PRODUCTS[product_key]

# ---------------------------------------------------------
# 7) DISPLAY
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown(f"### Recommending: **{metal} {product['title']}**")
    st.info(f"🗣️ **SAY THIS:** “{product['script']}”")

with col2:
    show_exact_image(product_key, product["title"], metal)

# ---------------------------------------------------------
# 8) SHOPPING LIST (shows exactly what you must upload)
# ---------------------------------------------------------
with st.expander("📸 Missing Photo Shopping List"):
    needed = []
    for key in PRODUCTS.keys():
        for metal_label, slug in METAL_SLUG.items():
            needed.append(f"{key}_{slug}.jpg")

    st.write(f"Upload into: `{ASSETS_DIR.name}/`")
    st.caption("Start with the products you sell most. Add more over time.")
    st.code("\n".join(needed[:25]) + "\n...\n", language="text")
