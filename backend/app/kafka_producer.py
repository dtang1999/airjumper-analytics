# kafka_producer.py
# Defines the Kafka producer that sends JSON-encoded game analytics data to a specified topic.

from confluent_kafka import Producer
import json
from app.config import KAFKA_BROKER, KAFKA_TOPIC

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def send_to_kafka(payload: dict):
    # Produce JSON data to the configured Kafka topic
    producer.produce(KAFKA_TOPIC, json.dumps(payload).encode('utf-8'))
    producer.flush()

# def send_to_kafka(payload: dict):
#     # 模拟发送逻辑，只打印
#     print("[Kafka DISABLED] Would send payload:")
#     print(payload)
