import boto3
import os
from flask import Flask

# 1. Initialize the Web Server
app = Flask(__name__)
s3 = boto3.client('s3')

# 2. Get the bucket name from your App Runner Environment Variables
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

@app.route('/')
def dashboard():
    """
    This is the main page supervisors will see. 
    It reaches into S3 and displays the outage data.
    """
    try:
        # Fetches your outage file from S3
        # Ensure 'outages.json' matches the filename in your S3 bucket
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        data = response['Body'].read().decode('utf-8')
        
        # Displays the raw data on the screen for the supervisor
        return f"<h1>CityGreen Supervisor Dashboard</h1><pre>{data}</pre>"
    
    except Exception as e:
        # If S3 fails, this tells you exactly why (e.g., Access Denied)
        return f"<h1>Connection Error</h1><p>Check S3 or Bucket Name: {str(e)}</p>", 500

@app.route('/health')
def health():
    """Standard health check so App Runner knows the app is alive."""
    return "OK", 200

# 3. The 'Listener' - FIXED SYNTAX
if __name__ == "__main__":
    # This MUST stay 0.0.0.0 and port 8080 to match your AWS settings
    app.run(host='0.0.0.0', port=8080)
