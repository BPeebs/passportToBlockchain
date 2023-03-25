pragma solidity ^0.8.0;

contract TravelRecords {
    struct TravelRecord {
        string passportID;
        string personalInfo;
        uint256 enterDate;
        uint256 plannedExitDate;
        uint256 actualExitDate;
    }

    mapping(string => TravelRecord[]) private travelLogs;
    mapping(string => bool) private passportIDs;

    address private admin;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this operation");
        _;
    }

    modifier validEnterDate(uint256 _enterDate) {
        require(_enterDate == block.timestamp, "Enter date must be current timestamp");
        _;
    }

    modifier canAddTravelRecord(string memory _passportID) {
        require(passportIDs[_passportID], "Passport ID does not exist");
        require(travelLogs[_passportID].length == 0 || travelLogs[_passportID][travelLogs[_passportID].length - 1].actualExitDate != 0, "Cannot add new travel record until previous travel record is exited");
        _;
    }

    function addTravelRecord(string calldata _passportID, string calldata _personalInfo, uint256 _enterDate, uint256 _plannedExitDate) external onlyAdmin validEnterDate(_enterDate) canAddTravelRecord(_passportID) {
        TravelRecord memory newRecord = TravelRecord(_passportID, _personalInfo, _enterDate, _plannedExitDate, 0);
        travelLogs[_passportID].push(newRecord);
    }

    function updateTravelRecordExit(string calldata _passportID, uint256 _actualExitDate) external onlyAdmin {
        require(travelLogs[_passportID].length > 0, "No travel record found for passport ID");
        require(travelLogs[_passportID][travelLogs[_passportID].length - 1].actualExitDate == 0, "No active travel record found for passport ID");
        require(_actualExitDate <= block.timestamp, "Actual exit date cannot be in the future");
        travelLogs[_passportID][travelLogs[_passportID].length - 1].actualExitDate = _actualExitDate;
    }

    function getTravelRecordsByPassportID(string calldata _passportID) external view returns (TravelRecord[] memory) {
        return travelLogs[_passportID];
    }

    function registerPassportID(string calldata _passportID) external onlyAdmin {
        passportIDs[_passportID] = true;
    }
}