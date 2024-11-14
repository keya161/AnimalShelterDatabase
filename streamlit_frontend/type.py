import streamlit as st
import requests

BASE_URL = "http://localhost:8000/types"

def add_type():
    st.header("Add a New Type")
    with st.form("add_type_form"):
        type_id = st.text_input("Type ID")
        breed = st.text_input("Breed")
        feed_id = st.number_input("Feed ID", min_value=1, step=1)
        freq_of_checkup = st.number_input("Frequency of Checkup", min_value=1, max_value=365)
        bath = st.date_input("Bath Date (Optional)", help="Leave empty if not applicable")
        submitted = st.form_submit_button("Add Type")

        if submitted:
            payload = {
                "type_id": type_id,
                "breed": breed,
                "feed_id": feed_id,
                "freq_of_checkup": freq_of_checkup,
                "bath": str(bath) if bath else None
            }
            response = requests.post(f"{BASE_URL}/", json=payload)
            if response.status_code == 200:
                st.success("Type added successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                st.write(response.text)

def get_type():
    st.header("Get Type Details")
    type_id = st.text_input("Enter Type ID to fetch details")
    if st.button("Get Type"):
        response = requests.get(f"{BASE_URL}/{type_id}")
        if response.status_code == 200:
            type_record = response.json()
            st.write(f"Type ID: {type_record['type_id']}")
            st.write(f"Breed: {type_record['breed']}")
            st.write(f"Feed ID: {type_record['feed_id']}")
            st.write(f"Frequency of Checkup: {type_record['freq_of_checkup']}")
            st.write(f"Bath Date: {type_record['bath'] if type_record['bath'] else 'N/A'}")
        else:
            st.error(f"Error: {response.json().get('detail', 'Type not found')}")

def update_type():
    st.header("Update Type Details")
    with st.form("update_type_form"):
        type_id = st.text_input("Type ID to update")
        new_breed = st.text_input("New Breed")
        new_feed_id = st.number_input("New Feed ID", min_value=1, step=1)
        new_freq_of_checkup = st.number_input("New Frequency of Checkup", min_value=1, max_value=365)
        new_bath = st.date_input("New Bath Date (Optional)", help="Leave empty if not applicable")
        update_submitted = st.form_submit_button("Update Type")

        if update_submitted:
            payload = {
                "breed": new_breed,
                "feed_id": new_feed_id,
                "freq_of_checkup": new_freq_of_checkup,
                "bath": str(new_bath) if new_bath else None
            }
            response = requests.put(f"{BASE_URL}/{type_id}", json=payload)
            if response.status_code == 200:
                st.success("Type updated successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Type not found')}")

def delete_type():
    st.header("Delete Type")
    type_id = st.text_input("Type ID to delete")
    if st.button("Delete Type"):
        response = requests.delete(f"{BASE_URL}/{type_id}")
        if response.status_code == 200:
            st.success("Type deleted successfully!")
        else:
            st.error(f"Error: {response.json().get('detail', 'Type not found')}")
