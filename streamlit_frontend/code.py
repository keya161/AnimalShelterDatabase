import streamlit as st
from animals import add_animal, get_animal, update_animal, delete_animal
from auth import login, register
from type import add_type, get_type, update_type, delete_type
from food import add_food_inventory, get_food_inventory, update_food_inventory, delete_food_inventory
from employees import create_employee, view_employees
import admin

# FastAPI backend URL
BASE_URL = "http://localhost:8000/auth"  # Replace with your FastAPI server URL

# Page navigation
page = st.sidebar.selectbox("Choose an option", ["Login", "Register"])

# Admin dashboard
if "role" in st.session_state and st.session_state["role"] == "admin":
    st.title("Admin Dashboard")
    st.write("Welcome to the Admin Dashboard!")

    # Create two separate selectboxes: one for animals, and one for types
    option1 = st.sidebar.selectbox("Animals:", ["Select Action", "Add Animal", "Get Animal", "Update Animal", "Delete Animal"])
    option2 = st.sidebar.selectbox("Types:", ["Select Action", "Add Type", "Get Type", "Update Type", "Delete Type"])
    option3 = st.sidebar.selectbox("Food Inventory:", ["Select Action", "Add Food Type", "Get Food Type", "Update Food Type", "Delete Food Type"])
    option4 = st.sidebar.selectbox("Employees:", ("Select Action","Create Employee", "View Employees"))


    # Show only the relevant content based on the selection
    if option1 == "Add Animal":
        add_animal()
    elif option1 == "Get Animal":
        get_animal()
    elif option1 == "Update Animal":
        update_animal()
    elif option1 == "Delete Animal":
        delete_animal()

    if option2 == "Add Type":
        add_type()
    elif option2 == "Get Type":
        get_type()
    elif option2 == "Update Type":
        update_type()
    elif option2 == "Delete Type":
        delete_type()
        
    #food     
    if option3 == "Add Food Type":
        add_food_inventory()
    elif option3 == "Get Food Type":
        get_food_inventory()
    elif option3 == "Update Food Type":
        update_food_inventory()
    elif option3 == "Delete Food Type":
        delete_food_inventory()
        
    #employee creation
    # Execute the corresponding function based on the selection
    if option4 == "Create Employee":
        create_employee()
    elif option4 == "View Employees":
        view_employees()

# If logged in as a regular user, show the regular user options
elif "role" in st.session_state and st.session_state["role"] != "admin":
    st.title("User Dashboard")
    st.write("Welcome to the User Dashboard!")
    option = st.sidebar.selectbox("Choose an action", ["Add Animal", "Get Animal", "Update Animal", "Delete Animal"])


# Handle Login Page
elif page == "Login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username and password:
            login_result = login(username, password)
            if login_result:
                st.session_state["token"] = login_result["access_token"]
                st.session_state["role"] = login_result["role"]
                st.session_state["employee_id"] = login_result["employee_id"]
                
                # Check role and navigate accordingly
                if st.session_state["role"] == "admin":
                    st.success("Login successful! Welcome, Admin.")
                    # Redirect to admin page by rerunning the app
                    st.rerun()
                else:
                    st.success("Login successful! You're logged in as a regular user.")
                    # Allow regular user actions (animal CRUD operations)
                    st.rerun()  # This will refresh the app and show the CRUD options
            else:
                st.error("Invalid credentials. Please try again.")

# Handle Register Page
elif page == "Register":
    st.title("Register")
    employee_id = st.text_input("Employee ID")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        if employee_id and username and password:
            register(employee_id, username, password)
            st.success("User registered successfully!")
        else:
            st.error("Please fill in all fields.")


else:
    # If the user is not logged in, show login/register options
    st.write("Please log in to access the app.")
