pragma solidity ^0.8.0;

contract TravelRecords {
    // Define a struct to hold the travel record data
    struct Record {
        string passportID;
        uint256 passportExpirationDate;
        string fullName;
        string countryOfResidence;
        string countryOfOrigin;
        string destinationCountry;
        uint256 entryDate;
        uint256 plannedExitDate;
        uint256 actualExitDate;
    }

    // Define an array to hold all travel records
    Record[] private records;

    // Define an admin address
    address private admin;

    // Define an event to log when a new travel record is added
    event NewTravelRecordAdded(uint256 indexed index);

    // Define a modifier to restrict access to the admin
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only the admin can perform this action.");
        _;
    }

    // Define a constructor to set the admin address
    constructor() {
        admin = msg.sender;
    }

    // Define a function to add a new travel record
    function addTravelRecord(
        string memory _passportID,
        uint256 _passportExpirationDate,
        string memory _fullName,
        string memory _countryOfResidence,
        string memory _countryOfOrigin,
        string memory _destinationCountry,
        uint256 _entryDate,
        uint256 _plannedExitDate
    ) public onlyAdmin {
        // Ensure that the passport expiration date is at least 6 months in the future
        require(_passportExpirationDate > block.timestamp + 26 weeks, "Passport has expired or will expire soon.");

        // Ensure that the entry date and planned exit date are valid
        require(_entryDate <= block.timestamp, "Entry date cannot be in the future.");
        require(_entryDate <= _plannedExitDate, "Planned exit date must be after entry date.");

        // Add the new travel record to the array
        records.push(Record({
            passportID: _passportID,
            passportExpirationDate: _passportExpirationDate,
            fullName: _fullName,
            countryOfResidence: _countryOfResidence,
            countryOfOrigin: _countryOfOrigin,
            destinationCountry: _destinationCountry,
            entryDate: _entryDate,
            plannedExitDate: _plannedExitDate,
            actualExitDate: 0
        }));

        // Log the new travel record index
        emit NewTravelRecordAdded(records.length - 1);
    }

    // Define a function to update the actual exit date of a travel record
    function updateActualExitDate(uint256 _index, uint256 _actualExitDate) public onlyAdmin {
        // Ensure that the actual exit date is valid
        require(_actualExitDate <= block.timestamp, "Actual exit date cannot be in the future.");

        // Ensure that the travel record exists and has not already been updated
        require(_index < records.length, "Invalid travel record index.");
        require(records[_index].actualExitDate == 0, "Actual exit date has already been set.");

        // Update the actual exit date of the travel record
        records[_index].actualExitDate = _actualExitDate;
    }

    // Define a function to get the number of travel records
    function getRecordCount() public view returns (uint256) {
        return records.length;
    }

    // Define a function to get a travel record by index
    function getRecordByIndex(uint256 _index) public view returns (Record memory) {
        require(_index < records.length, "Invalid travel record index.");
        return records[_index];
    }

    // Define a function to get a travel record by passport ID and entry date
    function getRecordByPassportIDAndEntryDate(string memory _passportID, uint256 _entryDate) public view returns (Record memory) {
        for (uint256 i = 0; i < records.length; i++) {
            if (
                keccak256(bytes(records[i].passportID)) == keccak256(bytes(_passportID)) &&
                records[i].entryDate == _entryDate
            ) {
                return records[i];
            }
        }
        revert("Travel record not found.");
}}