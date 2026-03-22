import boto3
import os
from flask import Flask

app = Flask(__name__)
s3 = boto3.client('s3')

# Pulls your bucket name from the AWS App Runner environment variable
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

@app.route('/')
def dashboard():
    try:
        # Fetches your outage file from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        data = response['Body'].read().decode('utf-8')
        
        # Displays it on the screen for the supervisor
        return f"<h1>CityGreen Supervisor Dashboard</h1><pre>{data}</pre>"
    
    except Exception as e:
        return f"<h1>Connection Error</h1><p>Check S3 or Bucket Name: {str(e)}</p>", 500

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    # Required for App Runner to stay 'Running'
    app.run(host='0.0.0.0', port=8080)
