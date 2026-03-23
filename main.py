from flask import flask, request, json

app = flask(__name__)

# THIS IS THE PART AWS NEEDS TO SEE
@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/outage-check', methods=['POST'])
def outage_check():
    data = request.json
    
    # Extract the ZIP from the Lex V2 request structure
    slots = data.get('sessionState', {}).get('intent', {}).get('slots', {})
    zip_code = slots.get('ZipCode', {}).get('value', {}).get('interpretedValue')

    # THE HARD-CODED ZIP CHECK
    if zip_code == "90210":
        response_text = "Confirmed: There is an active power outage in 90210. Our crews are currently on-site and estimated restoration is within 2 hours."
    else:
        response_text = f"There are no reported outages for the ZIP code {zip_code} at this time."

    return json({
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": data['sessionState']['intent']['name'],
                "slots": slots,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": response_text
            }
        ]
    })

if __name__ == "__main__":
    # HOST MUST BE 0.0.0.0 AND PORT MUST BE 5000
    app.run(host='0.0.0.0', port=5000)
