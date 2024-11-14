import streamlit as st
import requests

# FastAPI backend URL
BASE_URL = "http://localhost:8000/auth"  # Replace with your FastAPI server URL

# Function to login
def login(username, password):
    try:
        # Send login request to FastAPI backend
        response = requests.post(f"{BASE_URL}/login", data={"username": username, "password": password})
        if response.status_code == 200:
            return response.json()  # Return JWT token and user details
        else:
            st.error("Invalid username or password")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Function to register a new user
def register(employee_id, username, password):
    try:
        # Send registration request to FastAPI backend
        response = requests.post(f"{BASE_URL}/register", json={
            "employee_id": employee_id,
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            st.success("User registered successfully!")
        else:
            st.error("Error registering user")
    except Exception as e:
        st.error(f"Error: {str(e)}")