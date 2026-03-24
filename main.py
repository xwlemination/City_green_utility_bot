from fastapi 
import FastAPI, Request

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.post("/outage-check")
async def outage_check(request: Request):
    data = await request.json()
    print(f"DEBUG: {data}")
    
    try:
        slots = data.get('sessionState', {}).get('intent', {}).get('slots', {})
        zip_slot = slots.get('ZipCode') or {}
        zip_val = zip_slot.get('value', {}).get('interpretedValue')

        if zip_val == "90210":
            res_text = "Confirmed. There is an active power outage in 90210. Crews are on-site."
        else:
            res_text = f"There are no reported outages for the ZIP code {zip_val} at this time."

        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": data['sessionState']['intent']['name'],
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [{"contentType": "PlainText", "content": res_text}]
        }
    except Exception as e:
        print(f"ERROR: {e}")
        return {"messages": [{"contentType": "PlainText", "content": "I encountered an error processing your request."}]}
