import json
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the ZIP from the Contact Flow attributes
    # Connect sends this under Details -> ContactData -> Attributes
    attr = event.get('Details', {}).get('ContactData', {}).get('Attributes', {})
    user_zip = attr.get('service_zip', '00000') 
    
    # REACH INTO S3 (Requirement #4)
    # Replace 'citygreen-outage-data-2026' with your actual bucket name
    bucket_name = 'citygreen-outage-data-2026' 
    
    try:
        response = s3.get_object(Bucket=bucket_name, Key='outages.json')
        outage_map = json.loads(response['Body'].read().decode('utf-8'))
        # If zip is in the file and set to "true", there is an outage
        is_outage = outage_map.get(user_zip, "false")
    except Exception as e:
        print(f"Error reading S3: {e}")
        is_outage = "false"
    
    # Return attributes back to the Amazon Connect Flow
    return {
        "outage_status": is_outage,
        "retention_risk": "false" 
    }
