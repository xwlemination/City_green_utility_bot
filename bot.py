import json

def lambda_handler(event, context):
    # This grabs the "stop_reason" from your Lex Bot
    slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
    stop_reason = slots.get('stop_reason', {}).get('value', {}).get('interpretedValue', '')

    # This grabs the ZIP code for the outage check
    zip_code = slots.get('service_zip', {}).get('value', {}).get('interpretedValue', '')

    # Logic: If they mentioned "price", tag it for the Supervisor
    retention_risk = "true" if "price" in stop_reason.lower() else "false"

    # Logic: Mock outage ZIPs
    outage_zips = ["12345", "90210"]
    outage_found = "true" if zip_code in outage_zips else "false"

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
