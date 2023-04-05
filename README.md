# BlockChain Passport

Executive Summary

The goal of our Application is intended for customs agents to use as a validation method for travelers.
The appication will consist of a solidity smart contract and python GUI application. 
This will aim to prevent illegal travel between countries and fraudulent customs reporting.
The smart contract first creates a hashed ID associated with the users passport ID. This is then used to record any exit/entry/return actions for that user.
The user cannot create multiple accounts, and cannot 'return home' to a country not listed as their residence.
The contract checks the users passport expiration and will not allow them to create an ID if its within 6 months. 

## Main points:
- Travelers are not allowed to enter a country without having a recorded exit.
- Travelers can distinguish between leaving a country, entering a foreign country, and returning home to their country of residence.
- Records the time of entry/exit/return as the blockstamp time when the contract is called, i.e. a future/past time cannot be entered
- Passport Expiration date must be 6 months from entry date 




# Technologies 
- Remix https://remix.ethereum.org/
- Solidity: https://github.com/ethereum/solidity
- Streamlit: https://streamlit.io/gallery  'pip install streamlit' 
- Web3 : https://web3py.readthedocs.io/en/stable/overview.html 'pip install web3==5.17'







