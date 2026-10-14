pragma solidity >= 0.8.11 <= 0.8.11;

contract WSNSecurity {
    string public registered_user;
    string public iot_data;
       
    //add user details who are registered to access IOT and user password will be encrypted with sha512	
    function addUser(string memory us) public {
       registered_user = us;	
    }
   //get user details
    function getUser() public view returns (string memory) {
        return registered_user;
    }

    function setIOTData(string memory id) public {
       iot_data = id;	
    }

    function getIOTData() public view returns (string memory) {
        return iot_data;
    }

    constructor() public {
        registered_user = "";
	iot_data="";
    }
}