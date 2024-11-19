import streamlit as st
from datetime import date, datetime

import requests

BASE_URL = "http://localhost:8000"

def add_record():
    st.title("Add a Medical Record")

    with st.form(key="record_form"):
        name = st.text_input("Name")
        report = st.text_input("Report")
        doctor = st.text_input("Doctor Name")
        diagnosis = st.text_input("Diagnosis")
        medicine = st.text_input("Medicine")
        followUp = st.date_input("Date for follow up", min_value=date.today())
        freq = st.number_input("Frequency of usage")
        submit_button = st.form_submit_button(label="Add Record")

        if submit_button:
            # Convert date_of_joining to string format 'YYYY-MM-DD'
            followUp = followUp.strftime('%Y-%m-%d')
            datet = datetime.now().strftime('%Y-%m-%d')

            # datet = date.strftime('%Y-%m-%d')
            # API request to create the employee
            record_data = {
                "name": name,
                "report": report,
                "doctor": doctor,
                "date": datet,
                "diagnosis": diagnosis,
                "medicine":  medicine,
                "follow_up": followUp,
                "freq_of_usage": freq
            }

            # Send the employee data to the backend API
            response = requests.post(f"{BASE_URL}/medical-records/create", json=record_data)
            
            if response.status_code == 200:
                st.success("Record added successfully!")
            else:
                st.error(f"Failed to add record: {response.text}")


# Function to view employees
def view_records():
    st.title("View All Records")

    search_name = st.text_input("Search by name (optional)", "")
    if search_name:
        response = requests.get(f"{BASE_URL}/medical-records/get?name={search_name}")
    else:
        response = requests.get(f"{BASE_URL}/medical-records/get")

    if response.status_code == 200:
        record = response.json()
        if record:
            # Display employee list
            for r in record:
                st.write(f"**Name**: {r['name']}")
                st.write(f"**Report**: {r['report']}")
                st.write(f"**Doctor**: {r['doctor']}")
                st.write(f"**Date of checkup**: {r['date']}")
                st.write(f"**Diagnosis**: {r['diagnosis']}")
                st.write(f"**Medicine**: {r['medicine']}")
                st.write(f"**Date of follow up**: {r['follow_up']}")
                st.write(f"**Frequency of use**: {r['freq_of_usage']}")
                st.write("---")
        else:
            st.write("No records found.")
    else:
        st.error(f"Failed to fetch records: {response.text}")


