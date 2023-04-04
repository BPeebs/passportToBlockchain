pragma solidity ^0.8.0;

contract PassportRegistry {
    struct Passport {
        string firstName;
        string lastName;
        string passportNum;
        string countryOfResidence;
        string countryOfOrigin;
        string dob;
        string gender;
        string dateIssued;
        string dateExpire;
        string destinationCountry;
    }

    mapping(string => Passport) private passports;

    function passportDetailUpload(string memory _firstName, string memory _lastName, string memory _passportNum, string memory _countryOfResidence, string memory _countryOfOrigin, string memory _dob, string memory _gender, string memory _dateIssued, string memory _dateExpire) public {
        passports[_passportNum] = Passport({
            firstName: _firstName,
            lastName: _lastName,
            passportNum: _passportNum,
            countryOfResidence: _countryOfResidence,
            countryOfOrigin: _countryOfOrigin,
            dob: _dob,
            gender: _gender,
            dateIssued: _dateIssued,
            dateExpire: _dateExpire,
            destinationCountry: ""
        });
    }

    function getPassportDetails(string memory _passportNum) public view returns (string memory, string memory, string memory, string memory, string memory, string memory, string memory, string memory, string memory, string memory) {
        Passport memory passport = passports[_passportNum];
        return (passport.firstName, passport.lastName, passport.passportNum, passport.countryOfResidence, passport.countryOfOrigin, passport.dob, passport.gender, passport.dateIssued, passport.dateExpire, passport.destinationCountry);
    }

    function addDestination(string memory _passportNum, string memory _destinationCountry) public {
        Passport storage passport = passports[_passportNum];
        require(
            keccak256(abi.encodePacked(passport.countryOfOrigin)) != keccak256(abi.encodePacked(_destinationCountry)),
            "Destination country cannot be the same as the country of origin"
        );
        passport.destinationCountry = _destinationCountry;
    }
    
    function leaveCountry(string memory _passportNum) public {
        Passport storage passport = passports[_passportNum];
        passport.destinationCountry = "";
    }
}

