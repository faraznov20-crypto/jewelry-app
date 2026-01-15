import streamlit as st

st.set_page_config(page_title="Faraz Jewelry AI", page_icon="💎")

st.title("💎 Faraz Jewelry Sales Tool")

# --- SIDEBAR (THE QUESTIONS) ---
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("What is the Customer's Budget?", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.sidebar.selectbox("What Metal do they like?", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("What Style?", ["Simple", "Classic", "Iced Out"])

# --- MAIN PAGE (THE RECOMMENDATION) ---
# The Logic
recommendation = "Ask Manager for Help" 

if budget == "$100" and metal == "Silver":
    recommendation = "Thin Box Chain"
elif budget == "$500" and metal == "Gold":
    recommendation = "3mm Rope Chain"
elif budget == "$1000" and style == "Iced Out":
    recommendation = "Diamond Cross Pendant"
elif budget == "$1000+" and style == "Classic":
    recommendation = "Moissanite Tennis Bracelet"
elif budget == "$5000+":
    recommendation = "Real Diamond Tennis Bracelet"

# Show the Result
st.header("Recommended Item:")
st.success(f"**{recommendation}**")

# The Visuals & Script
if recommendation == "Thin Box Chain":
    st.image("https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400")
    st.info("🗣️ Say this: 'This is our classic daily chain. It is strong but very light.'")

elif recommendation == "3mm Rope Chain":
    st.image("https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400")
    st.info("🗣️ Say this: 'The Rope chain is the best seller for men. It catches the light perfectly.'")

elif recommendation == "Diamond Cross Pendant":
    st.image("https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=400")
    st.info("🗣️ Say this: 'This is a statement piece. It shines from across the room.'")

elif recommendation == "Moissanite Tennis Bracelet":
    st.image("https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400")
    st.info("🗣️ Say this: 'You get the diamond look for 10% of the price. Smart choice.'")

elif recommendation == "Real Diamond Tennis Bracelet":
    st.image("https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=400")
    st.info("🗣️ Say this: 'This is an investment. Pure luxury. It will last forever.'")
