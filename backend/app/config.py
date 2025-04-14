# config.py
# Central configuration file for Kafka, database, and other environment-level variables.

import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "airjumper-analytics")

DB_URI = os.getenv(
    "DB_URI", "dbname=airjumper user=postgres password=secret host=localhost port=5432"
)
