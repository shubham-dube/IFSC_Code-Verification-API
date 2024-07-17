# IFSC Code Verification API

This API fetches IFSC Code Details in JSON format

## Table of Contents

- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
- [Endpoints](#EndPoints)
- [Support](#Support)
- [Contribution](#Contribution)

## Features
- Sends only IFSC Code to get its details.
- Return IFSC Code details in a structured JSON format.
- Easy to integrate in any of your application.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shubham-dube/IFSC_Code-Verification-API.git
   cd IFSC_Code-Verification-API
   
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate # On Linux use `source venv/bin/activate`
   
3. Install the dependencies:
   ```bash
   pip install flask requests bs4 re html

4. Run the Application:
   ```bash
   python app.py
 *The API will be available at http://127.0.0.1:5000.*
 
## Usage
- Show the IFSC Code input Field to the user.
- Send the entered IFSC Code to the given endpoint request body.
- You will get all the details related to that IFSC Code in the JSON format.
  
## EndPoints

### Fetching IFSC Code Details

**Endpoint:** `/api/v1/getIFSCDetails`

**Method:** `POST`

**Description:** `This Endpoint takes the IFSC Code and return all the details regarding that IFSC Code.`

**Request Body:**
```json
{
    "IFSC": "UTIB0000046"
}
```
**Response**
```json
{
    "IFSC Code": "UTIB0000046",
    "MICR": "680211002",
    "address": {
        "district": "THRISSUR",
        "location": "CITY CENTRE, XXV/1130  ROUND WEST",
        "state": "KERALA"
    },
    "bank": "AXIS BANK",
    "branch": "THRISSUR",
    "branchCode": "000046"
}
```
**Status Codes**
- 200 OK : `Details Recieved`

## Support
For Support Contact me at itzshubhamofficial@gmail.com
or Mobile Number : `+917687877772`

## Contribution

We welcome contributions to improve this project. Here are some ways you can contribute:

1. **Report Bugs:** If you find any bugs, please report them by opening an issue on GitHub.
2. **Feature Requests:** If you have ideas for new features, feel free to suggest them by opening an issue.
3. **Code Contributions:** 
    - Fork the repository.
    - Create a new branch (`git checkout -b feature-branch`).
    - Make your changes.
    - Commit your changes (`git commit -m 'Add some feature'`).
    - Push to the branch (`git push origin feature-branch`).
    - Open a pull request.

4. **Documentation:** Improve the documentation to help others understand and use the project.
5. **Testing:** Write tests to improve code coverage and ensure stability.

Please make sure your contributions adhere to our coding guidelines and standards.
