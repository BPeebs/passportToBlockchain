#This GUI works for the passport.sol smart contract

from pathlib import Path
import json
import tkinter as tk
from web3 import Web3
from dateutil.parser import parse
from dateutil import tz
import datetime



root = tk.Tk()


# Create the GUI
class TravelLogGUI:
    def __init__(self, master):
        self.master = master
        master.title("TravelLog GUI")
        with open(Path(r'C:\Users\ajcth\Documents\GitHub\Passport_To_Blockchain\passport_abi.json')) as f:
            self.abi = json.load(f)
        self.contract_address = "0x03743299B5f93C7cA1806BBa48AbD04a3548fc0D"
        self.network = "HTTP://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(self.network))
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        

        
        self.add_travel_record_fields = [
            ("Passport ID", str),
            ("Passport Expiration Date (DD/MM/YYYY)", int),
            ("Full Name", str),
            ("Country of Residence", str),
            ("Country of Origin", str),
            ("Destination Country", str),
            ("Entry Date (DD/MM/YYYY)", int),
            ("Planned Exit Date (DD/MM/YYYY)", int)
        ]
        self.update_travel_record_fields = [
            ("Passport ID", str),
        ]
        self.get_travel_record_fields = [
            ("Passport ID", str),
        ]
        self.create_widgets()
    def create_widgets(self):

        self.add_travel_record_frame = tk.LabelFrame(self.master, text="Add Travel Record")
        self.add_travel_record_frame.pack()

        self.update_travel_record_frame = tk.LabelFrame(self.master, text="Update Travel Record")
        self.update_travel_record_frame.pack()

        self.get_travel_record_frame = tk.LabelFrame(self.master, text="Get Travel Record")
        self.get_travel_record_frame.pack()


        self.add_travel_record_entries = []
        for field, datatype in self.add_travel_record_fields:
            frame = tk.Frame(self.add_travel_record_frame)
            frame.pack()
            label = tk.Label(frame, text=field)
            label.pack()
            entry = tk.Entry(frame)
            entry.pack()
            self.add_travel_record_entries.append((entry, datatype))

        # Create input fields for updateTravelRecord function
        self.update_travel_record_entries = []
        for field, datatype in self.update_travel_record_fields:
            frame = tk.Frame(self.update_travel_record_frame)
            frame.pack()
            label = tk.Label(frame, text=field)
            label.pack()
            entry = tk.Entry(frame)
            entry.pack()
            self.update_travel_record_entries.append((entry, datatype))

        # Create input fields for getTravelRecord function
        self.get_travel_record_entries = []
        for field, datatype in self.get_travel_record_fields:
            frame = tk.Frame(self.get_travel_record_frame)
            frame.pack()
            label = tk.Label(frame, text=field)
            label.pack()
            entry = tk.Entry(frame)
            entry.pack()
            self.get_travel_record_entries.append((entry, datatype))

        # Create buttons for each function
        self.add_travel_record_button = tk.Button(self.add_travel_record_frame, text="Add Travel Record", command=self.add_travel_record)
        self.add_travel_record_button.pack()

        self.update_travel_record_button = tk.Button(self.update_travel_record_frame, text="Update Travel Record", command=self.update_travel_record)
        self.update_travel_record_button.pack()

        self.get_travel_record_button = tk.Button(self.get_travel_record_frame, text="Get Travel Record", command=self.get_travel_record)
        self.get_travel_record_button.pack()

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
                # Convert date string to datetime object and then to Unix timestamp
                dt = parse(value)
                dt = dt.astimezone(tz.UTC)
                values.append(int(dt.timestamp()))

        # Call the addTravelRecord function from the smart contract with the values as arguments
        tx_hash = self.contract.functions.addTravelRecord(*values).transact({'from': '0x332F6a1F6691503855D59DB8A5fAc61789Bc99BD'})

        # Wait for the transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)

        # Clear the input fields
        for entry in self.add_travel_record_entries:
            entry[0].delete(0, tk.END)
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
            entry[0].delete(0, tk.END)

    def get_travel_record(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.get_travel_record_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                # Convert date string to datetime object and then to Unix timestamp
                dt = parse(value)
                dt = dt.astimezone(tz.UTC)
                values.append(int(dt.timestamp()))

        # Call the getTravelRecord function from the smart contract with the values as arguments
        result = self.contract.functions.getTravelRecord(*values).call()

        # Format the output and display it in the output_text box
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Passport ID: {result[0]}\n")
        self.output_text.insert(tk.END, f"Passport Expiration Date: {datetime.datetime.utcfromtimestamp(result[1]).strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.output_text.insert(tk.END, f"Full Name: {result[2]}\n")
        self.output_text.insert(tk.END, f"Country of Residence: {result[3]}\n")
        self.output_text.insert(tk.END, f"Country of Origin: {result[4]}\n")
        self.output_text.insert(tk.END, f"Destination Country: {result[5]}\n")
        if result[6] == 0:
            self.output_text.insert(tk.END, "This individual has not arrived in a new country since leaving their last location, and is likely still in transit.\n")
        else:
            self.output_text.insert(tk.END, f"Entry Date: {datetime.datetime.utcfromtimestamp(result[6]).strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.output_text.insert(tk.END, f"Planned Exit Date: {datetime.datetime.utcfromtimestamp(result[7]).strftime('%Y-%m-%d %H:%M:%S')}\n")

travel_log_gui = TravelLogGUI(root)
root.mainloop()