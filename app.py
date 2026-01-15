import streamlit as st

st.title("💎 Faraz Jewelry Sales Tool")

# 1. Ask the Questions
budget = st.selectbox("What is the Customer's Budget?", ["$100", "$500", "$1000", "$1000+", "$5000+"])
metal = st.selectbox("What Metal do they like?", ["Silver", "Gold", "White Gold", "Rose Gold"])
style = st.selectbox("What Style?", ["Simple", "Classic", "Iced Out"])

# 2. The Logic (Your 5 Rules)
recommendation = "Ask Manager for Help" # This is the default answer

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
