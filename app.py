import streamlit as st

st.set_page_config(page_title="Faraz Jewelry AI", page_icon="💎")

st.title("💎 Faraz Jewelry Sales Tool")

# --- SIDEBAR (THE QUESTIONS) ---
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("What is the Customer's Budget?", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.sidebar.selectbox("What Metal do they like?", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("What Style?", ["Simple", "Classic", "Iced Out"])
occasion = st.sidebar.selectbox("What is the Occasion?", ["Daily Wear", "Gift", "Special Event"])

# --- MAIN PAGE (THE LOGIC) ---
# Default "Safe" Choice
recommendation = "3mm Rope Chain"
image_url = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400"

# The 5 Specific Rules
if budget == "$100" and metal == "Silver":
    recommendation = "Thin Box Chain"
    # Silver Chain Picture
    image_url = "https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?w=400"

elif budget == "$500" and metal == "Gold":
    recommendation = "3mm Rope Chain"
    # Gold Chain Picture
    image_url = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400"

elif budget == "$1000" and style == "Iced Out":
    recommendation = "Diamond Cross Pendant"
    # Cross Pendant Picture
    image_url = "https://images.unsplash.com/photo-1599643478518-17488fbbcd75?w=400"

elif budget == "$1000+" and style == "Classic":
    recommendation = "Moissanite Tennis Bracelet"
    # Gold/Diamond Bangle Picture
    image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400"

elif budget == "$5000+":
    recommendation = "Real Diamond Tennis Bracelet"
    # Real Diamond Bracelet Picture (Silver/White Gold look)
    image_url = "
