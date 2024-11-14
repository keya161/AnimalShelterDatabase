import streamlit as st

# Check if the user is logged in and has an 'admin' role
if "role" in st.session_state and st.session_state["role"] == "admin":
    st.title("Admin Dashboard")
    st.write("Welcome to the Admin Dashboard!")
else:
    st.write("You do not have access to this page. Please log in as an admin.")
