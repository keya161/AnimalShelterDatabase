import streamlit as st
import requests
import pandas as pd

BASE_URL = "http://localhost:8000/animaldetails"

def get_animal_by_name():
    st.header("Get Animal Details by Name")
    animal_name = st.text_input("Enter Animal Name to fetch details")
    
    if st.button("Get Animal by Name"):
        # Make a GET request to the appropriate endpoint
        response = requests.get(f"{BASE_URL}/{animal_name}")
        
        if response.status_code == 200:
            animal_details = response.json()
            st.write(f"**Animal ID**: {animal_details['animal_id']}")
            st.write(f"**Name**: {animal_details['name']}")
            st.write(f"**Breed**: {animal_details['breed']}")
            
            # Display medical records in a table format
            st.write("**Medical Records:**")
            if animal_details['medical_records']:
                medical_records = []
                for record in animal_details['medical_records']:
                    medical_records.append({
                        "Record ID": record['record_id'],
                        "Doctor": record['doctor'],
                        "Date": record['date'],
                        "Diagnosis": record['diagnosis'],
                        "Medicine": record['medicine']
                    })
                # Convert to DataFrame and display as a table
                st.table(pd.DataFrame(medical_records))
            else:
                st.write("No medical records found.")
            
            # Display adopters in a table format
            st.write("**Adopter:**")
            if animal_details['passive_adopter']:
                adopters = []
                for adopter in animal_details['passive_adopter']:
                    adopters.append({
                        "Adopter ID": adopter['adopter_id'],
                        "Name": adopter['name'],
                        "Contribution": adopter['contribution']
                    })
                # Convert to DataFrame and display as a table
                st.table(pd.DataFrame(adopters))
            else:
                st.write("No adopters found.")
        else:
            st.error(f"Error: {response.json().get('detail', 'Animal not found')}")
