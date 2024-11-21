import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/type_count"  # Endpoint to fetch the animals by breed

def fetch_animals_by_breed():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            animals_by_breed = response.json()
            if animals_by_breed:
                return animals_by_breed
            else:
                st.write("No animal breeds found.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def display_animals_by_breed():
    animals_by_breed = fetch_animals_by_breed()
    if animals_by_breed:
        # Convert the data into a DataFrame for easier display
        df = pd.DataFrame(animals_by_breed)

        # Display the result in a table
        st.write("Number of Animals by Breed (Type):")
        st.table(df)


