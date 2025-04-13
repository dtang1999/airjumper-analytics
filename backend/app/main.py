# main.py
# Entry point for the FastAPI application.
# Defines the route to receive analytics data from Unity and forwards it to Kafka.

from fastapi import FastAPI
from app.models import AnalyticsPayload
from app.kafka_producer import send_to_kafka
from app.kafka_health import router as kafka_health_router


app = FastAPI()

@app.post("/analytics")
async def receive_analytics(data: AnalyticsPayload):
    # Serialize and send the received analytics data to Kafka
    send_to_kafka(data.model_dump())
    return {"status": "queued"}

app.include_router(kafka_health_router)
    
