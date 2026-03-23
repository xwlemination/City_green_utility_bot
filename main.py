import boto3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
s3 = boto3.client('s3')

# Your specific S3 Bucket name from your screenshot
BUCKET_NAME = 'citygreen-outage-data-eina-961341532793-us-east-1-am'

@app.route('/')
def dashboard():
    """SUPERVISOR DASHBOARD: Shows all outages in S3 for viewing in browser."""
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        data = response['Body'].read().decode('utf-8')
        return f"<h1>CityGreen Supervisor Dashboard</h1><pre>{data}</pre>"
    except Exception as e:
        return f"<h1>Dashboard Error</h1><p>Check S3 Bucket: {str(e)}</p>", 500

@app.route('/check_outage', methods=['POST'])
def check_outage():
    """REPORTING: Handles Lex V2 fulfillment by checking S3 data."""
    try:
        # 1. Get data from Lex Request
        content = request.json
        # Lex V2 stores slot values in: sessionState -> intent -> slots
        slots = content.get('sessionState', {}).get('intent', {}).get('slots', {})
        
        # Pull the ZIP code the user told the bot
        user_zip_data = slots.get('service_zip') or {}
        user_zip = user_zip_data.get('value', {}).get('interpretedValue', '98225')

        # 2. Pull the mapping from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        outage_map = json.loads(response['Body'].read().decode('utf-8'))

        # 3. Check status
        is_outage = outage_map.get(user_zip, "false")
        
        status_text = "there IS currently an active outage" if is_outage.lower() == "true" else "there are no reported outages"

        # 4. Return the LEX V2 formatted JSON
        return jsonify({
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": content['sessionState']['intent']['name'],
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"For the zip code {user_zip}, {status_text} at this time."
                }
            ]
        })

    except Exception as e:
        # Fallback message so the bot doesn't just go silent on error
        return jsonify({
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "CheckOutage", "state": "Failed"}
            },
            "messages": [{"contentType": "PlainText", "content": f"Error: {str(e)}"}]
        }), 200

@app.route('/health')
def health():
    """Crucial for App Runner: Needs to return 200 to stay 'Active'."""
    return "OK", 200

if __name__ == "__main__":
    # Ensure port matches your App Runner Service settings (default is often 8080)
    app.run(host='0.0.0.0', port=8080)
