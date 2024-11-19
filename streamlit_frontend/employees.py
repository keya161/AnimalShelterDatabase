import streamlit as st
import requests
from datetime import date

# Define the base URL of your FastAPI backend
BASE_URL = "http://127.0.0.1:8000"  # Update this with your actual FastAPI backend URL

def create_employee():
    st.title("Create Employee")

    # Form to create a new employee
    with st.form(key="employee_form"):
        employee_id = st.text_input("Employee ID")
        name = st.text_input("Name")
        date_of_joining = st.date_input("Date of Joining", min_value=date(2020, 1, 1), max_value=date.today())
        role = st.selectbox("Role", ["admin", "doctor", "technician", "volunteer"])  # Assuming roles are Admin, Manager, Employee
        submit_button = st.form_submit_button(label="Create Employee")

        if submit_button:
            # Convert date_of_joining to string format 'YYYY-MM-DD'
            date_of_joining_str = date_of_joining.strftime('%Y-%m-%d')

            # API request to create the employee
            employee_data = {
                "employee_id": employee_id,
                "name": name,
                "date_of_joining": date_of_joining_str,  # Use the string representation of the date
                "role": role
            }

            # Send the employee data to the backend API
            response = requests.post(f"{BASE_URL}/employees/create", json=employee_data)
            
            if response.status_code == 200:
                st.success("Employee created successfully!")
            else:
                st.error(f"Failed to create employee: {response.text}")


# Function to view employees
def view_employees():
    st.title("View Employees")

    search_name = st.text_input("Search by name (optional)", "")
    if search_name:
        response = requests.get(f"{BASE_URL}/employees/get?name={search_name}")
    else:
        response = requests.get(f"{BASE_URL}/employees/get")

    if response.status_code == 200:
        employees = response.json()
        if employees:
            # Display employee list
            for emp in employees:
                st.write(f"**Employee ID**: {emp['employee_id']}")
                st.write(f"**Name**: {emp['name']}")
                st.write(f"**Date of Joining**: {emp['date_of_joining']}")
                st.write(f"**Role**: {emp['role']}")
                st.write("---")
        else:
            st.write("No employees found.")
    else:
        st.error(f"Failed to fetch employees: {response.text}")

