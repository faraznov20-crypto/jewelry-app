import streamlit as st

st.set_page_config(page_title="Faraz Jewelry AI", page_icon="💎")

st.title("💎 Faraz Jewelry Sales Tool")

# --- SIDEBAR ---
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("Budget", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.sidebar.selectbox("Metal", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("Style", ["Simple", "Classic", "Iced Out"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Wear", "Gift", "Special Event"])

# --- LOGIC START ---
# We set a "Default" first, then override it if it matches a specific rule.
recommendation = "Ask to see the Manager"
image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400" # Generic Jewelry Image

# RULE 1: Silver Cheap ($100) -> Box Chain
if budget == "$100" and metal == "Silver":
    recommendation = "Thin Box Chain (Silver)"
    image_url = "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=400" # Silver Chain

# RULE 2: Gold Medium ($500) -> Rope Chain
elif budget == "$500" and metal == "Gold":
    recommendation = "3mm Rope Chain (Gold)"
    image_url = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400" # Gold Chain

# RULE 3: Iced Out ($1000) -> Cross Pendant
elif budget == "$1000" and style == "Iced Out":
    recommendation = "Diamond Cross Pendant"
    image_url = "https://images.unsplash.com/photo-1599643478518-17488fbbcd75?w=400" # Pendant

# RULE 4: Classic Expensive ($1000+) -> Moissanite Bracelet
elif budget == "$1000+" and style == "Classic":
    recommendation = "Moissanite Tennis Bracelet"
    image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400" # Rose Gold/Diamond Bangle look

# RULE 5: Super Rich ($5000+) -> Real Diamonds
elif budget == "$5000+":
    recommendation = "Real Diamond Tennis Bracelet"
    image_url = "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=400" # Silver Diamond Bracelet

# --- DISPLAY ---
st.header("Recommended Item:")
st.success(f"**{recommendation}**")
st.image(image_url)

# --- SCRIPT ---
st.write("---")
st.subheader("🗣️ Sales Script")

if occasion == "Gift":
    st.info(f"Say this: 'This {recommendation} is our best-seller. It comes in a premium gift box. They will love it.'")
elif occasion == "Special Event":
    st.info(f"Say this: 'This piece catches the light beautifully. It is designed to stand out at events.'")
else:
    st.info(f"Say this: 'This is solid and durable. You can wear it to the gym or in the shower, no problem.'")
