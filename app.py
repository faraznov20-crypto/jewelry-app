import streamlit as st
from pathlib import Path

# ---------- SETUP ----------
st.set_page_config(page_title="Faraz Jewelry Sales Tool", page_icon="💎")
st.title("💎 Faraz Jewelry Sales Tool")

ASSETS = Path(__file__).parent / "assets"

# ---------- SIDEBAR (INPUTS) ----------
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("Budget", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.sidebar.selectbox("Metal", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("Style", ["Simple", "Classic", "Iced Out"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Wear", "Gift", "Special Event"])

# ---------- ITEMS (NAME + IMAGE + SCRIPTS) ----------
ITEMS = {
    "thin_box_chain": {
        "name": "Thin Box Chain",
        "image": "thin_box_chain.jpg",
        "script": {
            "Daily Wear": "This is strong but light. Easy daily wear.",
            "Gift": "Perfect gift. Clean look and fits anyone.",
            "Special Event": "Simple but classy. Looks clean in photos.",
        },
    },
    "rope_chain": {
        "name": "3mm Rope Chain",
        "image": "rope_chain.jpg",
        "script": {
            "Daily Wear": "Best seller. Durable and catches light nicely.",
            "Gift": "This is our #1 gift chain. Looks expensive in the box.",
            "Special Event": "This shines under lights. Great for going out.",
        },
    },
    "cross_pendant": {
        "name": "Diamond Cross Pendant",
        "image": "cross_pendant.jpg",
        "script": {
            "Daily Wear": "Strong piece, great daily statement.",
            "Gift": "Very meaningful gift. People love this style.",
            "Special Event": "This stands out across the room. Big shine.",
        },
    },
    "moissanite_bracelet": {
        "name": "Moissanite Tennis Bracelet",
        "image": "moissanite_bracelet.jpg",
        "script": {
            "Daily Wear": "Diamond look for less money. Smart daily luxury.",
            "Gift": "Looks like diamonds. Huge wow gift.",
            "Special Event": "Perfect for events. It sparkles hard.",
        },
    },
    "diamond_tennis_bracelet": {
        "name": "Real Diamond Tennis Bracelet",
        "image": "diamond_tennis_bracelet.jpg",
        "script": {
            "Daily Wear": "Real luxury. Built to last.",
            "Gift": "This is a serious gift. Pure class.",
            "Special Event": "Top level shine. This is the showpiece.",
        },
    },
}

# ---------- RULE ENGINE (ONE PATH ONLY) ----------
def pick_item(budget: str, metal: str, style: str) -> str:
    # 1) Style priority
    if style == "Iced Out":
        return "cross_pendant"

    # 2) Budget priority
    if budget == "$5000+":
        return "diamond_tennis_bracelet"

    if budget == "$1000+" and style == "Classic":
        return "moissanite_bracelet"

    # 3) Your original strong rules
    if budget == "$100" and metal == "Silver":
        return "thin_box_chain"

    if budget == "$500" and metal == "Gold":
        return "rope_chain"

    # 4) Clean fallback (never weird)
    # If metal is Silver -> show silver chain, else show gold rope chain
    if metal == "Silver":
        return "thin_box_chain"
    return "rope_chain"

chosen_key = pick_item(budget, metal, style)
chosen = ITEMS[chosen_key]

# ---------- DISPLAY ----------
st.caption(f"Budget: {budget} | Metal: {metal} | Style: {style} | Occasion: {occasion}")

st.header("Recommended Item:")
st.success(f"**{chosen['name']}**")

img_path = ASSETS / chosen["image"]
if img_path.exists():
    st.image(str(img_path), caption=chosen["name"])
else:
    st.error("Image file not found in /assets.")
    st.write("Missing file:", chosen["image"])
    st.write("Make sure you uploaded it to GitHub in the assets folder.")

st.write("---")
st.subheader("🗣️ Sales Script")
st.info(f"Say this: '{chosen['script'][occasion]}'")
