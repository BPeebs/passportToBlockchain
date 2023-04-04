pragma solidity ^0.8.0;

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

    mapping (bytes32 => TravelRecord) private travelRecords;
    mapping (string => bool) private passportExists;
    address private admin;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    function addTravelRecord(
        string memory _passportID,
        uint _passportExpirationDate,
        string memory _fullName,
        string memory _countryOfResidence,
        string memory _countryOfOrigin,
        string memory _destinationCountry,
        uint _entryDate,
        uint _plannedExitDate
    ) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        require(!passportExists[_passportID], "Travel record already exists");
        require(_passportExpirationDate > block.timestamp + 180 days, "Passport expiration date must be at least 6 months from entry date");
        travelRecords[recordKey] = TravelRecord(
            _passportID,
            _passportExpirationDate,
            _fullName,
            _countryOfResidence,
            _countryOfOrigin,
            _destinationCountry,
            _entryDate,
            _plannedExitDate,
            0
        );
        passportExists[_passportID] = true;
    }

    function addEntryDate(string memory _passportID, uint _plannedExitDate) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        TravelRecord storage record = travelRecords[recordKey];
        require(passportExists[_passportID], "Travel record does not exist");
        require(record.entryDate == 0, "User cannot input a new entry date until entering an exit date.");
        record.entryDate = block.timestamp;
        record.plannedExitDate = _plannedExitDate;
        record.actualExitDate = 0;
    }

    function addExitDate(string memory _passportID) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID));
        TravelRecord storage record = travelRecords[recordKey];
        require(passportExists[_passportID], "Travel record does not exist");
        require(record.actualExitDate == 0, "Exit date already set");
        record.entryDate = 0;
        record.actualExitDate = block.timestamp;
    }

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