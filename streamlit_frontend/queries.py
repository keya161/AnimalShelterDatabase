import streamlit as st
import requests
import pandas as pd

# Define the base URL for your FastAPI backend
API_URL = "http://127.0.0.1:8000/queries"

# Function to fetch animals without medical records
def get_animals_without_medical_records():
    try:
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            animals = response.json()
            return animals
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Streamlit frontend code
st.title("Animal Shelter Database")

# Button to fetch animals without medical records
if st.button("Get Animals Without Medical Records"):
    animals = get_animals_without_medical_records()
    
    if animals:
        # Create a DataFrame to display animals in tabular form
        df = pd.DataFrame(animals)
        
        # Show the DataFrame as a table
        st.table(df)
    else:
        st.write("No animals without medical records found.")
