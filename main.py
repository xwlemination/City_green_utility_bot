
import boto3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
s3 = boto3.client('s3')

BUCKET_NAME = 'citygreen-outage-data-eina-961341532793-us-east-1-an'

@app.route('/check_outage', methods=['POST'])
def check_outage():
    try:
        content = request.json
        user_zip = content.get('service_zip', '90210')
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        outage_map = json.loads(response['Body'].read().decode('utf-8'))
        is_outage = outage_map.get(user_zip, "false")
        
        print(f"REPORT: ZIP {user_zip} status: {is_outage}")
        
        return jsonify({
            "outage_status": is_outage,
            "service_zip": user_zip
        })
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": "System error"}), 500

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    # Must use 0.0.0.0 and Port 8080
    app.run(host='0.0.0.0', port=8080)
