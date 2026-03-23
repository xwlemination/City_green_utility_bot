import os
import boto3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
s3 = boto3.client('s3')

# Replace with your actual bucket name
BUCKET_NAME = 'citygreen-outage-data-eina' 

# 1. ADDED: Health check route for App Runner
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

@app.route('/', methods=['POST'])
def handle_lex():
    data = request.get_json()
    
    # 2. Grab the ZIP from the Lex V2 slot
    try:
        slots = data['sessionState']['intent']['slots']
        user_zip = slots['zip_code']['value']['interpretedValue']
    except (KeyError, TypeError):
        user_zip = "Unknown"

    # 3. Fetch the outage data from S3
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        outages = json.loads(response['Body'].read().decode('utf-8'))
        
        # Check if the zip has an outage
        has_outage = outages.get(user_zip, False)
        status_text = "there IS an active outage" if has_outage else "there are no active outages"
    except Exception as e:
        print(f"Error: {e}")
        status_text = "we are having trouble checking our system right now"

    # 4. Return the LEX V2 formatted response
    return jsonify({
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
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

if __name__ == '__main__':
    # Listen on port 8080 as required by App Runner
    app.run(host='0.0.0.0', port=8080)
