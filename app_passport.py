
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/passport_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

# Add a form to add a travel record
st.markdown("# Travel Log ")
st.write('# Add Travel Record')
with st.form(key='add_travel_record'):
    passport_id = st.text_input('Passport ID')
    passport_expiration_date = st.date_input('Passport Expiration Date')
    full_name = st.text_input('Full Name')
    country_of_residence = st.text_input('Country of Residence')
    country_of_origin = st.text_input('Country of Origin')
    destination_country = st.text_input('Destination Country')
    entry_date = st.date_input('Entry Date')
    planned_exit_date = st.date_input('Planned Exit Date')

    if st.form_submit_button('Submit'):
        # Call the addTravelRecord function on the contract
        tx_hash = contract.functions.addTravelRecord(
            passport_id,
            passport_expiration_date,
            full_name,
            country_of_residence,
            country_of_origin,
            destination_country,
            entry_date,
            planned_exit_date
        ).transact()

# Add a form to update a travel record
st.write('# Update Travel Record')
with st.form(key='update_travel_record'):
    passport_id = st.text_input('Passport ID')
    exit_date = st.date_input('Exit Date')

    if st.form_submit_button('Submit'):
        # Call the updateTravelRecord function on the contract
        tx_hash = contract.functions.updateTravelRecord(
            passport_id,
            exit_date
        ).transact()

# Add a form to get a travel record
st.write('# Get Travel Record')
with st.form(key='get_travel_record'):
    passport_id = st.text_input('Passport ID')
    entry_date = st.date_input('Entry Date')

    if st.form_submit_button('Submit'):
        # Call the getTravelRecord function on the contract
        tx_hash = contract.functions.getTravelRecord(
            passport_id,
            entry_date
        ).call()
   
