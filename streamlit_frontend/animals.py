import streamlit as st
import requests

BASE_URL = "http://localhost:8000/animals"

def add_animal():
    st.header("Add a New Animal")
    with st.form("add_animal_form"):
        name = st.text_input("Name")
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["M", "F"])
        passive_adopter = st.text_input("Passive Adopter")
        breed_id = st.text_input("Breed ID")
        submitted = st.form_submit_button("Add Animal")

        if submitted:
            payload = {
                "name": name,
                "dob": str(dob),
                "gender": gender,
                "passive_adopter": passive_adopter,
                "breed_id": breed_id
            }
            response = requests.post(f"{BASE_URL}/", json=payload)
            if response.status_code == 200:
                st.success("Animal added successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
def get_animal():
    st.header("Get Animal Details")
    animal_id = st.text_input("Enter Animal ID to fetch details")
    if st.button("Get Animal"):
        response = requests.get(f"{BASE_URL}/{animal_id}")
        if response.status_code == 200:
            animal = response.json()
            st.write(f"Name: {animal['name']}")
            st.write(f"Date of Birth: {animal['dob']}")
            st.write(f"Gender: {animal['gender']}")
            st.write(f"Passive Adopter: {animal['passive_adopter']}")
            st.write(f"Breed ID: {animal['breed_id']}")
        else:
            st.error(f"Error: {response.json().get('detail', 'Animal not found')}")
            
def update_animal():
    st.header("Update Animal Details")
    with st.form("update_animal_form"):
        update_animal_id = st.text_input("Animal ID to update")
        new_name = st.text_input("New Name")
        new_dob = st.date_input("New Date of Birth")
        new_gender = st.selectbox("New Gender", ["M", "F"])
        new_passive_adopter = st.text_input("New Passive Adopter")
        new_breed_id = st.text_input("New Breed ID")
        update_submitted = st.form_submit_button("Update Animal")

        if update_submitted:
            payload = {
                "name": new_name,
                "dob": str(new_dob),
                "gender": new_gender,
                "passive_adopter": new_passive_adopter,
                "breed_id": new_breed_id
            }
            response = requests.put(f"{BASE_URL}/{update_animal_id}", json=payload)
            if response.status_code == 200:
                st.success("Animal updated successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Animal not found')}")
                
def delete_animal():
    st.header("Delete Animal")
    delete_animal_id = st.text_input("Animal ID to delete")
    if st.button("Delete Animal"):
        response = requests.delete(f"{BASE_URL}/{delete_animal_id}")
        if response.status_code == 200:
            st.success("Animal deleted successfully!")
        else:
            st.error(f"Error: {response.json().get('detail', 'Animal not found')}")