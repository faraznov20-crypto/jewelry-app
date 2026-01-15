import streamlit as st

# 1. PAGE SETUP
st.set_page_config(page_title="Faraz Jewelry AI", page_icon="💎")
st.title("💎 Faraz Jewelry Sales Tool")

# 2. SIDEBAR (INPUTS)
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("Budget", ["$100", "$500", "$1000", "$5000+"])
metal = st.sidebar.selectbox("Metal", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("Style", ["Simple", "Iced Out"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Wear", "Gift"])

# 3. THE BRAIN (SIMPLE LOGIC)
# We set valid defaults so the app never breaks.
item_name = "Gold Rope Chain" 
image_url = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600" # Standard Gold Chain

# LOGIC RULE 1: IF SILVER -> SHOW SILVER CHAIN
if metal == "Silver":
    item_name = "Sterling Silver Box Chain"
    image_url = "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=600" 
    # (Note: This image is a clean silver/white metal look)

# LOGIC RULE 2: IF GOLD -> SHOW GOLD CHAIN
elif metal == "Gold":
    item_name = "Solid Gold Rope Chain"
    image_url = "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=600" 
    # (Note: This is a classic gold chain image)

# LOGIC RULE 3: IF WHITE GOLD or PLATINUM -> SHOW DIAMOND LOOK
elif metal == "White Gold" or metal == "Platinum":
    item_name = "White Gold Tennis Bracelet"
    image_url = "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=600"
    # (Note: Real Diamond Bracelet image)

# LOGIC RULE 4: IF ROSE GOLD -> SHOW ROSE GOLD LOOK
elif metal == "Rose Gold":
    item_name = "Rose Gold Chain"
    image_url = "https://images.unsplash.com/photo-1599643477877-530eb83d70d2?w=600"
    # (Note: Warm gold/rose tone image)

# OVERRIDE: IF BUDGET IS HUGE ($5000+), ALWAYS SHOW DIAMONDS
if budget == "$5000+":
    item_name = "Real Diamond Tennis Bracelet (VVS)"
    image_url = "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=600"

# OVERRIDE: IF STYLE IS ICED OUT, SHOW PENDANT
if style == "Iced Out":
    item_name = "Diamond Cross Pendant"
    image_url = "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=600"


# 4. DISPLAY RESULT
st.header("Recommended Item:")
st.success(f"**{item_name}**")
st.image(image_url, caption=item_name)

# 5. SALES SCRIPT
st.write("---")
st.subheader("🗣️ Sales Script")
if occasion == "Gift":
    st.info(f"Say this: 'This {item_name} is our #1 gift item. It comes in a luxury box and looks twice as expensive as it actually is.'")
else:
    st.info(f"Say this: 'This {item_name} is solid and durable. You can wear it in the shower or gym, no problem.'")
