pragma solidity ^0.8.0;

// Import BokkyPooBahsDateTimeLibrary from https://github.com/bokkypoobah/BokkyPooBahsDateTimeLibrary
import "https://github.com/bokkypoobah/BokkyPooBahsDateTimeLibrary/blob/master/contracts/BokkyPooBahsDateTimeLibrary.sol";

contract TravelRecords {
    struct PassportTravelDetails {
        bytes32 passportId;
        bytes32 fullName;
        bytes32 countryOfResidence;
        bytes32 countryOfOrigin;
        bytes32 destinationCountry;
        uint256 passportExpirationDate;
        uint256 entryDate;
        uint256 plannedExitDate;
    }

    struct Record {
        PassportTravelDetails passportDetails;
        uint256 actualExitDate;
    }

    mapping(bytes32 => mapping(uint256 => Record)) private records;
    address private admin;

    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier validDate(uint256 date) {
        require(date == 0 || BokkyPooBahsDateTimeLibrary.getYear(date) >= 2021, "Invalid date");
        _;
    }

    modifier futureDate(uint256 date) {
        require(date == 0 || date >= block.timestamp, "Date cannot be in the past");
        _;
    }

    modifier validPassport(PassportTravelDetails memory passport) {
        require(passport.passportExpirationDate == 0 || passport.passportExpirationDate > block.timestamp + 15778463 * 6, "Passport has expired or will expire within 6 months");
        _;
    }

    function addRecord(PassportTravelDetails memory passportDetails) public onlyAdmin validDate(passportDetails.entryDate) validDate(passportDetails.plannedExitDate) futureDate(passportDetails.entryDate) validPassport(passportDetails) {
        require(records[passportDetails.passportId][passportDetails.entryDate].passportDetails.entryDate == 0, "Record already exists");

        Record memory newRecord = Record(passportDetails, 0);
        records[passportDetails.passportId][passportDetails.entryDate] = newRecord;
    }

    function setActualExitDate(bytes32 passportId, uint256 entryDate, uint256 actualExitDate) public onlyAdmin validDate(actualExitDate) futureDate(actualExitDate) {
        require(records[passportId][entryDate].passportDetails.entryDate != 0, "Record does not exist");
        require(records[passportId][entryDate].actualExitDate == 0, "Actual exit date already set");
        require(BokkyPooBahsDateTimeLibrary.getDay(actualExitDate) == BokkyPooBahsDateTimeLibrary.getDay(block.timestamp), "Actual exit date must match current date");

        records[passportId][entryDate].actualExitDate = actualExitDate;
    }
    function getRecord(bytes32 passportId, uint256 entryDate) public view returns (bytes32, bytes32, bytes32, bytes32, bytes32, uint256, uint256, uint256, uint256) {
        Record memory record = records[passportId][entryDate];
        require(record.passportDetails.entryDate != 0, "Record does not exist");

        return (
            record.passportDetails.passportId,
            record.passportDetails.fullName,
            record.passportDetails.countryOfResidence,
            record.passportDetails.countryOfOrigin,
            record.passportDetails.destinationCountry,
            record.passportDetails.passportExpirationDate,
            record.passportDetails.entryDate,
            record.passportDetails.plannedExitDate,
            record.actualExitDate
        );
    }}