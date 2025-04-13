from fastapi import APIRouter
from confluent_kafka import Producer
from confluent_kafka.cimpl import KafkaException

router = APIRouter()


@router.get("/health/kafka")
async def kafka_health_check():
    try:
        producer = Producer({"bootstrap.servers": "kafka:9092"})
        metadata = producer.list_topics(timeout=2.0)
        broker_info = [f"{b.id}: {b.host}:{b.port}" for b in metadata.brokers.values()]
        return {
            "status": "connected",
            "message": "Kafka is reachable.",
            "brokers": broker_info,
        }
    except KafkaException as e:
        return {"status": "error", "message": f"Kafka connection failed: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}
