import boto3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
s3 = boto3.client('s3')

# Direct bucket for CityGreen
BUCKET_NAME = 'citygreen-outage-data-eina-961341532793-us-east-1-an'

@app.route('/check_outage', methods=['POST'])
def check_outage():
    """
    THE REPORTING SYSTEM: 
    The bot sends a ZIP code here. We check S3 and return the status.
    Every request is automatically logged to CloudWatch.
    """
    try:
        content = request.json
        user_zip = content.get('service_zip', '90210')

        # Get the latest outage map from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        outage_map = json.loads(response['Body'].read().decode('utf-8'))

        # Check the status
        is_outage = outage_map.get(user_zip, "false")

        # This print statement goes directly to CloudWatch for the supervisor
        print(f"REPORT: ZIP {user_zip} status requested. Result: {is_outage}")

        return jsonify({
            "outage_status": is_outage,
            "service_zip": user_zip
        })
    except Exception as e:
        print(f"ERROR: System failed to check S3: {str(e)}")
        return jsonify({"error": "System temporarily unavailable"}), 500

@app.route('/health')
def health():
    """Essential for App Runner to stay Active."""
    return "OK", 200

if __name__ == "__main__":
    # Must use 0.0.0.0 and Port 8080
    app.run(host='0.0.0.0', port=8080)
