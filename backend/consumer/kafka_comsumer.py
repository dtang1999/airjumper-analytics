# consumer/kafka_consumer.py

from confluent_kafka import Consumer
import psycopg2, json
from app.config import *

consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'game-analytics-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([KAFKA_TOPIC])

conn = psycopg2.connect(DB_URI)
cur = conn.cursor()

while True:
    msg = consumer.poll(1.0)
    if msg is None: continue

    data = json.loads(msg.value())
    cur.execute("""
        INSERT INTO airjumper_analytics (
            session_id, level_index, regular_platform_count,
            building_platform_count, total_jump_count, game_over_count,
            time_to_flag, jumps_to_flag, health_after_kills, checkpoint_data
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['session_id'], data['level_index'], data['regular_platform_count'],
        data['building_platform_count'], data['total_jump_count'], data['game_over_count'],
        data['time_to_flag'], data['jumps_to_flag'],
        json.dumps(data.get('health_after_kills')),
        json.dumps(data.get('checkpoint_data'))
    ))
    conn.commit()
