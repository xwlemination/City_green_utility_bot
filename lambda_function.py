import json

def lambda_handler(event, context):
    # Grabs data from your Lex slots
    slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
    
    stop_reason = slots.get('stop_reason', {}).get('value', {}).get('interpretedValue', '')
    zip_code = slots.get('service_zip', {}).get('value', {}).get('interpretedValue', '')

    # Requirement: Flag 'price' as a retention risk
    retention_risk = "true" if "price" in str(stop_reason).lower() else "false"
    
    # Requirement: Mock outage check
    outage_found = "true" if zip_code == "12345" else "false"

    return {
        "sessionState": {
            "sessionAttributes": {
                "retention_risk": retention_risk,
                "outage_found": outage_found
            },
            "dialogAction": {"type": "Close"},
            "intent": {"name": event['sessionState']['intent']['name'], "state": "Fulfilled"}
        }
    }
