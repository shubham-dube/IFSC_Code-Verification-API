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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host='0.0.0.0', port=5001)