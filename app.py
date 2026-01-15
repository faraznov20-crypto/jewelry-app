import streamlit as st

st.set_page_config(page_title="Faraz Jewelry AI", page_icon="💎")

st.title("💎 Faraz Jewelry Sales Tool")

# 1. Ask the Questions
budget = st.selectbox("What is the Customer's Budget?", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.selectbox("What Metal do they like?", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.selectbox("What Style?", ["Simple", "Classic", "Iced Out"])

# 2. The Logic (Your 5 Rules)
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

# 3. Show the Result
st.write("---")
st.header("Recommended Item:")
st.success(f"**{recommendation}**")

# 4. The Visuals (Selling the Dream)
if recommendation == "Thin Box Chain":
    st.image("https://m.media-amazon.com/images/I/51b+I0sS+QL._AC_UY1100_.jpg", width=300)

elif recommendation == "3mm Rope Chain":
    st.image("https://m.media-amazon.com/images/I/61F9kL-xLcL._AC_UY1100_.jpg", width=300)

elif recommendation == "Diamond Cross Pendant":
    st.image("https://m.media-amazon.com/images/I/61Z+2u+qLgL._AC_UY1000_.jpg", width=300)

elif recommendation == "Moissanite Tennis Bracelet":
    st.image("https://m.media-amazon.com/images/I/71w-w-q-GgL._AC_UY1000_.jpg", width=300)

elif recommendation == "Real Diamond Tennis Bracelet":
    st.image("https://m.media-amazon.com/images/I/71rQ6Q01m+L._AC_UY1000_.jpg", width=300)
