import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change to deployed URL if hosted

st.set_page_config(page_title="Patient Management System", layout="wide")

st.title("🏥 Patient Management System")

menu = st.sidebar.selectbox("Menu", ["Home", "View All", "View Patient", "Add Patient", "Edit Patient", "Delete Patient", "Sort Patients"])

if menu == "Home":
    response = requests.get(f"{API_URL}/")
    st.info(response.json()['message'])

elif menu == "View All":
    response = requests.get(f"{API_URL}/view")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Unable to fetch patients.")

elif menu == "View Patient":
    pid = st.text_input("Enter Patient ID:")
    if st.button("View"):
        response = requests.get(f"{API_URL}/patient/{pid}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.json()['detail'])

elif menu == "Add Patient":
    with st.form("add_form"):
        pid = st.text_input("Patient ID (e.g., P001)")
        name = st.text_input("Name")
        city = st.text_input("City")
        age = st.number_input("Age", 1, 120)
        gender = st.selectbox("Gender", ["male", "female", "others"])
        height = st.number_input("Height (in meters)", 0.1, 3.0)
        weight = st.number_input("Weight (in kg)", 1.0, 500.0)
        submit = st.form_submit_button("Add Patient")

        if submit:
            patient_data = {
                "id": pid,
                "name": name,
                "city": city,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight
            }
            response = requests.post(f"{API_URL}/create", json=patient_data)
            if response.status_code == 201:
                st.success("Patient added successfully!")
            else:
                st.error(response.json()['detail'])

elif menu == "Edit Patient":
    pid = st.text_input("Enter Patient ID to Edit:")
    if pid:
        response = requests.get(f"{API_URL}/patient/{pid}")
        if response.status_code == 200:
            patient = response.json()
            with st.form("edit_form"):
                name = st.text_input("Name", value=patient['name'])
                city = st.text_input("City", value=patient['city'])
                age = st.number_input("Age", 1, 120, value=patient['age'])
                gender = st.selectbox("Gender", ["male", "female", "others"], index=["male", "female", "others"].index(patient['gender']))
                height = st.number_input("Height (in meters)", 0.1, 3.0, value=patient['height'])
                weight = st.number_input("Weight (in kg)", 1.0, 500.0, value=patient['weight'])
                update = st.form_submit_button("Update Patient")

                if update:
                    update_data = {
                        "name": name,
                        "city": city,
                        "age": age,
                        "gender": gender,
                        "height": height,
                        "weight": weight
                    }
                    response = requests.put(f"{API_URL}/edit/{pid}", json=update_data)
                    if response.status_code == 200:
                        st.success("Patient updated successfully!")
                    else:
                        st.error(response.json()['detail'])
        else:
            st.error(response.json()['detail'])

elif menu == "Delete Patient":
    pid = st.text_input("Enter Patient ID to Delete:")
    if st.button("Delete"):
        response = requests.delete(f"{API_URL}/delete/{pid}")
        if response.status_code == 200:
            st.success("Patient deleted successfully!")
        else:
            st.error(response.json()['detail'])

elif menu == "Sort Patients":
    sort_by = st.selectbox("Sort by", ["height", "weight", "bmi"])
    order = st.radio("Order", ["asc", "desc"])
    if st.button("Sort"):
        response = requests.get(f"{API_URL}/sort", params={"sort_by": sort_by, "order": order})
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.json()['detail'])
