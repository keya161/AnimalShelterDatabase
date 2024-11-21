import streamlit as st
import requests
from datetime import date

def create_medicine():
    """Streamlit form for creating a new medicine"""
    st.header("Add New Medicine")
    name = st.text_input("Medicine Name")
    stock = st.number_input("Initial Stock", min_value=0, value=0)
    expiry = st.date_input("Expiry Date", min_value=date.today())
    date_of_buying = st.date_input("Date of Buying", max_value=date.today())
    
    if st.button("Create Medicine"):
        if name and stock:
            payload = {
                "name": name,
                "stock": stock,
                "expiry": expiry.isoformat(),
                "date_of_buying": date_of_buying.isoformat()
            }
            try:
                response = requests.post("http://localhost:8000/medicines/", json=payload)
                response.raise_for_status()
                st.success(f"Medicine created successfully! Medicine ID: {response.json().get('medicine_id')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error creating medicine: {e}")
        else:
            st.warning("Please fill in all required fields")

def get_medicine():
    """Streamlit form for retrieving medicine details"""
    st.header("Retrieve Medicine Details")
    medicine_id = st.text_input("Enter Medicine ID (e.g., M001)")
    
    if st.button("Retrieve Medicine"):
        if medicine_id:
            try:
                response = requests.get(f"http://localhost:8000/medicines/{medicine_id}")
                response.raise_for_status()
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error retrieving medicine: {e}")
        else:
            st.warning("Please enter a Medicine ID")

def update_medicine_stock():
    st.header("Update Medicine Inventory Stock")
    
    # Form to update stock
    with st.form("update_medicine_stock_form"):
        medicine_id = st.text_input("Medicine ID", placeholder="Enter the Medicine ID to update")
        new_stock = st.number_input("New Stock", min_value=0, step=1)
        submitted = st.form_submit_button("Update Stock")
        
        if submitted:
            # Payload to send to the API
            payload = {"stock": new_stock}
            
            try:
                # Make the PUT request to update stock
                response = requests.put(f"http://localhost:8000/medicines/{medicine_id}", json=payload)
                
                if response.status_code == 200:
                    st.success("Medicine stock updated successfully!")
                    
                    # Try fetching the updated item
                    fetch_response = requests.get(f"http://localhost:8000/medicines/{medicine_id}")
                    if fetch_response.status_code == 404:
                        st.warning("The medicine was deleted due to stock depletion.")
                    else:
                        st.info("The medicine still exists in the inventory.")
                        updated_item = fetch_response.json()
                        st.write("Updated Medicine Details:")
                        st.json(updated_item)
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

def delete_medicine():
    """Streamlit form for deleting a medicine"""
    st.header("Delete Medicine")
    medicine_id = st.text_input("Enter Medicine ID to Delete")
    
    if st.button("Delete Medicine"):
        if medicine_id:
            try:
                response = requests.delete(f"http://localhost:8000/medicines/{medicine_id}")
                response.raise_for_status()
                st.success("Medicine deleted successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error deleting medicine: {e}")
        else:
            st.warning("Please enter a Medicine ID")

def update_medicine_stock():
    """Simplified stock update for volunteer role"""
    st.header("Update Medicine Stock")
    medicine_id = st.text_input("Enter Medicine ID")
    new_stock = st.number_input("New Stock Quantity", min_value=0)
    
    if st.button("Update Stock"):
        if medicine_id and new_stock >= 0:
            try:
                response = requests.put(f"http://localhost:8000/medicines/{medicine_id}?stock={new_stock}")
                response.raise_for_status()
                st.success("Stock updated successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error updating medicine stock: {e}")
        else:
            st.warning("Please enter a valid Medicine ID and stock quantity")