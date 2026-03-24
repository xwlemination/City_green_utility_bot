import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Active"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/lex")
async def handle_lex(request: Request):
    lex_event = await request.json()
    
    try:
        intent = lex_event['sessionState']['intent']['name']
        zip_code = lex_event['sessionState']['intent']['slots']['service_zip']['value']['interpretedValue']

        if intent == "ReportOutage" and zip_code == "90210":
            is_outage_active = "true"
        else:
            is_outage_active = "false"

        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent, "state": "Fulfilled"}
            },
            "sessionAttributes": {
                "service_zip": zip_code,
                "is_outage": is_outage_active
            }
        }

    except (KeyError, TypeError):
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "FallbackIntent", "state": "Failed"}
            },
            "sessionAttributes": {
                "is_outage": "false",
                "error_flag": "true"
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
