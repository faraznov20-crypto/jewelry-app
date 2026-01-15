import io
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import streamlit as st
from PIL import Image, ImageDraw

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
        font-weight: 700;
        width: 100%;
        display: inline-block;
      }
      .gj-muted { color: #6b7280; }
      .gj-hr { border-top: 1px solid #eee; margin: 18px 0; }
      .small { font-size: 0.92rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# Assets folder (fix assets/assets mistake too)
# ----------------------------
def get_assets_dir() -> Path:
    base = Path(__file__).parent
    a = base / "assets"
    b = base / "assets" / "assets"

    # Make sure at least assets/ exists
    a.mkdir(exist_ok=True)

    # If you accidentally uploaded into assets/assets and it has images, use it
    if b.exists() and any(b.glob("*.jpg")):
        return b

    return a


ASSETS_DIR = get_assets_dir()


# ----------------------------
# Simple helpers
# ----------------------------
def slug(s: str) -> str:
    return (
        s.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("&", "and")
        .replace("-", "_")
    )


def metal_slug(metal: str) -> str:
    # keep names short and stable
    mapping = {
        "Yellow Gold": "yellow",
        "White Gold": "white",
        "Rose Gold": "rose",
        "Silver": "silver",
        "Platinum": "platinum",
    }
    return mapping.get(metal, slug(metal))


def style_slug(style: str) -> str:
    return slug(style)


def occasion_slug(occasion: str) -> str:
    return slug(occasion)


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


# ----------------------------
# Data
# ----------------------------
@dataclass(frozen=True)
class Product:
    key: str
    title: str
    # This is ONLY a fallback if you do not upload metal images
    default_image: str
    # Optional web fallback (you can paste vendor URLs here)
    fallback_url: Optional[str]
    talk_track: str
    why_it_fits: str
    add_on: str


# IMPORTANT:
# Images are chosen like this (most specific → less specific):
# 1) assets/{product_key}_{metal}_{style}_{occasion}.jpg
# 2) assets/{product_key}_{metal}.jpg
# 3) assets/{product.default_image}
CATALOG: Dict[str, Product] = {
    "cuban_chain": Product(
        key="cuban_chain",
        title="4mm Cuban Link Chain",
        default_image="cuban_chain.jpg",
        fallback_url=None,  # (optional) paste vendor URL later
        talk_track="Clean, strong, and sits flat—this is the everyday flex chain.",
        why_it_fits="It lays flat, looks premium, and works daily or party. Great ‘safe’ best seller.",
        add_on="Match with a Cuban bracelet (bundle) + cleaning kit.",
    ),
    "figaro_chain": Product(
        key="figaro_chain",
        title="3.5mm Figaro Chain",
        default_image="figaro_chain.jpg",
        fallback_url=None,
        talk_track="Italian classic—simple pattern, always in style.",
        why_it_fits="If they want simple + timeless, Figaro is the safe winner.",
        add_on="Offer clasp upgrade or cleaning kit to close today.",
    ),
    "rope_chain": Product(
        key="rope_chain",
        title="3mm Rope Chain",
        default_image="rope_chain.jpg",
        fallback_url=None,
        talk_track="Best seller—durable and catches light beautifully.",
        why_it_fits="Rope reflects light and hides small scratches well. Clean daily chain.",
        add_on="Add a small pendant (cross/initial/coin).",
    ),
    "iced_chain": Product(
        key="iced_chain",
        title="Iced Out Cuban Chain",
        default_image="iced_chain.jpg",
        fallback_url=None,
        talk_track="This is the loud piece—maximum shine for party nights.",
        why_it_fits="If they want iced + trendy, this is the right category.",
        add_on="Add matching iced bracelet for a full set.",
    ),
    "tennis_bracelet": Product(
        key="tennis_bracelet",
        title="Diamond Tennis Bracelet",
        default_image="tennis_bracelet.jpg",
        fallback_url=None,
        talk_track="Quiet luxury—sparkle, but classy and everyday wearable.",
        why_it_fits="High budget + luxury style = tennis bracelet. Always looks expensive.",
        add_on="Add diamond studs for a matching daily luxury set.",
    ),
    "diamond_studs": Product(
        key="diamond_studs",
        title="Diamond Stud Earrings",
        default_image="diamond_studs.jpg",
        fallback_url=None,
        talk_track="Studs are the #1 forever piece—goes with everything.",
        why_it_fits="For simple daily wear, studs are unbeatable: clean, classic, always appropriate.",
        add_on="Offer set: studs + tennis bracelet (bundle).",
    ),
}


# ----------------------------
# Recommendation rules (more variety)
# ----------------------------
def recommend(budget_label: str, metal: str, style: str, occasion: str) -> Product:
    b = budget_floor(budget_label)

    # Style first (so categories feel real)
    if style == "Iced Out":
        return CATALOG["iced_chain"]

    if style == "Luxury" or b >= 5000:
        # luxury budget usually wants diamonds
        if occasion in {"Daily Wear", "Business/Formal"}:
            return CATALOG["tennis_bracelet"]
        return CATALOG["diamond_studs"]

    # Occasion next
    if occasion == "Party/Club":
        return CATALOG["cuban_chain"]

    if occasion in {"Wedding/Engagement", "Gift"} and b >= 1000:
        return CATALOG["diamond_studs"]

    # Budget next
    if b < 300:
        return CATALOG["figaro_chain"]
    if b < 1000:
        return CATALOG["rope_chain"]
    return CATALOG["cuban_chain"]


# ----------------------------
# Image choosing (THIS is the Rose Gold fix)
# ----------------------------
def image_candidates(product: Product, metal: str, style: str, occasion: str) -> List[str]:
    m = metal_slug(metal)
    s = style_slug(style)
    o = occasion_slug(occasion)

    return [
        f"{product.key}_{m}_{s}_{o}.jpg",  # most specific
        f"{product.key}_{m}.jpg",          # metal-specific
        product.default_image,             # last fallback
    ]


def make_clean_placeholder(text: str) -> Image.Image:
    img = Image.new("RGB", (1600, 900), (235, 235, 235))
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "No image found", fill=(40, 40, 40))
    draw.text((60, 110), text, fill=(70, 70, 70))
    return img


@st.cache_data(show_spinner=False)
def _load_image_cached(path_str: str, fallback_url: Optional[str], cache_bust: float) -> Tuple[Image.Image, str]:
    """
    Returns (image, source)
    source: "local" | "web" | "placeholder"
    cache_bust changes when file changes, so Streamlit updates images.
    """
    p = Path(path_str)

    # 1) Local
    try:
        if p.exists():
            return Image.open(p).convert("RGB"), "local"
    except Exception:
        pass

    # 2) Web (optional)
    if fallback_url:
        try:
            with urllib.request.urlopen(fallback_url, timeout=8) as resp:
                data = resp.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
            return img, "web"
        except Exception:
            pass

    # 3) Placeholder
    return make_clean_placeholder(f"Upload into: {ASSETS_DIR.as_posix()}/"), "placeholder"


def load_best_image(product: Product, metal: str, style: str, occasion: str) -> Tuple[Image.Image, str, str]:
    """
    Finds the best matching image file based on metal/style/occasion.
    Returns (image, source, chosen_filename)
    """
    candidates = image_candidates(product, metal, style, occasion)

    for fname in candidates:
        p = ASSETS_DIR / fname
        mtime = p.stat().st_mtime if p.exists() else 0.0  # cache bust
        img, src = _load_image_cached(str(p), product.fallback_url, mtime)
        if src == "local":
            return img, src, fname

    # none local found
    p = ASSETS_DIR / candidates[0]
    mtime = p.stat().st_mtime if p.exists() else 0.0
    img, src = _load_image_cached(str(p), product.fallback_url, mtime)
    return img, src, candidates[0]


# ----------------------------
# UI
# ----------------------------
left, right = st.columns([1, 2.2], gap="large")

with left:
    st.markdown('<div class="gj-card">', unsafe_allow_html=True)
    st.subheader("Customer Details")

    budget = st.selectbox(
        "Budget",
        ["Under $300", "$300–$500", "$500–$1,000", "$1,000–$2,500", "$2,500–$5,000", "$5,000+"],
    )
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

    img, src, chosen = load_best_image(product, metal, style, occasion)
    st.image(img, use_container_width=True, caption=product.title)

    # Simple explanation + exact file names
    cands = image_candidates(product, metal, style, occasion)

    if src != "local":
        st.warning("Image not found. You need to upload a photo file with the correct name.")
        st.markdown("**Upload ONE of these file names (top is best):**")
        for f in cands:
            st.code(f"{ASSETS_DIR.name}/{f}", language="text")
    else:
        st.caption(f"✅ Using local image: `{ASSETS_DIR.name}/{chosen}`")

    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)

    st.markdown("### 🗣️ Sales Script")
    st.success(f"Say this: **“{product.talk_track}”**")

    st.markdown("### ✅ Why this fits")
    st.write(product.why_it_fits)

    st.markdown("### 🔥 Easy add-on to increase ticket")
    st.write(product.add_on)

    # Checklist (metal images)
    metals = ["yellow", "white", "rose", "silver", "platinum"]
    base_missing = []
    for k, p in CATALOG.items():
        if not (ASSETS_DIR / p.default_image).exists():
            base_missing.append(f"{ASSETS_DIR.name}/{p.default_image}")

    metal_missing = []
    for k in CATALOG.keys():
        for m in metals:
            fn = f"{k}_{m}.jpg"
            if not (ASSETS_DIR / fn).exists():
                metal_missing.append(f"{ASSETS_DIR.name}/{fn}")

    with st.expander("📸 Image checklist (simple)"):
        st.markdown("**Minimum (one image per product):**")
        if base_missing:
            for f in base_missing:
                st.code(f, language="text")
        else:
            st.success("All base product images found ✅")

        st.markdown("**Better (one image per metal):**")
        st.caption("Add these to make Metal change the photo.")
        # show only first 25 so it doesn't spam
        if metal_missing:
            for f in metal_missing[:25]:
                st.code(f, language="text")
            if len(metal_missing) > 25:
                st.caption(f"...and {len(metal_missing) - 25} more")
        else:
            st.success("All metal images found ✅")

st.caption("Best result: upload real product photos (same angle, clean background). Metal + style + occasion images are optional.")
