import streamlit as st
import requests

# Base URL for the medical inventory API
BASE_URL = "http://localhost:8000/medicine_inventory"

# Function to add a new medical inventory item
def add_medical_inventory():
    st.header("Add a New Medical Inventory Item")
    with st.form("add_medical_inventory_form"):
        name = st.text_input("Medicine Name")
        stock = st.number_input("Stock", min_value=0, step=1)
        expiry = st.date_input("Expiry Date")
        date_of_buying = st.date_input("Date of Buying")
        submitted = st.form_submit_button("Add Medicine")

        if submitted:
            payload = {
                "name": name,
                "stock": stock,
                "expiry": str(expiry),
                "date_of_buying": str(date_of_buying)
            }
            response = requests.post(f"{BASE_URL}/", json=payload)
            if response.status_code == 200:
                st.success("Medical Inventory Item added successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# Function to get details of a medical inventory item
def get_medical_inventory():
    st.header("Get Medical Inventory Details")
    medicine_id = st.text_input("Enter Medicine ID to fetch details")
    if st.button("Get Medicine Item"):
        response = requests.get(f"{BASE_URL}/{medicine_id}")
        if response.status_code == 200:
            medicine_item = response.json()
            st.write(f"Medicine ID: {medicine_item['medicine_id']}")
            st.write(f"Name: {medicine_item['name']}")
            st.write(f"Stock: {medicine_item['stock']}")
            st.write(f"Expiry Date: {medicine_item['expiry']}")
            st.write(f"Date of Buying: {medicine_item['date_of_buying']}")
        else:
            st.error(f"Error: {response.json().get('detail', 'Medicine item not found')}")

# Function to update details of an existing medical inventory item
def update_medical_inventory():
    st.header("Update Medical Inventory Item")
    with st.form("update_medical_inventory_form"):
        medicine_id = st.text_input("Medicine ID to update")
        new_name = st.text_input("New Medicine Name")
        new_stock = st.number_input("New Stock", min_value=0, step=1)
        new_expiry = st.date_input("New Expiry Date")
        new_date_of_buying = st.date_input("New Date of Buying")
        update_submitted = st.form_submit_button("Update Medicine Item")

        if update_submitted:
            payload = {
                "name": new_name,
                "stock": new_stock,
                "expiry": str(new_expiry),
                "date_of_buying": str(new_date_of_buying)
            }
            response = requests.put(f"{BASE_URL}/{medicine_id}", json=payload)
            if response.status_code == 200:
                st.success("Medical Inventory Item updated successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Medicine item not found')}")

# Function to delete a medical inventory item
def delete_medical_inventory():
    st.head
