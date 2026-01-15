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
    image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400"

elif budget == "$500" and metal == "Gold":
    recommendation = "3mm Rope Chain"
    image_url = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400"

elif budget == "$1000" and style == "Iced Out":
    recommendation = "Diamond Cross Pendant"
    image_url = "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=400"

elif budget == "$1000+" and style == "Classic":
    recommendation = "Moissanite Tennis Bracelet"
    image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400"

elif budget == "$5000+":
    recommendation = "Real Diamond Tennis Bracelet"
    image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400"

# --- SHOW RESULT ---
st.header("Recommended Item:")
st.success(f"**{recommendation}**")
st.image(image_url)

# --- THE SMART SCRIPT ---
st.write("---")
st.subheader("🗣️ Sales Script")

if occasion == "Gift":
    st.info(f"Say this: 'This is our best-selling {metal} piece. It comes in a premium gift box and looks much more expensive than {budget}. They will love it.'")
elif occasion == "Special Event":
    st.info(f"Say this: 'This piece catches the light beautifully. It is designed to stand out at events and parties.'")
else:
    st.info(f"Say this: 'This {recommendation} is solid and durable. You can wear it to the gym or in the shower, no problem.'")
