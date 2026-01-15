import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="Faraz Jewelry AI", page_icon="💎", layout="centered")

st.title("💎 Faraz Jewelry Sales Tool")

# ---------- Helpers ----------
def placeholder_image(text: str) -> str:
    """
    Stable image that always loads.
    Shows a clean image with the item name written on it.
    """
    t = quote(text)
    return f"https://placehold.co/900x600?text={t}"

def sales_script(item_name: str, budget: str, metal: str, occasion: str) -> str:
    if occasion == "Gift":
        return f"Say this: 'This {item_name} is a best-seller gift. It looks expensive and comes ready to gift. Perfect for your {budget} budget.'"
    if occasion == "Special Event":
        return f"Say this: 'This {item_name} will catch light and stand out. Great choice for a special event.'"
    # Daily Wear
    return f"Say this: 'This {item_name} is durable for daily wear. Comfortable, strong, and easy to style.'"

# ---------- Sidebar Inputs ----------
st.sidebar.header("Customer Details")
budget = st.sidebar.selectbox("Budget", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.sidebar.selectbox("Metal", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.sidebar.selectbox("Style", ["Simple", "Classic", "Iced Out"])
occasion = st.sidebar.selectbox("Occasion", ["Daily Wear", "Gift", "Special Event"])

st.write(f"**Budget:** {budget} | **Metal:** {metal} | **Style:** {style} | **Occasion:** {occasion}")

# ---------- Recommendation Logic (Simple + Predictable) ----------
# Default safe pick
item_name = "3mm Rope Chain"
image_url = placeholder_image(item_name)
upsell = None

# Your original 5 rules (clean + consistent)
if budget == "$100" and metal == "Silver":
    item_name = "Thin Box Chain"
    image_url = placeholder_image(item_name)

elif budget == "$500" and metal == "Gold":
    item_name = "3mm Rope Chain"
    image_url = placeholder_image(item_name)

elif budget == "$1000" and style == "Iced Out":
    item_name = "Diamond Cross Pendant"
    image_url = placeholder_image(item_name)

elif budget == "$1000+" and style == "Classic":
    item_name = "Moissanite Tennis Bracelet"
    image_url = placeholder_image(item_name)

elif budget == "$5000+":
    item_name = "Real Diamond Tennis Bracelet"
    image_url = placeholder_image(item_name)

# Style override (so “Iced Out” always feels iced out)
# BUT if budget is $5000+, keep the diamond bracelet as main and suggest the pendant as upsell.
if style == "Iced Out" and budget == "$5000+":
    upsell = "Diamond Cross Pendant"
elif style == "Iced Out" and budget != "$5000+":
    item_name = "Diamond Cross Pendant"
    image_url = placeholder_image(item_name)

# ---------- Display ----------
st.write("---")
st.header("Recommended Item:")
st.success(f"**{item_name}**")

st.image(image_url, caption=item_name, use_container_width=True)

if upsell:
    st.info(f"Upsell idea: Also show **{upsell}** (iced-out option).")

st.write("---")
st.subheader("🗣️ Sales Script")
st.info(sales_script(item_name, budget, metal, occasion))
