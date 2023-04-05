#This GUI works for the passport.sol smart contract

from pathlib import Path
import json
import tkinter as tk
from web3 import Web3
from dateutil.parser import parse
from dateutil import tz
import datetime
import tkcalendar
import os
from dotenv import load_dotenv

root = tk.Tk()
root.iconbitmap("C:\\Users\\ajcth\\Documents\\GitHub\\Passport_To_Blockchain\\resources\\images\\thumbnail.ico")

# Create the GUI
class TravelLogGUI:
    def __init__(self, master):
        self.master = master
        master.title("Travel Log")
        self.dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.abi_path = self.dir / '..' / 'resources' / 'abi' / 'passport_final_abi.json'
        with open(Path(self.abi_path)) as f:
            self.abi = json.load(f)
        self.dotenv_path = self.dir / '..' / 'resources' / 'env' / '.env'
        load_dotenv(dotenv_path=self.dotenv_path)
        self.contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
        self.network = os.getenv("WEB3_PROVIDER_URI")
        self.web3 = Web3(Web3.HTTPProvider(self.network))
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)
        
        self.add_passport_id_fields = [
            ("Passport ID", str),
            ("Passport Expiration (DD/MM/YYYY)", int),
            ("Full Name", str),
            ("Country of Residence", str),
        ]
        self.add_entry_date_fields = [
            ("Passport ID", str),
            ("Planned Exit Date", int),
            ("Country of Origin", str),
        ]
        self.add_exit_date_fields = [
            ("Passport ID", str),
            ("Destination Country", str),
        ]
        self.get_travel_record_fields = [
            ("Passport ID", str),
        ]
        self.return_home_fields = [
            ("Passport ID", str),
            ("Country of Origin", str),
            ("Country of Residence", str),
        ]

        self.create_widgets()

    def create_widgets(self):

        root.geometry("900x700")

        self.frame_image = tk.Frame(self.master, borderwidth=2, bg="white", relief='sunken')
        self.frame_image.pack(side='top', fill="x")

        self.frame_image.picture = tk.PhotoImage(name="background_photo", file="C:\\Users\\ajcth\\Documents\\GitHub\\Passport_To_Blockchain\\resources\\images\\background_photo.gif")
        self.frame_image.label = tk.Label(self.master, image=self.frame_image.picture)
        self.frame_image.label.place(x=0, y=0, relwidth=1, relheight=1)

        self.add_passport_id_frame = tk.LabelFrame(self.master, text="Add Passport ID Record", labelanchor='n')
        self.add_passport_id_frame.place(x=100, y=100)

        self.add_entry_date_frame = tk.LabelFrame(self.master, text="Add Entry Date", labelanchor='n')
        self.add_entry_date_frame.place(x=600, y=100)

        self.add_exit_date_frame = tk.LabelFrame(self.master, text="Add Exit Date", labelanchor='n')
        self.add_exit_date_frame.place(x=300, y=100)

        self.return_home_frame = tk.LabelFrame(self.master, text="Return Home", labelanchor='n')
        self.return_home_frame.place(x=450, y=100)

        self.get_travel_record_frame = tk.LabelFrame(self.master, text="Check Passport ID Record", labelanchor='n')
        self.get_travel_record_frame.place(x=750, y=100)

        self.output_text_frame = tk.LabelFrame(self.master, text="Travel Record Info", labelanchor='n', width=600, height=300)
        self.output_text_frame.pack(side=tk.BOTTOM)
        self.output_text_frame.pack_propagate(False)

        self.add_passport_id_entries = []
        for field, datatype in self.add_passport_id_fields:
            if datatype == str:
                frame = tk.Frame(self.add_passport_id_frame)
                frame.pack()
                label = tk.Label(frame, text=field)
                label.pack()
                entry = tk.Entry(frame)
                entry.pack()
                self.add_passport_id_entries.append((entry, datatype))
            else:
                frame = tk.Frame(self.add_passport_id_frame)
                frame.pack()
                label = tk.Label(frame, text=field)
                label.pack()
                entry = tkcalendar.DateEntry(frame)
                entry.pack()
                self.add_passport_id_entries.append((entry, datatype))


        # Create input fields for updateTravelRecord function
        self.add_entry_date_entries = []
        for field, datatype in self.add_entry_date_fields:
            if datatype == str:
                frame = tk.Frame(self.add_entry_date_frame)
                frame.pack()
                label = tk.Label(frame, text=field)
                label.pack()
                entry = tk.Entry(frame)
                entry.pack()
                self.add_entry_date_entries.append((entry, datatype))
            else:
                frame = tk.Frame(self.add_entry_date_frame)
                frame.pack()
                label = tk.Label(frame, text=field)
                label.pack()
                entry = tkcalendar.DateEntry(frame)
                entry.pack()
                self.add_entry_date_entries.append((entry, datatype))

        # Create input fields for updateTravelRecord function
        self.add_exit_date_entries = []
        for field, datatype in self.add_exit_date_fields:
            frame = tk.Frame(self.add_exit_date_frame)
            frame.pack()
            label = tk.Label(frame, text=field)
            label.pack()
            entry = tk.Entry(frame)
            entry.pack()
            self.add_exit_date_entries.append((entry, datatype))

        # Create input fields for updateTravelRecord function
        self.return_home_entries = []
        for field, datatype in self.return_home_fields:
            frame = tk.Frame(self.return_home_frame)
            frame.pack()
            label = tk.Label(frame, text=field)
            label.pack()
            entry = tk.Entry(frame)
            entry.pack()
            self.return_home_entries.append((entry, datatype))

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
        self.add_passport_id_button = tk.Button(self.add_passport_id_frame, text="Create Passport ID Record", command=self.add_passport_id_record)
        self.add_passport_id_button.pack()

        self.add_entry_date_button = tk.Button(self.add_entry_date_frame, text="Add Entry Date", command=self.add_entry_date)
        self.add_entry_date_button.pack()

        self.add_exit_date_button = tk.Button(self.add_exit_date_frame, text="Add Exit Date", command=self.add_exit_date)
        self.add_exit_date_button.pack()

        self.return_home_button = tk.Button(self.return_home_frame, text="Return Home", command=self.return_home)
        self.return_home_button.pack()

        self.get_travel_record_button = tk.Button(self.get_travel_record_frame, text="Get Travel Record", command=self.get_travel_record)
        self.get_travel_record_button.pack()

        # Create output area for getTravelRecord function
        self.output_text = tk.Text(self.output_text_frame)
        self.output_text.pack()


    def add_passport_id_record(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.add_passport_id_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                # Convert date string to datetime object and then to Unix timestamp
                dt = parse(value)
                dt = dt.astimezone(tz.UTC)
                values.append(int(dt.timestamp()))

        # Call the addTravelRecord function from the smart contract with the values as arguments
        self.deployer_address = os.getenv("DEPLOYER_ADDRESS")
        tx_hash = self.contract.functions.addPassportID(*values).transact({'from':  self.deployer_address})

        # Wait for the transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)

        # Clear the input fields
        for entry in self.add_passport_id_entries:
            entry[0].delete(0, tk.END)

    def add_entry_date(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.add_entry_date_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                # Convert date string to datetime object and then to Unix timestamp
                dt = parse(value)
                dt = dt.astimezone(tz.UTC)
                values.append(int(dt.timestamp()))
        # Call the updateTravelRecord function from the smart contract with the values as arguments
        self.deployer_address = os.getenv("DEPLOYER_ADDRESS")
        tx_hash = self.contract.functions.addEntryDate(*values).transact({'from': self.deployer_address})
        # Wait for the transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        # Clear the input fields
        for entry in self.add_entry_date_entries:
            entry[0].delete(0, tk.END)

    def add_exit_date(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.add_exit_date_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                # Convert date string to datetime object and then to Unix timestamp
                dt = parse(value)
                dt = dt.astimezone(tz.UTC)
                values.append(int(dt.timestamp()))
        # Call the updateTravelRecord function from the smart contract with the values as arguments
        self.deployer_address = os.getenv("DEPLOYER_ADDRESS")
        tx_hash = self.contract.functions.addExitDate(*values).transact({'from': self.deployer_address})
        # Wait for the transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        # Clear the input fields
        for entry in self.add_exit_date_entries:
                entry[0].delete(0, tk.END)

    def return_home(self):
        # Get the values from the input fields
        values = []
        for entry, datatype in self.return_home_entries:
            value = entry.get()
            if datatype == str:
                values.append(value)
            elif datatype == int:
                # Convert date string to datetime object and then to Unix timestamp
                dt = parse(value)
                dt = dt.astimezone(tz.UTC)
                values.append(int(dt.timestamp()))

        try:        
            # Call the updateTravelRecord function from the smart contract with the values as arguments
            self.deployer_address = os.getenv("DEPLOYER_ADDRESS")
            tx_hash = self.contract.functions.returnHome(*values).transact({'from': self.deployer_address})
            # Wait for the transaction to be mined
            self.web3.eth.waitForTransactionReceipt(tx_hash)
            # Clear the input fields
            for entry in self.return_home_entries:
                entry[0].delete(0, tk.END)
        except ValueError as e:
            # Catch the ValueError exception and display the error message
            error_message = f"Error: Country of Residence must match users records.\n {str(e)}"
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, error_message)
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
        try:
            # Call the getTravelRecord function from the smart contract with the values as arguments
            result = self.contract.functions.getTravelRecord(*values).call()

            # Format the output and display it in the output_text box
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Passport ID: {result[0]}\n")
            self.output_text.insert(tk.END, f"Passport Expiration: {datetime.datetime.utcfromtimestamp(result[1]).strftime('%Y-%m-%d')}\n")
            self.output_text.insert(tk.END, f"Full Name: {result[2]}\n")
            self.output_text.insert(tk.END, f"Country of Residence: {result[3]}\n")
            self.output_text.insert(tk.END, f"Country of Origin: {result[4]}\n")
            self.output_text.insert(tk.END, f"Destination Country: {result[5]}\n")
            if result[6] == 0:
                self.output_text.insert(tk.END, "Entry Date: This individual may still be in transit, or has created a passport ID record but has not since left their country of residence.\n")
            else:
                self.output_text.insert(tk.END, f"Entry Date: {datetime.datetime.utcfromtimestamp(result[6]).strftime('%Y-%m-%d')}\n")
            if result[7] == 0:
                self.output_text.insert(tk.END, "Planned Exit Date: This individual is in their home country.\n")
            else:
                self.output_text.insert(tk.END, f"Planned Exit Date: {datetime.datetime.utcfromtimestamp(result[7]).strftime('%Y-%m-%d')}\n")
            if result[8] == 0:
                self.output_text.insert(tk.END, "Actual Exit Date: This individual has not left the country.\n")
            else:
                self.output_text.insert(tk.END, f"Actual Exit Date: {datetime.datetime.utcfromtimestamp(result[8]).strftime('%Y-%m-%d')}\n")
        except ValueError as e:
            # Catch the ValueError exception and display the error message
            error_message = f"Error: travel record does not exist or network connection is down.\n {str(e)}"
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, error_message)

travel_log_gui = TravelLogGUI(root)
root.mainloop()