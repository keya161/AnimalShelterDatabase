import streamlit as st
import requests

# Base URL for the food inventory API
BASE_URL = "http://localhost:8000/food_inventory"

# Function to add a new food inventory item
def add_food_inventory():
    st.header("Add a New Food Inventory Item")
    with st.form("add_food_inventory_form"):
        food_type = st.text_input("Food Type")
        stock = st.number_input("Stock", min_value=0, step=1)
        cost_per_kg = st.number_input("Cost per KG", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Add Food Item")

        if submitted:
            payload = {
                "type": food_type,
                "stock": stock,
                "cost_per_kg": cost_per_kg
            }
            response = requests.post(f"{BASE_URL}/", json=payload)
            if response.status_code == 200:
                st.success("Food Inventory Item added successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# Function to get details of a food inventory item
def get_food_inventory():
    st.header("Get Food Inventory Details")
    food_id = st.text_input("Enter Food ID to fetch details")
    if st.button("Get Food Item"):
        response = requests.get(f"{BASE_URL}/{food_id}")
        if response.status_code == 200:
            food_item = response.json()
            st.write(f"Food ID: {food_item['food_id']}")
            st.write(f"Type: {food_item['type']}")
            st.write(f"Stock: {food_item['stock']}")
            st.write(f"Cost per KG: {food_item['cost_per_kg']}")
        else:
            st.error(f"Error: {response.json().get('detail', 'Food item not found')}")

# Function to update details of an existing food inventory item
def update_food_inventory():
    st.header("Update Food Inventory Item")
    with st.form("update_food_inventory_form"):
        food_id = st.text_input("Food ID to update")
        new_food_type = st.text_input("New Food Type")
        new_stock = st.number_input("New Stock", min_value=0, step=1)
        new_cost_per_kg = st.number_input("New Cost per KG", min_value=0.0, step=0.1)
        update_submitted = st.form_submit_button("Update Food Item")

        if update_submitted:
            payload = {
                "type": new_food_type,
                "stock": new_stock,
                "cost_per_kg": new_cost_per_kg
            }
            response = requests.put(f"{BASE_URL}/{food_id}", json=payload)
            if response.status_code == 200:
                st.success("Food Inventory Item updated successfully!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Food item not found')}")

# Function to delete a food inventory item
def delete_food_inventory():
    st.header("Delete Food Inventory Item")
    food_id = st.text_input("Food ID to delete")
    if st.button("Delete Food Item"):
        response = requests.delete(f"{BASE_URL}/{food_id}")
        if response.status_code == 200:
            st.success("Food Inventory Item deleted successfully!")
        else:
            st.error(f"Error: {response.json().get('detail', 'Food item not found')}")

# # Main function to display the frontend menu
# def main():
#     st.title("Food Inventory Management")

#     menu = ["View Food Inventory", "Add Food Item", "Update Food Item", "Delete Food Item"]
#     choice = st.sidebar.selectbox("Select Action", menu)

#     if choice == "View Food Inventory":
#         get_food_inventory()
#     elif choice == "Add Food Item":
#         add_food_inventory()
#     elif choice == "Update Food Item":
#         update_food_inventory()
#     elif choice == "Delete Food Item":
#         delete_food_inventory()

# if __name__ == "__main__":
#     main()
