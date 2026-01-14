import streamlit as st

st.title("💎 Faraz Jewelry Sales Tool")

# 1. Ask the Questions
budget = st.selectbox("What is the Customer's Budget?", ["$100", "$500", "$1000", "$5000+"])
metal = st.selectbox("What Metal do they like?", ["Silver", "Gold", "Rose Gold", "Platinum"])
style = st.selectbox("What Style?", ["Simple", "Iced Out", "Classic"])

# 2. Show the Selection (Testing)
st.write("---")
st.write(f"**Customer wants:** {metal} in {style} style for {budget}.")

# 3. Simple Recommendation Logic (We will make this smarter later)
if budget == "$5000+":
    st.success("Recommendation: Show the Diamond Tennis Bracelet!")
elif budget == "$100":
    st.info("Recommendation: Show the Silver Stud Earrings.")
else:
    st.warning("Recommendation: Show the Gold Chain.")
