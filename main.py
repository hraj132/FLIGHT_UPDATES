from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from twilio.rest import Client
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client["flight"]
flights_collection = db["flight_data"]

class FlightRequest(BaseModel):
    name: str
    flightDetails: str
    mobileNumber: str

def send_sms(mobile_number, message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")  #  Account SID
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")   # Auth Token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=mobile_number,
        from_=os.getenv("TWILIO_PHONE_NUMBER"),  #  Twilio number
        body=message)

    print(message.sid)

@app.post("/get-flight-status")
async def get_flight_status(flight_request: FlightRequest):
    print(f"Received request: {flight_request}")
    flight = flights_collection.find_one({"flightDetails": flight_request.flightDetails})
    print(f"Query result: {flight}")
    
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    status_message = f"Flight {flight_request.flightDetails} status: {flight['status']}"
    send_sms(flight_request.mobileNumber, status_message)

    return {"status": flight["status"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
