import io
import urllib.request, urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, List

import streamlit as st
from PIL import Image

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="Grand Jewelers Pentagon City — Sales Tool",
    page_icon="💎",
    layout="wide",
)

st.markdown(
    """
    <style>
      .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
      .gj-card {
        border: 1px solid #e6e6e6;
        border-radius: 14px;
        padding: 16px;
        background: white;
      }
      .gj-pill {
        background: #e9f8ee;
        color: #0f6a2a;
        border-radius: 10px;
        padding: 10px 12px;
        font-weight: 600;
        width: 100%;
        display: inline-block;
      }
      .gj-muted { color: #6b7280; }
      .gj-hr { border-top: 1px solid #eee; margin: 18px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create assets folder
ASSETS_DIR = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

# ----------------------------
# Helper for metals
# ----------------------------
METAL_SLUG = {
    "Yellow Gold": "yellow",
    "White Gold": "white",
    "Rose Gold": "rose",
    "Silver": "silver",
    "Platinum": "platinum",
}

# ----------------------------
# Product class
# ----------------------------
@dataclass(frozen=True)
class Product:
    key: str
    title: str
    local_image: str
    talk_track: str
    why_it_fits: str
    add_on: str

# ----------------------------
# Product catalog
# ----------------------------
CATALOG: Dict[str, Product] = {
    "rope_3mm": Product(
        key="rope_3mm",
        title="3mm Rope Chain",
        local_image="rope_chain.jpg",
        talk_track="Best seller. Durable and catches light nicely.",
        why_it_fits="Simple daily chain that looks clean solo or with a pendant. Rope pattern reflects light and hides scratches well.",
        add_on="Add a small pendant (cross or initial) + cleaning kit.",
    ),
    "cuban_4mm": Product(
        key="cuban_4mm",
        title="4mm Cuban Link Chain",
        local_image="cuban_chain.jpg",
        talk_track="Clean, strong, and sits flat—this is the everyday flex chain.",
        why_it_fits="Still simple, but feels more premium. Great for daily wear because it lays flat and looks bold without being loud.",
        add_on="Match with a Cuban bracelet for a set.",
    ),
    "figaro_3_5mm": Product(
        key="figaro_3_5mm",
        title="3.5mm Figaro Chain",
        local_image="figaro_chain.jpg",
        talk_track="Italian classic—simple pattern, always in style.",
        why_it_fits="Timeless, daily, clean look. Never goes out of style.",
        add_on="Offer clasp upgrade or cleaning kit.",
    ),
    "tennis_diamond": Product(
        key="tennis_diamond",
        title="Diamond Tennis Bracelet",
        local_image="tennis_bracelet.jpg",
        talk_track="Quiet luxury—sparkle but classy.",
        why_it_fits="Elegant, wearable daily, looks expensive without trying hard.",
        add_on="Add diamond studs for matching daily luxury.",
    ),
    "studs_diamond": Product(
        key="studs_diamond",
        title="Diamond Stud Earrings",
        local_image="diamond_studs.jpg",
        talk_track="Studs are the forever piece—goes with everything.",
        why_it_fits="For daily wear, studs are unbeatable: clean, classic, appropriate.",
        add_on="Offer studs + tennis bracelet set.",
    ),
}

# ----------------------------
# Choose metal-specific file
# ----------------------------
def best_local_image_filename(product: Product, metal: str) -> str:
    slug = METAL_SLUG.get(metal, "generic")
    base = Path(product.local_image).stem
    ext = Path(product.local_image).suffix
    metal_file = f"{base}_{slug}{ext}"
    if (ASSETS_DIR / metal_file).exists():
        return metal_file
    return product.local_image

# ----------------------------
# Load image (cache-safe)
# ----------------------------
@st.cache_data(show_spinner=False)
def load_image(local_path_str: str, fallback_url: str, file_mtime: float) -> Tuple[Image.Image, str]:
    local_path = Path(local_path_str)

    try:
        if local_path.exists():
            return Image.open(local_path).convert("RGB"), "local"
    except Exception:
        pass

    try:
        with urllib.request.urlopen(fallback_url, timeout=6) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        return img, "web"
    except Exception:
        pass

    img = Image.new("RGB", (1600, 900), (220, 220, 220))
    return img, "placeholder"

# ----------------------------
# Budget helper
# ----------------------------
def budget_floor(label: str) -> int:
    if label == "Under $300": return 0
    if label == "$300–$500": return 300
    if label == "$500–$1,000": return 500
    if label == "$1,000–$2,500": return 1000
    if label == "$2,500–$5,000": return 2500
    if label == "$5,000+": return 5000
    return 0

# ----------------------------
# Recommend logic
# ----------------------------
def recommend(budget_label: str, metal: str, style: str, occasion: str) -> Product:
    b = budget_floor(budget_label)

    if b >= 5000 and style in {"Simple", "Classic"}:
        return CATALOG["tennis_diamond"]

    if occasion in {"Wedding/Engagement", "Gift"} and b >= 1000:
        return CATALOG["studs_diamond"]

    if style in {"Trendy", "Iced Out"} and b >= 1000:
        return CATALOG["cuban_4mm"]

    if b < 300:
        return CATALOG["figaro_3_5mm"]

    return CATALOG["rope_3mm"]

# ----------------------------
# UI
# ----------------------------
left, right = st.columns([1, 2.2], gap="large")

with left:
    st.markdown('<div class="gj-card">', unsafe_allow_html=True)
    st.subheader("Customer Details")

    budget = st.selectbox("Budget", ["Under $300", "$300–$500", "$500–$1,000", "$1,000–$2,500", "$2,500–$5,000", "$5,000+"])
    metal = st.selectbox("Metal", ["Yellow Gold", "White Gold", "Rose Gold", "Silver", "Platinum"])
    style = st.selectbox("Style", ["Simple", "Classic", "Trendy", "Iced Out", "Luxury"])
    occasion = st.selectbox("Occasion", ["Daily Wear", "Gift", "Wedding/Engagement", "Party/Club", "Business/Formal"])

    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)
    st.markdown("**💎 Grand Jewelers Pentagon City — Sales Tool**")
    st.caption(f"Budget: {budget} | Metal: {metal} | Style: {style} | Occasion: {occasion}")
    st.markdown("</div>", unsafe_allow_html=True)

product = recommend(budget, metal, style, occasion)

with right:
    st.markdown("## Recommended Item:")
    st.markdown(f'<div class="gj-pill">{product.title}</div>', unsafe_allow_html=True)
    st.write("")

    img_file = best_local_image_filename(product, metal)
    img_path = ASSETS_DIR / img_file
    query = urllib.parse.quote_plus(f"{metal} {product.title} jewelry luxury")
    fallback_url = f"https://source.unsplash.com/1600x900/?{query}"

    mtime = img_path.stat().st_mtime if img_path.exists() else 0
    img, src = load_image(str(img_path), fallback_url, mtime)
    st.image(img, use_container_width=True, caption=product.title)

    if src != "local":
        st.caption(f"⚠️ Using {src} image. Upload: `assets/{img_file}` for your real photo.")

    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)
    st.markdown("### 🗣️ Sales Script")
    st.success(f"Say this: “{product.talk_track}”")

    st.markdown("### ✅ Why this fits")
    st.write(product.why_it_fits)

    st.markdown("### 🔥 Easy add-on to increase ticket")
    st.write(product.add_on)

    expected_files = sorted({p.local_image for p in CATALOG.values()})
    missing: List[str] = [f for f in expected_files if not (ASSETS_DIR / f).exists()]
    with st.expander("📸 Missing Images Checklist"):
        if missing:
            st.write("Missing right now:")
            for f in missing:
                st.code(f"assets/{f}", language="text")
        else:
            st.success("All images found ✅")

st.caption("Tip: Replace placeholder photos with your real jewelry shots for luxury impact.")
