import flask
import json

app = flask.Flask(__name__)

# This tells AWS your app is alive
@app.route('/health')
def health_check():
    return "OK", 200

# Your actual bot logic
@app.route('/outage-check', methods=['POST'])
def outage_check():
    data = flask.request.get_json()
    try:
        # Pulling the zip code from the Lex request
        slots = data.get('sessionState', {}).get('intent', {}).get('slots', {})
        zip_slot = slots.get('ZipCode', {}) or {}
        zip_val = zip_slot.get('value', {}).get('interpretedValue')

        if zip_val == "90210":
            res_text = "Confirmed: There is an active power outage in 90210. Our crews are on-site."
        else:
            res_text = f"There are no reported outages for the ZIP code {zip_val} at this time."

        response_body = {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": data['sessionState']['intent']['name'],
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [{"contentType": "PlainText", "content": res_text}]
        }
        
        # Using json.dumps instead of jsonify
        return flask.Response(json.dumps(response_body), mimetype='application/json')

    except Exception as e:
        error_body = {"messages": [{"contentType": "PlainText", "content": "Error."}]}
        return flask.Response(json.dumps(error_body), mimetype='application/json')

if __name__ == "__main__":
    # AWS needs host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
