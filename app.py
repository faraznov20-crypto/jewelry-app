import io
import urllib.request
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Tuple

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
      .gj-card { border: 1px solid #e6e6e6; border-radius: 14px; padding: 16px; background: white; }
      .gj-pill { background: #e9f8ee; color: #0f6a2a; border-radius: 10px; padding: 10px 12px; font-weight: 700; width: 100%; display: inline-block; }
      .gj-muted { color: #6b7280; }
      .gj-hr { border-top: 1px solid #eee; margin: 18px 0; }
      .gj-small { font-size: 0.92rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

APP_DIR = Path(__file__).parent

# ✅ Use /assets (and also support /assets/assets if you accidentally made it)
ASSETS_A = APP_DIR / "assets"
ASSETS_B = APP_DIR / "assets" / "assets"
ASSETS_A.mkdir(exist_ok=True)

def pick_assets_dir() -> Path:
    # If assets/assets has images and assets/ has none, use assets/assets
    a_has = any(ASSETS_A.glob("*.jpg")) or any(ASSETS_A.glob("*.png"))
    b_has = any(ASSETS_B.glob("*.jpg")) or any(ASSETS_B.glob("*.png"))
    if b_has and not a_has:
        return ASSETS_B
    return ASSETS_A

ASSETS_DIR = pick_assets_dir()


# ----------------------------
# Helpers
# ----------------------------
def slug(s: str) -> str:
    s = s.strip().lower()
    s = s.replace("&", "and")
    s = s.replace("/", "_")
    s = s.replace(" ", "_")
    s = s.replace("-", "_")
    s = s.replace("__", "_")
    return s

def metal_slug(metal: str) -> str:
    m = metal.strip().lower()
    if "yellow" in m: return "yellow"
    if "white" in m: return "white"
    if "rose" in m: return "rose"
    if "silver" in m: return "silver"
    if "platinum" in m: return "platinum"
    return "unknown"

def occasion_slug(occ: str) -> str:
    # keep it short for filenames
    o = occ.strip().lower()
    if "daily" in o: return "daily"
    if "gift" in o: return "gift"
    if "wedding" in o or "engagement" in o: return "wedding"
    if "party" in o or "club" in o: return "party"
    if "business" in o or "formal" in o: return "business"
    return slug(occ)

def style_slug(sty: str) -> str:
    s = sty.strip().lower()
    if "iced" in s: return "iced"
    if "lux" in s: return "luxury"
    if "trend" in s: return "trendy"
    if "classic" in s: return "classic"
    if "simple" in s: return "simple"
    return slug(sty)

def build_image_candidates(stem: str, metal: str, style: str, occasion: str) -> List[str]:
    """
    Priority order (best first):
    1) stem_metal_style_occasion.jpg
    2) stem_metal_style.jpg
    3) stem_metal.jpg
    4) stem.jpg
    """
    m = metal_slug(metal)
    s = style_slug(style)
    o = occasion_slug(occasion)
    return [
        f"{stem}_{m}_{s}_{o}.jpg",
        f"{stem}_{m}_{s}.jpg",
        f"{stem}_{m}.jpg",
        f"{stem}.jpg",
        f"{stem}.png",
    ]

@st.cache_data(show_spinner=False)
def load_image_from_web(query: str) -> Optional[Image.Image]:
    """
    Gets a nice random stock image from Unsplash Source.
    This is only a fallback. (Random = not always exact.)
    """
    try:
        q = urllib.parse.quote_plus(query)
        url = f"https://source.unsplash.com/1600x900/?{q}"
        with urllib.request.urlopen(url, timeout=8) as resp:
            data = resp.read()
        return Image.open(io.BytesIO(data)).convert("RGB")
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def load_best_image(candidates: List[str], web_query: str) -> Tuple[Image.Image, str, str]:
    """
    Returns: (image, source_label, used_filename)
    source_label: local | web | placeholder
    """
    # 1) Local
    for name in candidates:
        p = ASSETS_DIR / name
        if p.exists():
            try:
                return Image.open(p).convert("RGB"), "local", name
            except Exception:
                pass

    # 2) Web fallback (better than ugly placeholder)
    img = load_image_from_web(web_query)
    if img is not None:
        return img, "web", "(web)"

    # 3) Placeholder (last option)
    img = Image.new("RGB", (1600, 900), (220, 220, 220))
    return img, "placeholder", "(placeholder)"


def budget_floor(label: str) -> int:
    if label == "Under $300": return 0
    if label == "$300–$500": return 300
    if label == "$500–$1,000": return 500
    if label == "$1,000–$2,500": return 1000
    if label == "$2,500–$5,000": return 2500
    if label == "$5,000+": return 5000
    return 0


# ----------------------------
# Catalog
# ----------------------------
@dataclass(frozen=True)
class Product:
    key: str
    title: str
    category: str               # Chain / Bracelet / Ring / Earrings / Pendant
    stem: str                   # file stem, ex: "cuban_chain"
    min_budget: int
    max_budget: int
    styles: List[str]
    occasions: List[str]
    talk_track: str
    why_it_fits: str
    add_on: str
    web_keywords: str           # for web fallback (nice stock image)

CATALOG: List[Product] = [
    # CHAINS
    Product(
        key="cuban_4mm",
        title="4mm Cuban Link Chain",
        category="Chain",
        stem="cuban_chain",
        min_budget=500,
        max_budget=2500,
        styles=["Trendy", "Classic", "Simple", "Luxury"],
        occasions=["Daily Wear", "Party/Club", "Business/Formal"],
        talk_track="Clean, strong, and sits flat—this is the everyday flex chain.",
        why_it_fits="Cuban lays flat, looks premium, and works daily or for party. Easy yes item.",
        add_on="Match with a Cuban bracelet (bundle deal) + cleaning kit.",
        web_keywords="cuban link chain jewelry macro",
    ),
    Product(
        key="figaro_3_5mm",
        title="3.5mm Figaro Chain",
        category="Chain",
        stem="figaro_chain",
        min_budget=0,
        max_budget=1000,
        styles=["Simple", "Classic"],
        occasions=["Daily Wear", "Gift", "Business/Formal"],
        talk_track="Italian classic—simple pattern, always in style.",
        why_it_fits="Safe winner for simple daily wear. Timeless, clean, never goes out of style.",
        add_on="Offer clasp upgrade OR cleaning kit to close today.",
        web_keywords="figaro chain gold jewelry closeup",
    ),
    Product(
        key="rope_3mm",
        title="3mm Rope Chain",
        category="Chain",
        stem="rope_chain",
        min_budget=0,
        max_budget=1000,
        styles=["Simple", "Classic", "Trendy"],
        occasions=["Daily Wear", "Gift", "Party/Club"],
        talk_track="Best seller—durable and catches light nicely.",
        why_it_fits="Rope reflects light and hides small scratches well. Great for daily wear.",
        add_on="Add a small pendant (cross/initial) + cleaning kit.",
        web_keywords="rope chain gold jewelry macro",
    ),
    Product(
        key="tennis_bracelet_diamond",
        title="Diamond Tennis Bracelet",
        category="Bracelet",
        stem="tennis_bracelet",
        min_budget=2500,
        max_budget=999999,
        styles=["Simple", "Classic", "Luxury"],
        occasions=["Daily Wear", "Gift", "Business/Formal", "Wedding/Engagement"],
        talk_track="Quiet luxury—sparkle but still classy and wearable every day.",
        why_it_fits="High budget + simple style = tennis bracelet. Looks expensive without being loud.",
        add_on="Add diamond studs for a matching set.",
        web_keywords="diamond tennis bracelet closeup jewelry",
    ),
    Product(
        key="diamond_studs",
        title="Diamond Stud Earrings",
        category="Earrings",
        stem="diamond_studs",
        min_budget=1000,
        max_budget=999999,
        styles=["Simple", "Classic", "Luxury"],
        occasions=["Daily Wear", "Gift", "Wedding/Engagement", "Business/Formal"],
        talk_track="Studs are the forever piece—goes with everything.",
        why_it_fits="Clean, classic, always appropriate. Best gift item too.",
        add_on="Add a tennis bracelet (bundle + upgrade).",
        web_keywords="diamond stud earrings closeup jewelry",
    ),

    # Add one more “Party/Iced” item so categories don’t all show the same:
    Product(
        key="iced_cuban",
        title="Iced Cuban Chain (Diamond Look)",
        category="Chain",
        stem="iced_cuban_chain",
        min_budget=1000,
        max_budget=999999,
        styles=["Iced Out", "Luxury", "Trendy"],
        occasions=["Party/Club"],
        talk_track="This is the party chain—big shine, big energy.",
        why_it_fits="If they say party/club + iced out, this is the obvious pick.",
        add_on="Match with iced bracelet (set) + warranty talk.",
        web_keywords="iced out cuban chain jewelry diamonds closeup",
    ),
]

def score_product(p: Product, b: int, category: str, style: str, occasion: str) -> int:
    score = 0

    # Category match matters most
    if p.category == category:
        score += 100
    else:
        score -= 30

    # Budget match
    if p.min_budget <= b <= p.max_budget:
        score += 60
    else:
        # still allow but reduce
        if b < p.min_budget: score -= 40
        if b > p.max_budget: score -= 10

    # Style + occasion
    if style in p.styles:
        score += 30
    if occasion in p.occasions:
        score += 30

    # If user wants Iced Out and product is not iced, punish
    if style == "Iced Out" and "Iced Out" not in p.styles:
        score -= 50

    return score

def recommend_top3(budget_label: str, category: str, style: str, occasion: str) -> List[Product]:
    b = budget_floor(budget_label)
    ranked = sorted(CATALOG, key=lambda p: score_product(p, b, category, style, occasion), reverse=True)
    return ranked[:3]


# ----------------------------
# UI
# ----------------------------
left, right = st.columns([1, 2.2], gap="large")

with left:
    st.markdown('<div class="gj-card">', unsafe_allow_html=True)
    st.subheader("Customer Details")

    budget = st.selectbox("Budget", ["Under $300", "$300–$500", "$500–$1,000", "$1,000–$2,500", "$2,500–$5,000", "$5,000+"])
    metal = st.selectbox("Metal", ["Yellow Gold", "White Gold", "Rose Gold", "Silver", "Platinum"])
    category = st.selectbox("Category", ["Chain", "Bracelet", "Ring", "Earrings", "Pendant"])
    style = st.selectbox("Style", ["Simple", "Classic", "Trendy", "Iced Out", "Luxury"])
    occasion = st.selectbox("Occasion", ["Daily Wear", "Gift", "Wedding/Engagement", "Party/Club", "Business/Formal"])

    st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)
    st.markdown("**💎 Grand Jewelers Pentagon City — Sales Tool**")
    st.caption(f"Budget: {budget} | Metal: {metal} | Category: {category} | Style: {style} | Occasion: {occasion}")

    st.markdown("</div>", unsafe_allow_html=True)

top3 = recommend_top3(budget, category, style, occasion)
best = top3[0] if top3 else None

with right:
    st.markdown("## Recommended Items (Top 3):")

    for i, p in enumerate(top3, start=1):
        st.markdown(f"### #{i} {p.title}")

        # Build local filenames based on metal/style/occasion
        candidates = build_image_candidates(p.stem, metal, style, occasion)

        # Better web query (adds metal words)
        web_query = f"{metal} {p.web_keywords}"

        img, src, used = load_best_image(candidates, web_query)
        st.image(img, use_container_width=True, caption=p.title)

        if src != "local":
            st.info(
                f"Not using your real photo yet (source: {src}). "
                f"To force the correct photo, upload ONE of these filenames into `{ASSETS_DIR.name}/`:\n\n"
                + "\n".join([f"- {ASSETS_DIR.name}/{name}" for name in candidates[:3]])
            )
        else:
            st.success(f"Using your real photo ✅ ({used})")

        st.markdown("**🗣️ Sales Script**")
        st.success(f"Say this: “{p.talk_track}”")

        st.markdown("**✅ Why this fits**")
        st.write(p.why_it_fits)

        st.markdown("**🔥 Easy add-on**")
        st.write(p.add_on)

        st.markdown('<div class="gj-hr"></div>', unsafe_allow_html=True)

    with st.expander("📸 Exactly what to upload (for this selection)"):
        if best:
            candidates = build_image_candidates(best.stem, metal, style, occasion)
            st.write("Upload ONE of these (best first):")
            for name in candidates:
                st.code(f"{ASSETS_DIR.name}/{name}", language="text")

st.caption("Tip: Best results = upload real product photos. Web images are only fallback and may be random.")
