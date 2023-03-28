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
        require(_passportExpirationDate > block.timestamp + 180 days, "Passport expiration date must be at least 6 months from entry date");
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID, _entryDate));
        require(travelRecords[recordKey].entryDate == 0, "Travel record already exists");
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
    }

    function updateTravelRecord(string memory _passportID, uint _exitDate) public onlyAdmin {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID, block.timestamp));
        TravelRecord storage record = travelRecords[recordKey];
        require(record.entryDate != 0, "Travel record does not exist");
        require(_exitDate == 0 || _exitDate == block.timestamp, "Invalid exit date");
        record.actualExitDate = _exitDate;
    }

    function getTravelRecord(string memory _passportID, uint _entryDate) public view returns (string memory, uint, string memory, string memory, string memory, string memory, uint, uint, uint) {
        bytes32 recordKey = keccak256(abi.encodePacked(_passportID, _entryDate));
        TravelRecord storage record = travelRecords[recordKey];
        require(record.entryDate != 0, "Travel record does not exist");
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