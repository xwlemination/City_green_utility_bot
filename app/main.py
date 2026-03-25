import os
import sys
import boto3
import uvicorn
from fastapi import FastAPI, Request, UploadFile, File

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()
s3 = boto3.client('s3')

BUCKET_NAME = "citygreen-outage-data-eina-961341532793-us-east-1-an"

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_recording(file: UploadFile = File(...)):
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return {"message": "Upload successful"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/lex")
async def handle_lex(request: Request):
    lex_event = await request.json()
    try:
        intent = lex_event['sessionState']['intent']['name']
        slots = lex_event['sessionState']['intent']['slots']
        zip_code = slots['service_zip']['value']['interpretedValue']
        
        outage_zips = ["90210", "12345", "55555"]
        is_outage = "true" if intent == "Report Outage" and zip_code in outage_zips else "false"
        if is_outage == "true":
            report_data = f"Outage reported in {zip_code}"
            s3.put_object(Bucket=BUCKET_NAME, Key=f"outage_{zip_code}.txt", Body=report_data)
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent, "state": "Fulfilled"}
            },
            "sessionAttributes": {
                "service_zip": zip_code,
                "is_outage": is_outage
            }
        }
    except Exception:
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "FallbackIntent", "state": "Failed"}
            },
            "sessionAttributes": {"is_outage": "false", "error": "true"}
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
