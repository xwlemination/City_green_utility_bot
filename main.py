import flask
import json

app = flask.Flask(__name__)

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/outage-check', methods=['POST'])
def outage_check():
    data = flask.request.get_json()
    try:
        slots = data.get('sessionState', {}).get('intent', {}).get('slots', {})
        zip_slot = slots.get('ZipCode', {}) or {}
        zip_val = zip_slot.get('value', {}).get('interpretedValue')

        if zip_val == "90210":
            res_text = "Confirmed: There is an active power outage in 90210. Crews are on-site."
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
        return flask.Response(json.dumps(response_body), mimetype='application/json')
    except:
        err = {"messages": [{"contentType": "PlainText", "content": "Error."}]}
        return flask.Response(json.dumps(err), mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
