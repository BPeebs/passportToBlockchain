pragma solidity ^0.8.0;

contract TravelRecord {
    
    struct TravelLog {
        uint enterDate;
        uint exitDate;
        string passportId;
        string personalInfo;
    }

    mapping(string => TravelLog[]) private travelLogs;
    address private admin;
    
    constructor() {
        admin = msg.sender;
    }
    
    function addTravelRecord(string memory _passportId, string memory _personalInfo) public {
        require(msg.sender == admin, "Only the admin can add travel records.");
        TravelLog[] storage logs = travelLogs[_passportId];
        uint length = logs.length;
        if (length > 0) {
            require(logs[length - 1].exitDate != 0, "The user is still in another country.");
        }
        logs.push(TravelLog(block.timestamp, 0, _passportId, _personalInfo));
    }
    
    function updateTravelRecordExit(string memory _passportId) public {
        require(msg.sender == admin, "Only the admin can update travel records.");
        TravelLog[] storage logs = travelLogs[_passportId];
        uint length = logs.length;
        require(length > 0 && logs[length - 1].exitDate == 0, "No travel record to update or user already exited.");
        logs[length - 1].exitDate = block.timestamp;
    }
    
    function getTravelRecord(string memory _passportId) public view returns (uint, uint, string memory, string memory) {
        TravelLog[] storage logs = travelLogs[_passportId];
        uint length = logs.length;
        require(length > 0, "No travel records found for the given passport ID.");
        TravelLog storage latestLog = logs[length - 1];
        return (latestLog.enterDate, latestLog.exitDate, latestLog.passportId, latestLog.personalInfo);
    }

    function getTravelRecordByDate(string memory _passportId, uint _enterDate) public view returns (uint, uint, string memory, string memory) {
        TravelLog[] storage logs = travelLogs[_passportId];
        uint length = logs.length;
        require(length > 0, "No travel records found for the given passport ID.");
        for (uint i = 0; i < length; i++) {
            if (logs[i].enterDate == _enterDate) {
                return (logs[i].enterDate, logs[i].exitDate, logs[i].passportId, logs[i].personalInfo);
            }
        }
        revert("No travel record found for the given entry date.");
    }
}