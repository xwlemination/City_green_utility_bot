import boto3
import os
from flask import Flask, jsonify

# 1. Initialize the Web Server
app = Flask(__name__)
s3 = boto3.client('s3')

# 2. Get the bucket name from your App Runner Environment Variables
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

@app.route('/')
def dashboard():
    """
    This is the main page supervisors will see. 
    It replaces the 'lambda_handler' and keeps the app running.
    """
    try:
        # This keeps your original logic of checking S3 for outage data
        # Adjust 'outages.json' if your filename is different in S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        data = response['Body'].read().decode('utf-8')
        
        # This sends the data to the browser for the supervisor to see
        return f"<h1>CityGreen Supervisor Dashboard</h1><pre>{data}</pre>"
    
    except Exception as e:
        return f"<h1>Dashboard Error</h1><p>Check S3 connection: {str(e)}</p>", 500

@app.route('/health')
def health_check():
    """Tells AWS the app is alive so it doesn't shut down."""
    return "OK", 200

# 3. The 'Listener' that makes App Runner work
if __name__ == "__main__":
    # This MUST be 0.0.0.0 and port 8080 to match your AWS settings
    app.run(host='0.0.0.0', port=8080)
