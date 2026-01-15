import io
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, List

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

# ✅ Always create assets folder (so you never see “Folder not found”)
ASSETS_DIR = Path(__file__).parent / "assets" / "assets"

ASSETS_DIR.mkdir(exist_ok=True)


@dataclass(frozen=True)
class Product:
    key: str
    title: str
    local_image: str
    fallback_url: str
    talk_track: str
    why_it_fits: str
    add_on: str


# High-quality fallback URLs (only used if your local images are missing)
CATALOG: Dict[str, Product] = {
    "rope_3mm": Product(
        key="rope_3mm",
        title="3mm Rope Chain",
        local_image="rope_chain.jpg",
        fallback_url="https://source.unsplash.com/1600x900/?gold,rope,chain,jewelry",
        talk_track="Best seller. Durable and catches light nicely.",
        why_it_fits="Simple daily chain that looks clean solo or with a pendant. Rope pattern reflects light and hides small scratches well.",
        add_on="Add a small pendant (cross, initial, or coin) + cleaning kit.",
    ),
    "cuban_4mm": Product(
        key="cuban_4mm",
        title="4mm Cuban Link Chain",
        local_image="cuban_chain.jpg",
        fallback_url="https://source.unsplash.com/1600x900/?gold,cuban,chain,jewelry",
        talk_track="Clean, strong, and sits flat—this is the everyday flex chain.",
        why_it_fits="Still simple, but feels more premium than rope/figaro. Great for daily wear because it lays flat and looks bold without being loud.",
        add_on="Match with a Cuban bracelet for a set (bundle deal).",
    ),
    "figaro_3_5mm": Product(
        key="figaro_3_5mm",
        title="3.5mm Figaro Chain",
        local_image="figaro_chain.jpg",
        fallback_url="https://source.unsplash.com/1600x900/?gold,figaro,chain,jewelry",
        talk_track="Italian classic—simple pattern, always in style.",
        why_it_fits="If they want simple and timeless, Figaro is the safe winner. Easy to wear daily, clean look, never goes out of style.",
        add_on="Offer a free clasp upgrade (or cleaning kit) to close today.",
    ),
    "tennis_diamond": Product(
        key="tennis_diamond",
        title="Real Diamond Tennis Bracelet",
        local_image="tennis_bracelet.jpg",
        fallback_url="https://source.unsplash.com/1600x900/?diamond,tennis,bracelet,jewelry",
        talk_track="This is the ‘quiet luxury’ piece—sparkle, but classy and everyday wearable.",
        why_it_fits="High budget + simple style = tennis bracelet. It’s elegant, daily friendly, and looks expensive without trying hard.",
        add_on="Add diamond studs for a matching ‘daily luxury’ set.",
    ),
    "studs_diamond": Product(
        key="studs_diamond",
        title="Diamond Stud Earrings",
        local_image="diamond_studs.jpg",
        fallback_url="https://source.unsplash.com/1600x900/?diamond,stud,earrings,jewelry",
        talk_track="Studs are the #1 forever piece—goes with everything.",
        why_it_fits="For simple daily wear, studs are unbeatable: clean, classic, and always appropriate.",
        add_on="Offer a set: studs + tennis bracelet (bundle + upgrade).",
    ),
}


@st.cache_data(show_spinner=False)
def load_image(local_path: Path, fallback_url: str, title_for_placeholder: str) -> Tuple[Image.Image, str]:
    """
    Returns (image, source_label)
    source_label: "local" | "web" | "placeholder"
    """
    # 1) Try local
    try:
        if local_path.exists():
            return Image.open(local_path).convert("RGB"), "local"
    except Exception:
        pass

    # 2) Try web fallback
    try:
        with urllib.request.urlopen(fallback_url, timeout=6) as resp:
            data = resp.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        return img, "web"
    except Exception:
        pass

    # 3) Placeholder (simple gray)
    img = Image.new("RGB", (1600, 900), (220, 220, 220))
    return img, "placeholder"


def budget_floor(label: str) -> int:
    if label == "Under $300":
        return 0
    if label == "$300–$500":
        return 300
    if label == "$500–$1,000":
        return 500
    if label == "$1,000–$2,500":
        return 1000
    if label == "$2,500–$5,000":
        return 2500
    if label == "$5,000+":
        return 5000
    return 0


def recommend(budget_label: str, metal: str, style: str, occasion: str) -> Product:
    b = budget_floor(budget_label)

    # High budget → diamond daily luxury
    if b >= 5000 and style in {"Simple", "Classic"} and occasion in {"Daily Wear", "Business/Formal"}:
        return CATALOG["tennis_diamond"]

    # Engagement/gift direction
    if occasion in {"Wedding/Engagement", "Gift"} and b >= 1000:
        return CATALOG["studs_diamond"]

    # Mid budget daily chain
    if b >= 1000:
        return CATALOG["cuban_4mm"]

    # Under $300 daily simple gold chain: recommend Figaro as safe winner
    if b < 300 and metal in {"Yellow Gold", "White Gold", "Rose Gold"} and style == "Simple" and occasion == "Daily Wear":
        return CATALOG["figaro_3_5mm"]

    # Default simple classic
    return CATALOG["figaro_3_5mm"]


# ----------------------------
# UI Layout
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

    img_path = ASSETS_DIR / product.local_image
    img, src = load_image(img_path, product.fallback_url, product.title)

    st.image(img, use_container_width=True, caption=product.title)

    if src != "local":
        st.caption(
            f"⚠️ Using **{src}** image. To show your real product photo, upload: `assets/{product.local_image}`"
        )

    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)

    st.markdown("### 🗣️ Sales Script")
    st.success(f"Say this: **“{product.talk_track}”**")

    st.markdown("### ✅ Why this fits")
    st.write(product.why_it_fits)

    st.markdown("### 🔥 Easy add-on to increase ticket")
    st.write(product.add_on)

    expected_files = sorted({p.local_image for p in CATALOG.values()})
    missing: List[str] = [f for f in expected_files if not (ASSETS_DIR / f).exists()]

    with st.expander("📸 Missing Images Checklist (upload these to /assets)"):
        if missing:
            st.write("Missing right now:")
            for f in missing:
                st.code(f"assets/{f}", language="text")
        else:
            st.success("All images found ✅")

st.caption("Tip: Replace placeholder images with your real inventory photos for maximum trust and conversions.")
