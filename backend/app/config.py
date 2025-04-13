# config.py
# Central configuration file for Kafka, database, and other environment-level variables.

# Kafka broker address
KAFKA_BROKER = "kafka:9092"

# Kafka topic for game analytics
KAFKA_TOPIC = "airjumper-analytics"

# PostgreSQL database connection URI
DB_URI = "dbname=airjumper user=postgres password=secret host=localhost port=5432"
