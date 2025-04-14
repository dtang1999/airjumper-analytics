from confluent_kafka import Consumer
import psycopg2
import json
import time
from app.config import *


# Attempt to connect to PostgreSQL with retry logic
def connect_db_with_retry():
    for i in range(10):
        try:
            conn = psycopg2.connect(DB_URI)
            print("Database connection successful.")
            return conn
        except Exception as e:
            print(f"Attempt {i+1}/10 - Failed to connect to database: {e}")
            time.sleep(3)
    raise Exception("Database connection failed after multiple attempts.")


# Configure and start Kafka consumer
consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "game-analytics-group",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe([KAFKA_TOPIC])

# Connect to the database and create cursor
conn = connect_db_with_retry()
cur = conn.cursor()

# Create the analytics table if it doesn't exist
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS airjumper_analytics (
        id SERIAL PRIMARY KEY,
        session_id TEXT,
        level_index INT,
        regular_platform_count INT,
        building_platform_count INT,
        total_jump_count INT,
        game_over_count INT,
        time_to_flag FLOAT,
        jumps_to_flag INT,
        health_after_kills JSONB,
        checkpoint_data JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    )
"""
)
conn.commit()
print("Kafka consumer connected to the database and ensured table exists.")

# Continuously consume and process messages
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue

    try:
        value = msg.value()
        if not value:
            print("Empty message received. Skipping.")
            continue

        data = json.loads(value)

        cur.execute(
            """
            INSERT INTO airjumper_analytics (
                session_id, level_index, regular_platform_count,
                building_platform_count, total_jump_count, game_over_count,
                time_to_flag, jumps_to_flag, health_after_kills, checkpoint_data
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                data["session_id"],
                data["level_index"],
                data["regular_platform_count"],
                data["building_platform_count"],
                data["total_jump_count"],
                data["game_over_count"],
                data["time_to_flag"],
                data["jumps_to_flag"],
                json.dumps(data.get("health_after_kills")),
                json.dumps(data.get("checkpoint_data")),
            ),
        )
        conn.commit()
        print("Data inserted into database.")

    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print(f"Raw message: {value}")
    except Exception as e:
        print(f"Error during message processing or database insertion: {e}")
