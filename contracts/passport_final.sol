pragma solidity ^0.8.0;
// create the data structure to hold the travel record info
contract TravelLog {
    struct TravelRecord {
        string passportID;
        uint passportExpirationDate;
        string fullName;
        string countryOfResidence;
        string countryOfOrigin;
        string destinationCountry;
        uint entryDate;
        uint plannedExitDate;
        uint actualExitDate;
    }
// specify the mapping
    mapping (bytes32 => TravelRecord) private travelRecords;
    mapping (string => bool) private passportExists;
    address private admin;
// specify that the admin is the message sender
    constructor() {
        admin = msg.sender;
    }
// require admin-only permission
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
// function to add initial information on record; include logic requirements
    function addPassportID(
        string memory _passportID,
        uint _passportExpirationDate,
        string memory _fullName,
        string memory _countryOfResidence
    ) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        require(!passportExists[_passportID], "Passport record already exists");  
        require(_passportExpirationDate > block.timestamp + 180 days, "Passport expiration date must be at least 6 months from entry date");
        travelRecords[recordKey] = TravelRecord(
            _passportID,
            _passportExpirationDate,
            _fullName,
            _countryOfResidence,
            _countryOfResidence,
            '',
            0,
            0,
            0
        );
        passportExists[_passportID] = true;
    }
// add function to return Home, specifically different from addEntry in that it checks residency and doesnt ask for projected exit date
    function returnHome(string memory _passportID, string memory _countryOfOrigin, string memory _countryOfResidence) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        TravelRecord storage record = travelRecords[recordKey];
        require(keccak256(abi.encodePacked(record.countryOfResidence)) ==  keccak256(abi.encodePacked(_countryOfResidence)), "User is not a resident of this country. Please use the 'add entry date' form.");
        require(passportExists[_passportID], "Passport record does not exist");
        require(record.entryDate == 0, "User cannot input a new entry date until entering an exit date.");
        record.entryDate = block.timestamp;
        record.plannedExitDate = 0;
        record.actualExitDate = 0;
        record.countryOfOrigin = _countryOfOrigin;
        record.destinationCountry = '';
    }

// add function to add an Entry date
    function addEntryDate(string memory _passportID, uint _plannedExitDate, string memory _countryOfOrigin) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        TravelRecord storage record = travelRecords[recordKey];
        require(passportExists[_passportID], "Passport record does not exist");
        require(record.entryDate == 0, "User cannot input a new entry date until entering an exit date.");
        record.entryDate = block.timestamp;
        record.plannedExitDate = _plannedExitDate;
        record.actualExitDate = 0;
        record.countryOfOrigin = _countryOfOrigin;
    }
// add function to add an exit date
    function addExitDate(string memory _passportID, string memory _destinationCountry) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        TravelRecord storage record = travelRecords[recordKey];
        require(passportExists[_passportID], "Travel record does not exist");
        require(record.actualExitDate == 0, "Exit date already set");
        record.entryDate = 0;
        record.actualExitDate = block.timestamp;
        record.countryOfOrigin = record.destinationCountry;
        record.destinationCountry = _destinationCountry;
    }
// add function to query a travel record
    function getTravelRecord(string memory _passportID) public view returns (string memory, uint, string memory, string memory, string memory, string memory, uint, uint, uint) {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        TravelRecord storage record = travelRecords[recordKey];
        require(passportExists[_passportID], "Travel record does not exist");
        return (
            record.passportID,
            record.passportExpirationDate,
            record.fullName,
            record.countryOfResidence,
            record.countryOfOrigin,
            record.destinationCountry,
            record.entryDate,
            record.plannedExitDate,
            record.actualExitDate
        );
    }
}