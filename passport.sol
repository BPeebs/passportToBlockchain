// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TravelLog {
    
    struct TravelRecord {
        uint enterDate;
        uint exitDate;
        string passportId;
        string personalInfo;
    }
    
    mapping(string => TravelRecord) private travelLogs;
    
    address private admin;
    
    constructor() {
        admin = msg.sender;
    }
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can access this function");
        _;
    }
    
    function addTravelRecord(string memory _passportId, string memory _personalInfo, uint _enterDate, uint _exitDate) public onlyAdmin {
        require(travelLogs[_passportId].enterDate == 0, "User is already in a country");
        require(_enterDate <= _exitDate, "Enter date should be less than or equal to exit date");
        
        TravelRecord memory newRecord = TravelRecord(_enterDate, _exitDate, _passportId, _personalInfo);
        travelLogs[_passportId] = newRecord;
    }
    
    function getTravelRecord(string memory _passportId) public view returns (uint enterDate, uint exitDate, string memory passportId, string memory personalInfo) {
        require(travelLogs[_passportId].enterDate != 0, "No travel record found for this passport ID");
        
        enterDate = travelLogs[_passportId].enterDate;
        exitDate = travelLogs[_passportId].exitDate;
        passportId = travelLogs[_passportId].passportId;
        personalInfo = travelLogs[_passportId].personalInfo;
    }
    
    function canEnter(string memory _passportId) public view returns (bool) {
        return travelLogs[_passportId].exitDate != 0;
    }
}