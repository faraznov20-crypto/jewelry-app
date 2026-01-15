# app.py  ✅ FINAL (with all fixes)
# What this version fixes:
# 1) Uses DIFFERENT photos for Yellow/White/Rose/Silver/Platinum (if you upload them)
# 2) No more “old cached image” problem when you replace photos
# 3) Works even if you accidentally made assets/assets folder
# 4) Stops using random “ugly” web photos (shows a clean placeholder until you upload real photos)

import io
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, Dict, List

import streamlit as st
from PIL import Image, ImageDraw, ImageFont


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
      .small-note { font-size: 0.92rem; color: #6b7280; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Assets folder (fix assets/assets mistake)
# ----------------------------
APP_DIR = Path(__file__).parent
ASSETS_A = APP_DIR / "assets"
ASSETS_B = APP_DIR / "assets" / "assets"

def folder_has_images(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any(folder.glob("*.jpg")) or any(folder.glob("*.jpeg")) or any(folder.glob("*.png"))

# If user accidentally made assets/assets and put images there, use it.
if folder_has_images(ASSETS_B) and not folder_has_images(ASSETS_A):
    ASSETS_DIR = ASSETS_B
else:
    ASSETS_DIR = ASSETS_A

ASSETS_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Data
# ----------------------------
@dataclass(frozen=True)
class Product:
    key: str
    title: str
    base_image: str  # base image name (example: "cuban_chain.jpg")  -> you can also upload metal versions
    talk_track: str
    why_it_fits: str
    add_on: str


CATALOG: Dict[str, Product] = {
    "rope_3mm": Product(
        key="rope_3mm",
        title="3mm Rope Chain",
        base_image="rope_chain.jpg",
        talk_track="Best seller. Durable and catches light nicely.",
        why_it_fits="Simple daily chain that looks clean solo or with a pendant. Rope reflects light and hides small scratches well.",
        add_on="Add a small pendant (cross, initial, or coin) + cleaning kit.",
    ),
    "cuban_4mm": Product(
        key="cuban_4mm",
        title="4mm Cuban Link Chain",
        base_image="cuban_chain.jpg",
        talk_track="Clean, strong, and sits flat—this is the everyday flex chain.",
        why_it_fits="Simple but premium. Great daily wear because it lays flat and looks bold without being loud.",
        add_on="Match with a Cuban bracelet for a set (bundle deal).",
    ),
    "figaro_3_5mm": Product(
        key="figaro_3_5mm",
        title="3.5mm Figaro Chain",
        base_image="figaro_chain.jpg",
        talk_track="Italian classic—simple pattern, always in style.",
        why_it_fits="If they want simple and timeless, Figaro is the safe winner. Easy daily wear, clean look, never goes out of style.",
        add_on="Offer a free clasp upgrade (or cleaning kit) to close today.",
    ),
    "tennis_diamond": Product(
        key="tennis_diamond",
        title="Real Diamond Tennis Bracelet",
        base_image="tennis_bracelet.jpg",
        talk_track="This is quiet luxury—sparkle, but classy and everyday wearable.",
        why_it_fits="High budget + simple style = tennis bracelet. Elegant, daily friendly, and looks expensive without trying hard.",
        add_on="Add diamond studs for a matching daily-luxury set.",
    ),
    "studs_diamond": Product(
        key="studs_diamond",
        title="Diamond Stud Earrings",
        base_image="diamond_studs.jpg",
        talk_track="Studs are the #1 forever piece—goes with everything.",
        why_it_fits="For simple daily wear, studs are unbeatable: clean, classic, always appropriate.",
        add_on="Offer a set: studs + tennis bracelet (bundle + upgrade).",
    ),
}

# ----------------------------
# Simple helpers
# ----------------------------
METAL_SLUG = {
    "Yellow Gold": "yellow",
    "White Gold": "white",
    "Rose Gold": "rose",
    "Silver": "silver",
    "Platinum": "platinum",
}

STYLE_SLUG = {
    "Simple": "simple",
    "Classic": "classic",
    "Trendy": "trendy",
    "Iced Out": "iced",
    "Luxury": "luxury",
}

OCCASION_SLUG = {
    "Daily Wear": "daily",
    "Gift": "gift",
    "Wedding/Engagement": "wedding",
    "Party/Club": "party",
    "Business/Formal": "business",
}

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

    # Diamonds for high budget
    if b >= 5000:
        if occasion in {"Wedding/Engagement", "Gift"}:
            return CATALOG["studs_diamond"]
        return CATALOG["tennis_diamond"]

    # “Iced Out” (even mid budget) → push studs as “sparkle piece”
    if style == "Iced Out" and b >= 1000:
        return CATALOG["studs_diamond"]

    # Mid budget daily chain
    if b >= 1000:
        return CATALOG["cuban_4mm"]

    # Under $300 daily simple → Figaro safe winner
    if b < 300 and style == "Simple" and occasion == "Daily Wear":
        return CATALOG["figaro_3_5mm"]

    # Default
    return CATALOG["figaro_3_5mm"]


def make_placeholder(w: int, h: int, big_text: str, small_text: str) -> Image.Image:
    """Simple clean placeholder (not ugly random web photos)."""
    img = Image.new("RGB", (w, h), (235, 235, 235))
    draw = ImageDraw.Draw(img)

    # Try a default font (works on most systems)
    try:
        font_big = ImageFont.truetype("arial.ttf", 52)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Center big text
    bx, by = draw.textbbox((0, 0), big_text, font=font_big)[2:]
    sx, sy = draw.textbbox((0, 0), small_text, font=font_small)[2:]

    draw.text(((w - bx) / 2, (h * 0.42) - 40), big_text, fill=(50, 50, 50), font=font_big)
    draw.text(((w - sx) / 2, (h * 0.58)), small_text, fill=(90, 90, 90), font=font_small)

    return img


def image_candidates(product: Product, metal: str, style: str, occasion: str) -> List[str]:
    """
    We try these names in this order (best -> ok -> fallback).
    You only need to upload what you want.
    """
    metal_s = METAL_SLUG.get(metal, "generic")
    style_s = STYLE_SLUG.get(style, "any")
    occ_s = OCCASION_SLUG.get(occasion, "any")

    base = Path(product.base_image).stem   # "cuban_chain"
    ext = Path(product.base_image).suffix  # ".jpg"

    return [
        f"{base}_{metal_s}_{style_s}_{occ_s}{ext}",  # super specific
        f"{base}_{metal_s}_{style_s}{ext}",          # metal + style
        f"{base}_{metal_s}{ext}",                    # metal only
        product.base_image,                          # generic
    ]


@st.cache_data(show_spinner=False)
def load_local_image(path_str: str, file_mtime: float, want_name: str) -> Tuple[Image.Image, str]:
    """
    Cache-safe:
    - file_mtime changes when you replace the image
    - so Streamlit shows the new photo (no old cached photo)
    """
    p = Path(path_str)
    if p.exists():
        try:
            return Image.open(p).convert("RGB"), "local"
        except Exception:
            pass

    # Placeholder if missing/broken image
    img = make_placeholder(
        1600,
        900,
        big_text="UPLOAD PHOTO",
        small_text=f"assets/{want_name}",
    )
    return img, "placeholder"


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

    # pick best image file name (metal/style/occasion)
    candidates = image_candidates(product, metal, style, occasion)

    chosen_name = None
    chosen_path = None
    for name in candidates:
        p = ASSETS_DIR / name
        if p.exists():
            chosen_name = name
            chosen_path = p
            break

    # If nothing exists, use first candidate (most specific) so placeholder tells you exactly what to upload
    if chosen_name is None:
        chosen_name = candidates[0]
        chosen_path = ASSETS_DIR / chosen_name

    mtime = chosen_path.stat().st_mtime if chosen_path.exists() else 0
    img, src = load_local_image(str(chosen_path), mtime, chosen_name)

    st.image(img, use_container_width=True, caption=product.title)

    if src != "local":
        st.warning("Photo not found yet. Upload a real product photo so it looks premium.")
        st.markdown(f"<div class='small-note'>Upload file name: <b>assets/{chosen_name}</b></div>", unsafe_allow_html=True)

    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)

    st.markdown("### 🗣️ Sales Script")
    st.success(f"Say this: **“{product.talk_track}”**")

    st.markdown("### ✅ Why this fits")
    st.write(product.why_it_fits)

    st.markdown("### 🔥 Easy add-on to increase ticket")
    st.write(product.add_on)

    with st.expander("📸 Image names this product can use (upload any of these)"):
        st.write("Best → OK → fallback. The app will pick the first file it finds.")
        for name in candidates:
            st.code(f"assets/{name}", language="text")

st.caption("Tip: Use real iPhone photos + lightbox for premium look. Replace banner graphics with real product photos.")
