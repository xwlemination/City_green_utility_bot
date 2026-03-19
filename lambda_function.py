import json

def lambda_handler(event, context):
    # 1. Get data from the Lex bot/Connect flow
    # Connect sends parameters inside ['Details']['ContactData']['Attributes']
    attributes = event.get('Details', {}).get('ContactData', {}).get('Attributes', {})
    
    zip_code = attributes.get('service_zip', '00000')
    reason = attributes.get('stop_reason', '').lower()
    
    # 2. Logic for Scenario 4
    # Mock outage data: if zip starts with '9', there is an outage
    outage_status = "true" if zip_code.startswith('9') else "false"
    
    # Retention risk: if they mention 'price' or 'expensive'
    retention_risk = "true" if "price" in reason or "expensive" in reason else "false"
    
    # 3. Return the JSON "Attributes" back to the flow
    return {
        "outage_status": outage_status,
        "retention_risk": retention_risk,
        "processed_zip": zip_code
    }
