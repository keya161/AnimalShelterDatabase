import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000/adopters"  # Adjust this if your FastAPI backend is running on a different port

def add_adopter():
    st.header("Add a New Adopter")
    with st.form("add_adopter_form"):
        # adopter_id = st.text_input("Adopter ID")
        name = st.text_input("Name")
        animal_id = st.text_input("Animal ID")
        contribution = st.number_input("Contribution", min_value=0.0, step=100.0, format="%.2f")
        submitted = st.form_submit_button("Add Adopter")

        if submitted:
            payload = {
                # "adopter_id": adopter_id,
                "name": name,
                "animal_id": animal_id,
                "contribution": contribution
            }
            response = requests.post(f"{BASE_URL}/", json=payload)
            if str(response.status_code).startswith('2'):
                st.success("Adopter added successfully!")
            elif response.status_code == 404:
                st.error("Error: Animal not found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
            # else:
            #     st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
def get_adopter():
    st.header("Get Adopter Details")
    adopter_id = st.text_input("Enter Adopter ID to fetch details")
    if st.button("Get Adopter"):
        response = requests.get(f"{BASE_URL}/{adopter_id}")
        if response.status_code == 200:
            adopter = response.json()
            st.write(f"Adopter ID: {adopter['adopter_id']}")
            st.write(f"Name: {adopter['name']}")
            st.write(f"Animal ID: {adopter['animal_id']}")
            st.write(f"Contribution: {adopter['contribution']}")
        else:
            st.error(f"Error: {response.json().get('detail', 'Adopter not found')}")

def update_adopter():
    st.header("Update Adopter Details")
    with st.form("update_adopter_form"):
        update_adopter_id = st.text_input("Adopter ID to update")
        new_name = st.text_input("New Name")
        new_animal_id = st.text_input("New Animal ID")
        new_contribution = st.number_input("New Contribution", min_value=0.0, step=0.01)
        update_submitted = st.form_submit_button("Update Adopter")

        if update_submitted:
            payload = {
                "adopter_id": update_adopter_id,
                "name": new_name,
                "animal_id": new_animal_id,
                "contribution": new_contribution
            }
            response = requests.put(f"{BASE_URL}/{update_adopter_id}", json=payload)
            if response.status_code == 200:
                st.success("Adopter updated successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Adopter not found')}")
                
def delete_adopter():
    st.header("Delete Adopter")
    delete_adopter_id = st.text_input("Adopter ID to delete")
    if st.button("Delete Adopter"):
        response = requests.delete(f"{BASE_URL}/{delete_adopter_id}")
        if response.status_code == 200:
            st.success("Adopter deleted successfully!")
        else:
            st.error(f"Error: {response.json().get('detail', 'Adopter not found')}")
