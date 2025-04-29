import streamlit as st

# Page Title
st.title("🚀 Smart Content System Demo")

# Section Header
st.header("Welcome to your first Streamlit app!")

# Text Write
st.write("This is a mini dashboard powered by Streamlit + Python.")

# User Input Example
user_input = st.text_input("Enter a topic for your blog post:")

if user_input:
    st.success(f"Awesome! You entered: {user_input}")

# Button Example
if st.button("Generate Example Blog Intro"):
    st.info(f"Here's a blog intro for: **{user_input}**")
    st.write(f"Are you curious about {user_input}? Let's dive deep into the insights and exciting details that await you.")

# Footer
st.caption("Built with ❤️ by Elizabeth Clinen")