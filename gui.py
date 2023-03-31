#This GUI works for the passport.sol smart contract



import tkinter as tk
from web3 import Web3

root = tk.Tk()


# Create the GUI
class TravelLogGUI:
    def __init__(self, master):
        self.master = master
        master.title("TravelLog GUI")
        self.abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_passportID",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_passportExpirationDate",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_fullName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_countryOfResidence",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_countryOfOrigin",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_destinationCountry",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_entryDate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_plannedExitDate",
				"type": "uint256"
			}
		],
		"name": "addTravelRecord",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_passportID",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_exitDate",
				"type": "uint256"
			}
		],
		"name": "updateTravelRecord",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_passportID",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_entryDate",
				"type": "uint256"
			}
		],
		"name": "getTravelRecord",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
        #The above abi is very long, and its copied from the remix deployment page verbatum, so keep it collapsed for a cleaner view
        self.contract_address = "0x2f49fD4676F032147aEF73C188759d2c8Af36a24"
        self.network = "HTTP://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(self.network))
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        

        
        self.add_travel_record_fields = [
            ("Passport ID", str),
            ("Passport Expiration Date (Unix timestamp)", int),
            ("Full Name", str),
            ("Country of Residence", str),
            ("Country of Origin", str),
            ("Destination Country", str),
            ("Entry Date (Unix timestamp)", int),
            ("Planned Exit Date (Unix timestamp)", int)
        ]
        self.update_travel_record_fields = [
            ("Passport ID", str),
            ("Exit Date (Unix timestamp)", int)
        ]
        self.get_travel_record_fields = [
            ("Passport ID", str),
            ("Entry Date (Unix timestamp)", int)
        ]
        self.create_widgets()
    def create_widgets(self):
        self.add_travel_record_entries = []
        for field, datatype in self.add_travel_record_fields:
            frame = tk.Frame(self.master)
            frame.pack(anchor = 'w')
            label = tk.Label(frame, text=field)
            label.pack(anchor = 'w')
            entry = tk.Entry(frame)
            entry.pack(anchor = 'w')
            self.add_travel_record_entries.append((entry, datatype))

        # Create input fields for updateTravelRecord function
        self.update_travel_record_entries = []
        for field, datatype in self.update_travel_record_fields:
            frame = tk.Frame(self.master)
            frame.pack()
            label = tk.Label(frame, text=field)
            label.pack()
            entry = tk.Entry(frame)
            entry.pack()
            self.update_travel_record_entries.append((entry, datatype))

        # Create input fields for getTravelRecord function
        self.get_travel_record_entries = []
        for field, datatype in self.get_travel_record_fields:
            frame = tk.Frame(self.master)
            frame.pack(anchor = 'e')
            label = tk.Label(frame, text=field)
            label.pack(anchor = 'e')
            entry = tk.Entry(frame)
            entry.pack(anchor = 'e')
            self.get_travel_record_entries.append((entry, datatype))

        # Create buttons for each function
        self.add_travel_record_button = tk.Button(self.master, text="Add Travel Record", command=self.add_travel_record)
        self.add_travel_record_button.pack(anchor = 'w')

        self.update_travel_record_button = tk.Button(self.master, text="Update Travel Record", command=self.update_travel_record)
        self.update_travel_record_button.pack()

        self.get_travel_record_button = tk.Button(self.master, text="Get Travel Record", command=self.get_travel_record)
        self.get_travel_record_button.pack(anchor = 'e')

        # Create output area for getTravelRecord function
        self.output_text = tk.Text(self.master)
        self.output_text.pack()
    def add_travel_record(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.add_travel_record_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                values.append(int(value))
        # Call the addTravelRecord function from the smart contract with the values as arguments
        tx_hash = self.contract.functions.addTravelRecord(*values).transact({'from': '0x332F6a1F6691503855D59DB8A5fAc61789Bc99BD'})
        # Wait for the transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)

        # Clear the input fields
        #for entry in self.add_travel_record_entries:
        #    entry.delete(0, tk.END)   
        # NOT WORKING, NEED TO FIX 
        #          
    def update_travel_record(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.update_travel_record_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                values.append(int(value))
        # Call the updateTravelRecord function from the smart contract with the values as arguments
        tx_hash = self.contract.functions.updateTravelRecord(*values).transact({'from': '0x332F6a1F6691503855D59DB8A5fAc61789Bc99BD'})
        # Wait for the transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        # Clear the input fields
        for entry in self.update_travel_record_entries:
            entry.delete(0, tk.END)

    def get_travel_record(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.get_travel_record_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                values.append(int(value))
        # Call the updateTravelRecord function from the smart contract with the values as arguments
        tx_hash = self.contract.functions.getTravelRecord(*values).transact({'from': '0x332F6a1F6691503855D59DB8A5fAc61789Bc99BD'})
        # Wait for the transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        # Clear the input fields
        for entry in self.get_travel_record_entries:
            entry.delete(0, tk.END)

travel_log_gui = TravelLogGUI(root)
root.mainloop()