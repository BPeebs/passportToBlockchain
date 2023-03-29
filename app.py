import streamlit as st
import requests

# set the base URL for the API
BASE_URL = "http://localhost:8000/api"

def add_travel_record(passportID, passportExpirationDate, fullName, countryOfResidence, countryOfOrigin, destinationCountry, entryDate, plannedExitDate):
    url = BASE_URL + "/add_travel_record"
    data = {
        "passportID": passportID,
        "passportExpirationDate": passportExpirationDate,
        "fullName": fullName,
        "countryOfResidence": countryOfResidence,
        "countryOfOrigin": countryOfOrigin,
        "destinationCountry": destinationCountry,
        "entryDate": entryDate,
        "plannedExitDate": plannedExitDate
    }
    response = requests.post(url, json=data)
    return response.json()

def update_travel_record(passportID, exitDate):
    url = BASE_URL + "/update_travel_record"
    data = {
        "passportID": passportID,
        "exitDate": exitDate
    }
    response = requests.put(url, json=data)
    return response.json()

def get_travel_record(passportID, entryDate):
    url = BASE_URL + "/get_travel_record"
    params = {
        "passportID": passportID,
        "entryDate": entryDate
    }
    response = requests.get(url, params=params)
    return response.json()

# set the title and sidebar
st.set_page_config(page_title="TravelLog", page_icon=":airplane:", layout="wide")
st.sidebar.title("TravelLog Smart Contract")
st.sidebar.write("Enter the details of the travel record to add:")

# get the input from the user
passportID = st.sidebar.text_input("Passport ID")
passportExpirationDate = st.sidebar.date_input("Passport Expiration Date")
fullName = st.sidebar.text_input("Full Name")
countryOfResidence = st.sidebar.text_input("Country of Residence")
countryOfOrigin = st.sidebar.text_input("Country of Origin")
destinationCountry = st.sidebar.text_input("Destination Country")
entryDate = st.sidebar.date_input("Entry Date")
plannedExitDate = st.sidebar.date_input("Planned Exit Date")

# add the travel record to the blockchain
if st.sidebar.button("Add Travel Record"):
    response = add_travel_record(passportID, int(passportExpirationDate.timestamp()), fullName, countryOfResidence, countryOfOrigin, destinationCountry, int(entryDate.timestamp()), int(plannedExitDate.timestamp()))
    st.sidebar.write(response)

# set the main content area
st.title("TravelLog Smart Contract")
st.write("This smart contract allows you to add, update, and view travel records.")
st.write("Enter the passport ID and entry date of the travel record to view:")

# get the input from the user
passportID = st.text_input("Passport ID")
entryDate = st.date_input("Entry Date")

# get the travel record from the blockchain
if st.button("Get Travel Record"):
    response = get_travel_record(passportID, int(entryDate.timestamp()))
    st.write(response)
    
# update the travel record in the blockchain
exitDate = st.date_input("Exit Date")
if st.button("Update Travel Record"):
    response = update_travel_record(passportID, int(exitDate.timestamp()))
    st.write(response)
