import boto3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
s3 = boto3.client('s3')

BUCKET_NAME = 'citygreen-outage-data-eina-961341532793-us-east-1-am'

@app.route('/')
def dashboard():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        data = response['Body'].read().decode('utf-8')
        return f"<h1>CityGreen Supervisor Dashboard</h1><pre>{data}</pre>"
    except Exception as e:
        return f"<h1>Dashboard Error</h1><p>{str(e)}</p>", 500

@app.route('/check_outage', methods=['POST'])
def check_outage():
    try:
        content = request.json
        # Pull the ZIP from the Lex V2 slot structure
        slots = content.get('sessionState', {}).get('intent', {}).get('slots', {})
        user_zip_data = slots.get('service_zip') or {}
        user_zip = user_zip_data.get('value', {}).get('interpretedValue', '90210')

        # Pull from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        outage_map = json.loads(response['Body'].read().decode('utf-8'))

        # Check the map
        is_outage = outage_map.get(user_zip, "false")
        status_text = "there IS an active outage" if is_outage.lower() == "true" else "there are no outages"

        # Match the Intent Name from your screenshot: ReportOutage
        return jsonify({
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": "ReportOutage", 
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"For zip code {user_zip}, {status_text}."
                }
            ]
        })
    except Exception as e:
        return jsonify({
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "ReportOutage", "state": "Failed"}
            },
            "messages": [{"contentType": "PlainText", "content": "Sorry, I can't check outages right now."}]
        }), 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
