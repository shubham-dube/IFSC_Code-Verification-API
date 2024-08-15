from flask import Flask, jsonify, Response, make_response, request
import requests
from bs4 import BeautifulSoup
import re
import html
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)

@app.route("/api/v1/getIFSCDetails", methods=["POST"])
def getIFSCDetails():
    try:
        IFSC = request.json.get("IFSC")
        session = requests.Session()

        response = session.get(
            f"https://ifsc.bankifsccode.com/{IFSC}"
        )

        cleaned_html_string = response.text.replace('\n', '').replace('\r', '').replace('\t', '').replace('\\', '').replace('\"', '')
        cleaned_html_string = html.unescape(cleaned_html_string)

        soup = BeautifulSoup(cleaned_html_string, 'html.parser')
        mainDiv = soup.find_all('div', class_="text")
        if(len(mainDiv)==0):
            return jsonify({"status": "IFSC Code Not Found"})
        anchors = mainDiv[2].find_all('a')

        pattern = r'Address: (.*?)State:'
        match = re.search(pattern, mainDiv[2].get_text())
        address = match.group(1).strip()

        bank = anchors[0].get_text()
        state = anchors[1].get_text()
        district = anchors[2].get_text()
        branch = anchors[4].get_text()
        MICR = anchors[6].get_text()
        # print(mainDiv[2].get_text())

        jsonResponse = {
            "IFSC Code": IFSC,
            "bank": bank,
            "branch": branch,
            "MICR": MICR,
            "address": {
                "location": address,
                "district": district,
                "state": state
            },
            "branchCode": IFSC[-6:]
        }

        return jsonify(jsonResponse)

    except Exception as e:
        print(e)
        return jsonify({"error": "Error in fetching IFSC Code Details"})


# @app.route("/api/v1/professional/check-email-validity", methods=["POST"])
# def check_email_validity():
#     try:
#         url = "https://www.site24x7.com/tools/email-validator.html"
#         post_url = "https://www.site24x7.com/tools/email-validator"
        
#         email = request.json.get("email")
#         session = requests.Session()
    
#         postBody = {
#             "emails": email
#         }

#         response = session.post(post_url, data=postBody)

#         emailObject = response.json()

#         failedDomain = None

#         try:
#             failedDomain = emailObject['failed_domains']
#             failedDomain = True
#         except:
#             failedDomain = False
        
#         domain = list(emailObject['domainMap'].keys())[0]
        
#         if(not failedDomain):
#             statusCode = emailObject['results'][domain][email]['status']

#             status = ''
#             if(statusCode==250):
#                 status = "Valid"
#             else:
#                 status = "Invalid"
            
#             reason = emailObject['results'][domain][email]['reason']
            
#             jsonResponse = {
#                 "email": email,
#                 "domain": domain,
#                 "statusCode": statusCode,
#                 "status": status,
#                 "description": reason
#             }
#             print(jsonResponse)

#             return jsonify(jsonResponse)
#         else:
#             jsonResponse = {
#                 "email": email,
#                 "domain": domain,
#                 "statusCode": 404,
#                 "status": "Invalid",
#                 "description": "Domain Not Found"
#             }
#             print(jsonResponse)

#             return jsonify(jsonResponse)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in Checking email validity"})
    
# @app.route("/api/v1/company/get_fssai_details", methods=["POST"])
# def get_fssai_details():
#     try:
#         url = "https://foscos.fssai.gov.in/gateway/commonauth/commonapi/getsearchapplicationdetails/1"

#         licenceNumber = request.json.get("licenceNumber")
#         session = requests.Session()

#         session.verify = False

#         postBody = {
#             "flrsLicenseNo": licenceNumber
#         }

#         response = session.post(url, json=postBody)

#         return jsonify(response.json())
    
#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching fssai licence Details"})
    
# @app.route("/api/v1/professional/IFSC/getBanks", methods=["GET"])
# def getBanks():
#     try:
#         url = "https://www.policybazaar.com/ifsc/"
#         session = requests.Session()

#         session.headers = {
#             "authority": "www.policybazaar.com",
#             "method": "GET",
#             "path": "/ifsc/",
#             "scheme": "https",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Encoding": "gzip, deflate, br, zstd",
#             "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
#             "Cache-Control": "max-age=0",
#             "Priority": "u=0, i",
#             "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": '"Windows"',
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "cross-site",
#             "Sec-Fetch-User": "?1",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#         }

#         response = session.get(url)

#         htmlString = response.text
#         cleaned_html_string = htmlString.replace('\n', '').replace('\r', '').replace('\t', '').replace('\\', '')
#         cleaned_html_string = html.unescape(cleaned_html_string)

#         soup = BeautifulSoup(cleaned_html_string, 'html.parser')

#         bankOptions = soup.find('select', id="bank")
#         options = bankOptions.find_all('option')

#         bankValues = []
#         for i in range(1,len(options)):
#             bank = options[i].get('value')
#             bankValues.append(bank)

#         jsonResponse = {
#             "banks": bankValues,
#             "status": "Success"
#         }

#         return jsonify(jsonResponse)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching Bank Names"})
    
# @app.route("/api/v1/professional/IFSC/getStates", methods=["POST"])
# def getStates():
#     try:
#         post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
#         bank = request.json.get("bank")
#         session = requests.Session()

#         session.headers = {
#             "authority": "www.policybazaar.com",
#             "method": "GET",
#             "path": "/ifsc/",
#             "scheme": "https",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Encoding": "gzip, deflate, br, zstd",
#             "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
#             "Cache-Control": "max-age=0",
#             "Priority": "u=0, i",
#             "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": '"Windows"',
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "cross-site",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Sec-Fetch-User": "?1",
#             "Referer": "https://www.policybazaar.com/ifsc/",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#         }
         
#         postData = {
#             "task": "getstate",
#             "bankname": bank
#         }

#         response = session.post(post_url, data=postData)

#         return jsonify(response.json())

#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching State Names which has this Bank"})
    
# @app.route("/api/v1/professional/IFSC/getDistricts", methods=["POST"])
# def getDistricts():
#     try:
#         post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
#         bank = request.json.get("bank")
#         state = request.json.get("state")
#         session = requests.Session()

#         session.headers = {
#             "authority": "www.policybazaar.com",
#             "method": "GET",
#             "path": "/ifsc/",
#             "scheme": "https",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Encoding": "gzip, deflate, br, zstd",
#             "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
#             "Cache-Control": "max-age=0",
#             "Priority": "u=0, i",
#             "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": '"Windows"',
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "cross-site",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Sec-Fetch-User": "?1",
#             "Referer": "https://www.policybazaar.com/ifsc/",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#         }
         
#         postData = {
#             "task": "getdistrict",
#             "bankname": bank,
#             "statename": state
#         }

#         response = session.post(post_url, data=postData)

#         return jsonify(response.json())

#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching districts of state chosen"})
    
# @app.route("/api/v1/professional/IFSC/getBranches", methods=["POST"])
# def getBranches():
#     try:
#         post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
#         bank = request.json.get("bank")
#         state = request.json.get("state")
#         district = request.json.get("district")
#         session = requests.Session()

#         session.headers = {
#             "authority": "www.policybazaar.com",
#             "method": "GET",
#             "path": "/ifsc/",
#             "scheme": "https",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Encoding": "gzip, deflate, br, zstd",
#             "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
#             "Cache-Control": "max-age=0",
#             "Priority": "u=0, i",
#             "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": '"Windows"',
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "cross-site",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Sec-Fetch-User": "?1",
#             "Referer": "https://www.policybazaar.com/ifsc/",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#         }
         
#         postData = {
#             "task": "getbranch",
#             "bankname": bank,
#             "statename": state,
#             "districtname": district
#         }

#         response = session.post(post_url, data=postData)

#         return jsonify(response.json())

#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching branches in the branches"})

# @app.route("/api/v1/professional/IFSC/get_ifsc_code", methods=["POST"])
# def get_ifsc_code():
#     try:
#         post_url = "https://www.policybazaar.com/templates/policybazaar/getifscval.php"
#         bank = request.json.get("bank")
#         state = request.json.get("state")
#         district = request.json.get("district")
#         branch = request.json.get('branch')
#         session = requests.Session()

#         session.headers = {
#             "authority": "www.policybazaar.com",
#             "method": "GET",
#             "path": "/ifsc/",
#             "scheme": "https",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "Accept-Encoding": "gzip, deflate, br, zstd",
#             "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
#             "Cache-Control": "max-age=0",
#             "Priority": "u=0, i",
#             "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": '"Windows"',
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "Sec-Fetch-Site": "cross-site",
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "Sec-Fetch-User": "?1",
#             "Referer": "https://www.policybazaar.com/ifsc/",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#         }
         
#         postData = {
#             "task": "getdetail",
#             "bankname": bank,
#             "statename": state,
#             "districtname": district,
#             "branchname": branch
#         }

#         response = session.post(post_url, data=postData)

#         return jsonify(response.json())

#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching IFSC Code. Please Retry Again"})
    
# @app.route("/api/v1/professional/IFSC/getIFSCDetails", methods=["POST"])
# def getIFSCDetails():
#     try:
#         IFSC = request.json.get("IFSC")
#         session = requests.Session()

#         response = session.get(
#             f"https://ifsc.bankifsccode.com/{IFSC}"
#         )

#         cleaned_html_string = response.text.replace('\n', '').replace('\r', '').replace('\t', '').replace('\\', '').replace('\"', '')
#         cleaned_html_string = html.unescape(cleaned_html_string)

#         soup = BeautifulSoup(cleaned_html_string, 'html.parser')
#         mainDiv = soup.find_all('div', class_="text")
#         if(len(mainDiv)==0):
#             return jsonify({"status": "IFSC Code Not Found"})
#         anchors = mainDiv[2].find_all('a')

#         pattern = r'Address: (.*?)State:'
#         match = re.search(pattern, mainDiv[2].get_text())
#         address = match.group(1).strip()

#         bank = anchors[0].get_text()
#         state = anchors[1].get_text()
#         district = anchors[2].get_text()
#         branch = anchors[4].get_text()
#         MICR = anchors[6].get_text()
#         # print(mainDiv[2].get_text())

#         jsonResponse = {
#             "IFSC Code": IFSC,
#             "bank": bank,
#             "branch": branch,
#             "MICR": MICR,
#             "address": {
#                 "location": address,
#                 "district": district,
#                 "state": state
#             },
#             "branchCode": IFSC[-6:]
#         }

#         return jsonify(jsonResponse)

#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching IFSC Code Details"})
    
# @app.route("/api/v1/company/startup/getCertificate", methods=["POST"])
# def getCertificate():
#     try:
#         url = "https://api.startupindia.gov.in/sih/api/noauth/dpiit/services/validate/certificate"
        
#         dipp = request.json.get("dippNumber")  #DIPP141531
#         certType = request.json.get("certificateType")
#         session = requests.Session()

#         session.headers = {
#             'authority': 'api.startupindia.gov.in',
#             'method': 'POST',
#             'path': '/sih/api/noauth/dpiit/services/validate/certificate',
#             'scheme': 'https',
#             'Accept': 'application/json, text/javascript, */*; q=0.01',
#             'Accept-Encoding': 'gzip, deflate, br, zstd',
#             'Accept-Language': 'en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7',
#             'Content-Length': '75',
#             'Content-Type': 'application/json',
#             'Origin': 'https://www.startupindia.gov.in',
#             'Priority': 'u=1, i',
#             'Referer': 'https://www.startupindia.gov.in/',
#             'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
#             'Sec-Ch-Ua-Mobile': '?0',
#             'Sec-Ch-Ua-Platform': '"Windows"',
#             'Sec-Fetch-Dest': 'empty',
#             'Sec-Fetch-Mode': 'cors',
#             'Sec-Fetch-Site': 'same-site',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
#         }

#         postBody = {
#             "certificateType": certType,
#             "dippNumber": dipp,
#             "entityName": ""
#         }

#         response = session.post(url, json=postBody)

#         pdfLink = "https://recognition-be.startupindia.gov.in" + response.json()['data']

#         jsonResponse = {
#             "status": "Successfull",
#             "pdfLink": pdfLink
#         }

#         return jsonify(jsonResponse)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error in fetching Certificate of Recognization"})

@app.route("/api/v1/NID/check-PAN-aadhaar-linkage", methods=["POST"])
def check_PAN_aadhaar_linkage():
    try:
        post_url = "https://eportal.incometax.gov.in/iec/servicesapi/getEntity"
        
        PAN = request.json.get("PAN")
        aadhaar = request.json.get("aadhaar")
        session = requests.Session()
    
        postBody = {
            "aadhaarNumber": aadhaar,
            "pan": PAN,
            "preLoginFlag": "Y",
            "serviceName": "linkAadhaarPreLoginService"
        }

        response = session.post(post_url, json=postBody)

        objectBody = response.json()

        # linkedAadhaarNumber = objectBody['aadhaarNumber']
        # errors = objectBody['errors']
        # isMigrated = objectBody['isMigrated']
        description = objectBody['messages'][0]['desc']
        print(description)

        withGivenAadhar = None
        withGivenPAN = None
        isPanExist = None
        isAadhaarValid = None
        isPanInactive = None

        if("valid 12 digit Aadhaar" in description):
            isAadhaarValid = False
            jsonResponse = {
                "isPanExist": "Unknown",
                "isAadhaarValid": isAadhaarValid,
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": "Unknown",
                "description": description
            }
            return jsonify(jsonResponse)
        
        if("PAN entered is inactive"in description):
            isAadhaarValid = True
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": isAadhaarValid,
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": False,
                "description": description
            }
            return jsonify(jsonResponse)
        
        if("enter valid Pan Card" in description):
            jsonResponse = {
                "isPanExist": False,
                "isAadhaarValid": "Unknown",
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": "Unknown",
                "description": description
            }
            return jsonify(jsonResponse)
        if(("Your PAN" in description) and ("is already linked to given Aadhaar" in description)):
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": True,
                "linkedAadharNumber": objectBody['aadhaarNumber'],
                "linkedPanNumber": objectBody['pan'],
                "isPanLinkedToAdhaar": True,
                "description": description
            }
            return jsonify(jsonResponse)
        
        if(("Your PAN" in description) and ("is linked to some other Aadhaar" in description)):
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": True,
                "linkedAadharNumber": objectBody['aadhaarNumber'],
                "linkedPanNumber": objectBody['pan'],
                "isPanLinkedToAdhaar": True,
                "description": description
            }
            return jsonify(jsonResponse)
        
        if(("Your Aadhaar Number" in description) and ("is linked to some other PAN" in description)):
            jsonResponse = {
                "isPanExist": True,
                "isAadhaarValid": True,
                "linkedAadharNumber": objectBody['aadhaarNumber'],
                "linkedPanNumber": objectBody['pan'],
                "isPanLinkedToAdhaar": True,
                "description": description
            }
            return jsonify(jsonResponse)
        else:
            jsonResponse = {
                "isPanExist": "Unknown",
                "isAadhaarValid": "Unknown",
                "linkedAadharNumber": "Unknown",
                "linkedPanNumber": "Unknown",
                "isPanLinkedToAdhaar": False,
                "description": description
            }
            return jsonify(jsonResponse)
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in Checking the linkage status of PAN and Aadhaar."})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=5001)