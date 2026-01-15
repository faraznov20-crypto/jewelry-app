import io
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

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

APP_DIR = Path(__file__).parent
ASSETS_DIR = APP_DIR / "assets"


# ----------------------------
# Helpers
# ----------------------------
def make_placeholder(title: str, subtitle: str = "Upload your real photo to assets/") -> Image.Image:
    """Creates a clean luxury-style placeholder image."""
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), (245, 245, 245))
    draw = ImageDraw.Draw(img)

    # Simple frame
    margin = 40
    draw.rectangle([margin, margin, w - margin, h - margin], outline=(210, 210, 210), width=6)

    # Text (safe default font)
    try:
        font_title = ImageFont.truetype("DejaVuSans.ttf", 64)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 36)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Center title
    tw, th = draw.textbbox((0, 0), title, font=font_title)[2:]
    draw.text(((w - tw) / 2, h * 0.42), title, fill=(90, 90, 90), font=font_title)

    # Subtitle
    sw, sh = draw.textbbox((0, 0), subtitle, font=font_sub)[2:]
    draw.text(((w - sw) / 2, h * 0.55), subtitle, fill=(120, 120, 120), font=font_sub)

    # Brand tag
    brand = "Grand Jewelers Pentagon City"
    bw, bh = draw.textbbox((0, 0), brand, font=font_sub)[2:]
    draw.text(((w - bw) / 2, h * 0.80), brand, fill=(110, 110, 110), font=font_sub)

    return img


def load_product_image(filename: str, fallback_url: Optional[str], title: str) -> Image.Image:
    """Try local asset image, else fallback URL, else generated placeholder."""
    local_path = ASSETS_DIR / filename

    # 1) Local
    if local_path.exists():
        try:
            return Image.open(local_path).convert("RGB")
        except Exception:
            pass

    # 2) Fallback URL (optional)
    if fallback_url:
        try:
            with urllib.request.urlopen(fallback_url, timeout=6) as resp:
                data = resp.read()
            return Image.open(io.BytesIO(data)).convert("RGB")
        except Exception:
            pass

    # 3) Placeholder
    return make_placeholder(title)


# ----------------------------
# Data
# ----------------------------
@dataclass
class Product:
    key: str
    title: str
    local_image: str
    fallback_url: Optional[str]
    talk_track: str
    why_it_fits: str
    add_on: str


PRODUCTS: Dict[str, Product] = {
    "figaro_35": Product(
        key="figaro_35",
        title="3.5mm Figaro Chain",
        local_image="figaro_chain.jpg",
        fallback_url=None,
        talk_track="Italian classic — simple pattern, always in style.",
        why_it_fits="Simple + daily wear = Figaro is the safe winner. Clean, timeless, easy to wear every day.",
        add_on="Offer a free clasp check + cleaning kit to close today.",
    ),
    "rope_3": Product(
        key="rope_3",
        title="3mm Rope Chain",
        local_image="rope_chain.jpg",
        fallback_url=None,
        talk_track="Best seller. Durable and catches light nicely.",
        why_it_fits="Rope chains shine in normal light, feel solid, and work with any outfit daily.",
        add_on="Add a small pendant or extend warranty/cleaning kit.",
    ),
    "cuban_5": Product(
        key="cuban_5",
        title="5mm Cuban Chain",
        local_image="cuban_chain.jpg",
        fallback_url=None,
        talk_track="Bold but still wearable — this is the ‘confidence chain’.",
        why_it_fits="If they want simple but stronger presence, Cuban is clean, heavy-looking, and daily friendly.",
        add_on="Upgrade clasp (box lock) or add matching bracelet.",
    ),
    "studs_diamond": Product(
        key="studs_diamond",
        title="Diamond Stud Earrings",
        local_image="diamond_studs.jpg",
        fallback_url=None,
        talk_track="Studs are the #1 forever piece — goes with everything.",
        why_it_fits="For simple daily wear, studs are unbeatable: clean, classic, always appropriate.",
        add_on="Bundle: studs + chain = easy set (small discount or free cleaning kit).",
    ),
    "tennis_real": Product(
        key="tennis_real",
        title="Real Diamond Tennis Bracelet",
        local_image="tennis_bracelet.jpg",
        fallback_url=None,
        talk_track="Quiet luxury — sparkle, but classy and everyday wearable.",
        why_it_fits="High budget + simple style = tennis bracelet. Looks expensive without trying hard.",
        add_on="Add diamond studs for a matching daily luxury set.",
    ),
}


def recommend(budget: str, metal: str, style: str, occasion: str) -> Product:
    """Simple rule-based recommendation."""
    # Big spend → tennis
    if budget in ["$3000-$5000", "$5000+"]:
        return PRODUCTS["tennis_real"]

    # Gift / special → studs
    if occasion in ["Gift", "Anniversary"] and budget != "Under $300":
        return PRODUCTS["studs_diamond"]

    # Daily wear simple → chain based on budget
    if occasion == "Daily Wear" and style == "Simple":
        if budget == "Under $300":
            return PRODUCTS["figaro_35"]
        if budget in ["$300-$500", "$500-$1000"]:
            return PRODUCTS["rope_3"]
        return PRODUCTS["cuban_5"]

    # Default fallback
    if budget == "Under $300":
        return PRODUCTS["figaro_35"]
    return PRODUCTS["rope_3"]


# ----------------------------
# UI
# ----------------------------
st.title("💎 Grand Jewelers Pentagon City — Sales Tool")

left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader("Customer Details")

    budget = st.selectbox(
        "Budget",
        ["Under $300", "$300-$500", "$500-$1000", "$1000-$3000", "$3000-$5000", "$5000+"],
        index=0,
    )

    metal = st.selectbox("Metal", ["Yellow Gold", "White Gold", "Rose Gold"], index=0)
    style = st.selectbox("Style", ["Simple", "Iced", "Luxury"], index=0)
    occasion = st.selectbox("Occasion", ["Daily Wear", "Gift", "Party/Night Out", "Anniversary"], index=0)

    st.divider()
    st.markdown(
        f"**Budget:** {budget}  \n"
        f"**Metal:** {metal}  \n"
        f"**Style:** {style}  \n"
        f"**Occasion:** {occasion}"
    )

with right:
    product = recommend(budget, metal, style, occasion)

    st.subheader("Recommended Item:")
    st.success(product.title)

    img = load_product_image(product.local_image, product.fallback_url, product.title)
    st.image(img, use_container_width=True, caption=product.title)

    st.divider()
    st.markdown("### 🗣️ Sales Script")
    st.write(f"Say this: **“{product.talk_track}”**")

    st.markdown("### ✅ Why this fits")
    st.write(product.why_it_fits)

    st.markdown("### 🔥 Easy add-on to increase ticket")
    st.write(product.add_on)

    st.divider()

    # Missing images checklist
    required = [
        "cuban_chain.jpg",
        "diamond_studs.jpg",
        "figaro_chain.jpg",
        "rope_chain.jpg",
        "tennis_bracelet.jpg",
    ]

    st.markdown("### 📸 Missing Images Checklist (upload these to /assets)")
    if not ASSETS_DIR.exists():
        st.error("Folder not found: assets/ (create it in the same folder as app.py).")
    else:
        missing = [f for f in required if not (ASSETS_DIR / f).exists()]
        if missing:
            st.warning("These files are missing right now:")
            for m in missing:
                st.write(f"- assets/{m}")
            st.info("Tip: Use clean white background product photos for the most luxury look.")
        else:
            st.success("All product images are present ✅")
