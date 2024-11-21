import streamlit as st
import requests
import pandas as pd
# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/queries/animals_with_medical_records_and_adopters"

def fetch_animals_with_medical_records_and_adopters():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            animals = response.json()
            if animals:
                return animals
            else:
                st.write("No animals found.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def process_and_display_animals():
    animals = fetch_animals_with_medical_records_and_adopters()
    if animals:
        # Process the data to flatten the nested fields
        processed_data = []
        
        for animal in animals:
            # Flatten medical records
            for record in animal['medical_records']:
                record_data = {
                    "animal_id": animal["animal_id"],
                    "animal_name": animal["name"],
                    "animal_dob": animal["dob"],
                    "animal_gender": animal["gender"],
                    "record_name": record["name"],
                    "record_report": record["diagnosis"],
                    "record_medicine": record["medicine"],
                    "record_follow_up": record["follow_up"],
                }
                # Flatten adopters
                for adopter in animal['adopters']:
                    adopter_data = record_data.copy()
                    adopter_data.update({
                        "adopter_name": adopter["name"],
                        "adopter_contribution": adopter["contribution"],
                    })
                    processed_data.append(adopter_data)

        # Convert the processed data into a DataFrame
        df = pd.DataFrame(processed_data)

        # Display the processed data as a table
        st.write("Animals with Medical Records and Adopters:")
        st.table(df)
