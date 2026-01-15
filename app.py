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

# 4. The Visuals (Stable Images)
if recommendation == "Thin Box Chain":
    st.image("https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400", caption="Thin Silver Chain")

elif recommendation == "3mm Rope Chain":
    st.image("https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400", caption="Gold Rope Chain")

elif recommendation == "Diamond Cross Pendant":
    st.image("https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=400", caption="Diamond Pendant")

elif recommendation == "Moissanite Tennis Bracelet":
    st.image("https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400", caption="Moissanite Bracelet")

elif recommendation == "Real Diamond Tennis Bracelet":
    st.image("https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=400", caption="Real Diamond Tennis Bracelet")
