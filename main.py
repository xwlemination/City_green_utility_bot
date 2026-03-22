import boto3
import os
from flask import Flask

app = Flask(__name__)
s3 = boto3.client('s3')

# Pulls your bucket name from the AWS environment variable you set
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

@app.route('/')
def dashboard():
    try:
        # Reaches into S3 to get the outage data
        response = s3.get_object(Bucket=BUCKET_NAME, Key='outages.json')
        data = response['Body'].read().decode('utf-8')
        
        # Shows the data to the supervisor
        return f"<h1>CityGreen Supervisor Dashboard</h1><pre>{data}</pre>"
    
    except Exception as e:
        return f"<h1>Dashboard Connection Error</h1><p>{str(e)}</p>", 500

@app.route('/health')
def health():
    return "OK", 200

# This is the part that was broken in your screenshot—it needs double underscores
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
