import boto3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
s3 = boto3.client('s3')

# Your specific S3 Bucket name
BUCKET_NAME = 'citygreen-outage-data-eina-961341532793-us-east-1-an'

@app.route('/')
def dashboard():
    """SUPERVISOR DASHBOARD: Shows all outages in S3 for viewing in browser."""
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        data = response['Body'].read().decode('utf-8')
        # This returns the raw JSON data to your browser screen
        return f"<h1>CityGreen Supervisor Dashboard</h1><pre>{data}</pre>"
    except Exception as e:
        return f"<h1>Dashboard Error</h1><p>Check S3 Bucket: {str(e)}</p>", 500

@app.route('/check_outage', methods=['POST'])
def check_outage():
    """REPORTING: Handles ZIP code checks for the Lex bot."""
    try:
        content = request.json
        user_zip = content.get('service_zip', '90210')

        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        outage_map = json.loads(response['Body'].read().decode('utf-8'))

        is_outage = outage_map.get(user_zip, "false")
        
        return jsonify({
            "outage_status": is_outage,
            "service_zip": user_zip
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Keeps the AWS App Runner service 'Active'."""
    return "OK", 200

if __name__ == "__main__":
    # Essential settings for App Runner
    app.run(host='0.0.0.0', port=8080)
