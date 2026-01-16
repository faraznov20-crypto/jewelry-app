"""
Grand Jewelers Pentagon City - Sales Tool
Production-Ready Version with Enhanced Features
"""

import io
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# ----------------------------
# Configuration & Setup
# ----------------------------
st.set_page_config(
    page_title="Grand Jewelers Pentagon City — Sales Tool",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for luxury feel
st.markdown(
    """
    <style>
      .block-container { 
        padding-top: 1.2rem; 
        padding-bottom: 2rem; 
        max-width: 1400px;
      }
      .gj-card {
        border: 1px solid #e6e6e6;
        border-radius: 14px;
        padding: 20px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      }
      .gj-pill {
        background: linear-gradient(135deg, #e9f8ee 0%, #d4f1dd 100%);
        color: #0f6a2a;
        border-radius: 10px;
        padding: 12px 16px;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        display: inline-block;
        text-align: center;
        border: 2px solid #0f6a2a;
      }
      .gj-warning {
        background: #fff4e6;
        border-left: 4px solid #ff9800;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
      }
      .gj-hr { 
        border-top: 1px solid #eee; 
        margin: 20px 0; 
      }
      h1 { color: #1a1a1a; font-weight: 700; }
      h2 { color: #2c2c2c; font-weight: 600; }
      h3 { color: #3d3d3d; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------
# Assets Directory Management
# ----------------------------
def get_assets_dir() -> Path:
    """
    Intelligently locate assets directory.
    Handles both correct structure and accidental nested assets/assets/
    """
    base = Path(__file__).parent
    primary = base / "assets"
    nested = base / "assets" / "assets"
    
    # Create primary if doesn't exist
    primary.mkdir(exist_ok=True)
    
    # Prefer primary unless it's empty and nested has content
    if list(primary.glob("*.jpg")) or list(primary.glob("*.png")):
        return primary
    elif nested.exists() and (list(nested.glob("*.jpg")) or list(nested.glob("*.png"))):
        return nested
    else:
        return primary


ASSETS_DIR = get_assets_dir()


# ----------------------------
# Helper Functions
# ----------------------------
def slug(s: str) -> str:
    """Convert string to filename-safe slug"""
    return (
        s.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("&", "and")
        .replace("-", "_")
        .replace("–", "_")
        .replace("$", "")
        .replace(",", "")
        .replace("+", "plus")
    )


def metal_slug(metal: str) -> str:
    """Standardized metal names for filenames"""
    mapping = {
        "Yellow Gold": "yellow",
        "White Gold": "white",
        "Rose Gold": "rose",
        "Silver": "silver",
        "Platinum": "platinum",
    }
    return mapping.get(metal, slug(metal))


def budget_to_number(label: str) -> int:
    """Convert budget label to numeric floor value"""
    ranges = {
        "Under $300": 0,
        "$300–$500": 300,
        "$500–$1,000": 500,
        "$1,000–$2,500": 1000,
        "$2,500–$5,000": 2500,
        "$5,000+": 5000,
    }
    return ranges.get(label, 0)


def make_placeholder(title: str, subtitle: str = "Upload product photo") -> Image.Image:
    """Create professional placeholder image"""
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), (248, 248, 248))
    draw = ImageDraw.Draw(img)
    
    # Border
    margin = 50
    draw.rectangle([margin, margin, w - margin, h - margin], 
                   outline=(200, 200, 200), width=8)
    
    # Load fonts safely
    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 40)
        font_brand = ImageFont.truetype("DejaVuSans.ttf", 32)
    except:
        try:
            font_title = ImageFont.truetype("Arial.ttf", 72)
            font_sub = ImageFont.truetype("Arial.ttf", 40)
            font_brand = ImageFont.truetype("Arial.ttf", 32)
        except:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            font_brand = ImageFont.load_default()
    
    # Title
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) / 2, h * 0.38), title, fill=(80, 80, 80), font=font_title)
    
    # Subtitle
    bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
    sw = bbox[2] - bbox[0]
    draw.text(((w - sw) / 2, h * 0.52), subtitle, fill=(120, 120, 120), font=font_sub)
    
    # Brand
    brand = "Grand Jewelers Pentagon City"
    bbox = draw.textbbox((0, 0), brand, font=font_brand)
    bw = bbox[2] - bbox[0]
    draw.text(((w - bw) / 2, h * 0.75), brand, fill=(100, 100, 100), font=font_brand)
    
    return img


# ----------------------------
# Product Data Model
# ----------------------------
@dataclass(frozen=True)
class Product:
    key: str
    title: str
    category: str  # "chain", "earrings", "bracelet"
    default_image: str
    fallback_url: Optional[str]
    price_range: str
    talk_track: str
    why_it_fits: str
    add_on: str
    keywords: List[str]  # For better matching


# ----------------------------
# Product Catalog (Expanded)
# ----------------------------
CATALOG: Dict[str, Product] = {
    "figaro_chain": Product(
        key="figaro_chain",
        title="3.5mm Figaro Chain",
        category="chain",
        default_image="figaro_chain.jpg",
        fallback_url=None,
        price_range="$250–$450",
        talk_track="Italian classic—simple pattern, always in style. This is our most requested starter chain.",
        why_it_fits="Perfect for customers wanting timeless simplicity. Figaro has been a staple for 50+ years.",
        add_on="Offer a free clasp upgrade or cleaning kit to close today.",
        keywords=["simple", "classic", "daily", "affordable", "italian"]
    ),
    
    "rope_chain": Product(
        key="rope_chain",
        title="3mm Rope Chain",
        category="chain",
        default_image="rope_chain.jpg",
        fallback_url=None,
        price_range="$350–$650",
        talk_track="Best seller—durable and catches light beautifully. Hides scratches better than any other chain style.",
        why_it_fits="Rope chains reflect light from every angle, feel substantial, and work with any outfit.",
        add_on="Add a small pendant (cross, initial, or coin medallion).",
        keywords=["bestseller", "durable", "shiny", "daily", "versatile"]
    ),
    
    "cuban_chain": Product(
        key="cuban_chain",
        title="4mm Cuban Link Chain",
        category="chain",
        default_image="cuban_chain.jpg",
        fallback_url=None,
        price_range="$600–$1,200",
        talk_track="Clean, strong, and sits flat—this is the everyday confidence chain. Miami Cuban link quality.",
        why_it_fits="Lays flat against the chest, looks premium, works daily or for nights out. Our #1 chain for style.",
        add_on="Bundle with matching Cuban bracelet (15% off set).",
        keywords=["bold", "trendy", "cuban", "miami", "flex", "party"]
    ),
    
    "iced_chain": Product(
        key="iced_chain",
        title="Iced Out Cuban Chain",
        category="chain",
        default_image="iced_chain.jpg",
        fallback_url=None,
        price_range="$1,500–$3,500",
        talk_track="This is the statement piece—maximum shine for party nights. Lab diamonds, real flash.",
        why_it_fits="For customers who want to stand out. Full CZ or lab diamond coverage, catches every light.",
        add_on="Add matching iced bracelet for a complete set (bundle discount available).",
        keywords=["iced", "flashy", "party", "diamonds", "statement", "luxury"]
    ),
    
    "tennis_bracelet": Product(
        key="tennis_bracelet",
        title="Diamond Tennis Bracelet",
        category="bracelet",
        default_image="tennis_bracelet.jpg",
        fallback_url=None,
        price_range="$2,000–$6,000",
        talk_track="Quiet luxury—sparkle without shouting. This is the piece that says 'I've made it' with class.",
        why_it_fits="High-budget customers love tennis bracelets for daily luxury. Timeless, elegant, investment piece.",
        add_on="Add diamond studs for a matching daily luxury set (we offer set pricing).",
        keywords=["luxury", "diamonds", "elegant", "investment", "classic", "formal"]
    ),
    
    "diamond_studs": Product(
        key="diamond_studs",
        title="Diamond Stud Earrings (1.0 ct tw)",
        category="earrings",
        default_image="diamond_studs.jpg",
        fallback_url=None,
        price_range="$800–$2,500",
        talk_track="Studs are the #1 forever piece—goes with everything, every day, every occasion.",
        why_it_fits="For simple daily wear, studs are unbeatable: clean, classic, always appropriate.",
        add_on="Bundle: studs + chain = complete set (small discount or free cleaning kit).",
        keywords=["earrings", "classic", "gift", "diamonds", "daily", "versatile", "anniversary"]
    ),
    
    # Additional products for more variety
    "herringbone_chain": Product(
        key="herringbone_chain",
        title="5mm Herringbone Chain",
        category="chain",
        default_image="herringbone_chain.jpg",
        fallback_url=None,
        price_range="$450–$900",
        talk_track="Sleek and sophisticated—herringbone lays perfectly flat and has a unique woven texture.",
        why_it_fits="Great for customers who want something different from the usual chains. Very comfortable.",
        add_on="Suggest a matching herringbone bracelet for a coordinated look.",
        keywords=["sleek", "flat", "sophisticated", "unique", "comfortable"]
    ),
    
    "box_chain": Product(
        key="box_chain",
        title="2.5mm Box Chain",
        category="chain",
        default_image="box_chain.jpg",
        fallback_url=None,
        price_range="$200–$400",
        talk_track="Simple, strong, and affordable—the perfect chain for pendants and everyday wear.",
        why_it_fits="Box chains are incredibly durable and ideal for holding pendants without twisting.",
        add_on="Add any of our pendant collection—this chain holds them perfectly.",
        keywords=["simple", "affordable", "pendant", "daily", "durable"]
    ),
}


# ----------------------------
# Smart Recommendation Engine
# ----------------------------
def recommend(budget_label: str, metal: str, style: str, occasion: str) -> Product:
    """
    Enhanced recommendation logic with fallback chain.
    Priority: Style → Budget → Occasion → Default
    """
    budget = budget_to_number(budget_label)
    
    # PRIORITY 1: Style-based (strongest signal)
    if style == "Iced Out":
        return CATALOG["iced_chain"]
    
    if style == "Luxury":
        if budget >= 2000:
            # Alternate based on occasion
            if occasion in ["Daily Wear", "Business/Formal"]:
                return CATALOG["tennis_bracelet"]
            else:
                return CATALOG["diamond_studs"]
        else:
            return CATALOG["tennis_bracelet"]  # Aspirational
    
    # PRIORITY 2: Budget-based (clear price signals)
    if budget >= 5000:
        return CATALOG["tennis_bracelet"]
    
    if budget >= 2500:
        if occasion == "Gift" or occasion == "Wedding/Engagement":
            return CATALOG["diamond_studs"]
        return CATALOG["iced_chain"]
    
    if budget >= 1000:
        if occasion in ["Gift", "Wedding/Engagement", "Anniversary"]:
            return CATALOG["diamond_studs"]
        if occasion == "Party/Club":
            return CATALOG["iced_chain"]
        return CATALOG["cuban_chain"]
    
    # PRIORITY 3: Occasion-based (mid-range budgets)
    if occasion == "Party/Club":
        if budget >= 600:
            return CATALOG["cuban_chain"]
        return CATALOG["rope_chain"]
    
    if occasion in ["Gift", "Wedding/Engagement", "Anniversary"]:
        if budget >= 800:
            return CATALOG["diamond_studs"]
        return CATALOG["rope_chain"]
    
    if occasion == "Business/Formal":
        if budget >= 400:
            return CATALOG["herringbone_chain"]
        return CATALOG["box_chain"]
    
    # PRIORITY 4: Budget tiers (daily wear default)
    if budget < 300:
        return CATALOG["box_chain"]
    elif budget < 500:
        return CATALOG["figaro_chain"]
    elif budget < 1000:
        return CATALOG["rope_chain"]
    else:
        return CATALOG["cuban_chain"]


# ----------------------------
# Image Loading System
# ----------------------------
def image_candidates(product: Product, metal: str, style: str, occasion: str) -> List[str]:
    """
    Generate list of possible image filenames in priority order.
    Format: {product_key}_{metal}_{style}_{occasion}.jpg
    """
    m = metal_slug(metal)
    s = slug(style)
    o = slug(occasion)
    
    return [
        f"{product.key}_{m}_{s}_{o}.jpg",  # Most specific
        f"{product.key}_{m}_{s}.jpg",       # Metal + style
        f"{product.key}_{m}.jpg",           # Metal only
        product.default_image,              # Fallback
    ]


@st.cache_data(show_spinner=False)
def load_image_cached(path_str: str, fallback_url: Optional[str], mtime: float) -> Tuple[Image.Image, str]:
    """
    Load image with caching. Returns (image, source).
    Source: "local" | "web" | "placeholder"
    """
    p = Path(path_str)
    
    # Try local first
    if p.exists():
        try:
            return Image.open(p).convert("RGB"), "local"
        except Exception as e:
            st.warning(f"Error loading {p.name}: {e}")
    
    # Try web fallback
    if fallback_url:
        try:
            with urllib.request.urlopen(fallback_url, timeout=10) as resp:
                data = resp.read()
            return Image.open(io.BytesIO(data)).convert("RGB"), "web"
        except Exception:
            pass
    
    # Generate placeholder
    return make_placeholder(p.stem.replace("_", " ").title()), "placeholder"


def load_best_image(product: Product, metal: str, style: str, occasion: str) -> Tuple[Image.Image, str, str]:
    """
    Find and load the best matching image.
    Returns (image, source, chosen_filename)
    """
    candidates = image_candidates(product, metal, style, occasion)
    
    for fname in candidates:
        p = ASSETS_DIR / fname
        mtime = p.stat().st_mtime if p.exists() else 0.0
        img, src = load_image_cached(str(p), product.fallback_url, mtime)
        
        if src == "local":
            return img, src, fname
    
    # No local images found - return placeholder with first candidate name
    p = ASSETS_DIR / candidates[0]
    mtime = p.stat().st_mtime if p.exists() else 0.0
    img, src = load_image_cached(str(p), product.fallback_url, mtime)
    return img, src, candidates[0]


# ----------------------------
# Main UI
# ----------------------------
st.title("💎 Grand Jewelers Pentagon City — Sales Tool")
st.markdown("**Intelligent Product Recommendations for Your Customers**")
st.markdown("---")

# Two-column layout
left_col, right_col = st.columns([1, 2.2], gap="large")

# LEFT COLUMN: Customer Inputs
with left_col:
    st.markdown('<div class="gj-card">', unsafe_allow_html=True)
    st.subheader("📋 Customer Profile")
    
    budget = st.selectbox(
        "💰 Budget Range",
        ["Under $300", "$300–$500", "$500–$1,000", "$1,000–$2,500", "$2,500–$5,000", "$5,000+"],
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
        ["Daily Wear", "Gift", "Wedding/Engagement", "Party/Club", "Business/Formal", "Anniversary"],
        help="What's the jewelry for?"
    )
    
    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)
    
    # Summary
    st.markdown("**Current Selection:**")
    st.caption(f"💰 {budget} | 🔶 {metal}")
    st.caption(f"✨ {style} | 🎯 {occasion}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Get recommendation
product = recommend(budget, metal, style, occasion)

# RIGHT COLUMN: Recommendation Display
with right_col:
    # Product Title
    st.markdown("## 🎁 Recommended Product")
    st.markdown(f'<div class="gj-pill">{product.title}</div>', unsafe_allow_html=True)
    st.caption(f"💵 Price Range: **{product.price_range}**")
    st.write("")
    
    # Load and display image
    img, img_source, chosen_filename = load_best_image(product, metal, style, occasion)
    st.image(img, use_container_width=True, caption=product.title)
    
    # Image status indicator
    candidates = image_candidates(product, metal, style, occasion)
    
    if img_source != "local":
        st.markdown('<div class="gj-warning">⚠️ <strong>Placeholder Image</strong> - Upload real product photo</div>', 
                   unsafe_allow_html=True)
        
        with st.expander("📸 Upload Instructions"):
            st.markdown("**Upload ONE of these filenames (in priority order):**")
            for i, fname in enumerate(candidates, 1):
                icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "💾"
                st.code(f"{icon} {ASSETS_DIR.name}/{fname}", language="text")
            st.info("💡 Tip: Upload metal-specific images for automatic switching when metal changes.")
    else:
        st.success(f"✅ Using: `{ASSETS_DIR.name}/{chosen_filename}`")
    
    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)
    
    # Sales Information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🗣️ Sales Script")
        st.info(f'**Say this:**\n\n"{product.talk_track}"')
    
    with col2:
        st.markdown("### ✅ Why This Works")
        st.success(product.why_it_fits)
    
    st.markdown("### 🔥 Upsell Strategy")
    st.warning(f"**Add-on opportunity:** {product.add_on}")
    
    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)
    
    # Image Checklist
    with st.expander("📸 Complete Image Checklist"):
        st.markdown("#### Base Images (Required)")
        
        base_missing = []
        base_found = []
        
        for key, prod in CATALOG.items():
            if (ASSETS_DIR / prod.default_image).exists():
                base_found.append(prod.default_image)
            else:
                base_missing.append(prod.default_image)
        
        if base_missing:
            st.error(f"**Missing {len(base_missing)} base images:**")
            for fname in base_missing:
                st.code(f"{ASSETS_DIR.name}/{fname}", language="text")
        else:
            st.success(f"✅ All {len(base_found)} base product images uploaded!")
        
        st.markdown("---")
        st.markdown("#### Metal-Specific Images (Optional)")
        st.caption("Upload these to show different metals automatically")
        
        metals = ["yellow", "white", "rose", "silver", "platinum"]
        metal_examples = []
        
        for key in list(CATALOG.keys())[:3]:  # Show examples for first 3 products
            for m in metals:
                metal_examples.append(f"{key}_{m}.jpg")
        
        st.code("\n".join(metal_examples[:10]), language="text")
        st.caption(f"...and {len(CATALOG) * len(metals) - 10} more combinations")

# Footer
st.markdown("---")
st.caption("💎 Grand Jewelers Pentagon City | Sales Tool v2.0 | Upload photos to assets/ folder for best results")
