# consumer/kafka_consumer.py

from confluent_kafka import Consumer
import psycopg2
import json
import time
from app.config import *


def connect_db_with_retry():
    for i in range(10):
        try:
            conn = psycopg2.connect(DB_URI)
            print("数据库连接成功")
            return conn
        except Exception as e:
            print(f"第 {i+1}/10 次连接数据库失败：{e}")
            time.sleep(3)
    raise Exception("数据库连接失败，退出")


consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "game-analytics-group",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe([KAFKA_TOPIC])

conn = connect_db_with_retry()
cur = conn.cursor()

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

print("Kafka Consumer 已连接数据库并确保表存在")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue

    try:
        value = msg.value()
        if not value:
            print("收到空消息，跳过")
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
        print("数据已插入数据库")

    except json.JSONDecodeError as e:
        print(f"JSON 解码失败：{e}")
        print(f"原始消息内容：{value}")
    except Exception as e:
        print(f"消费或写入数据库出错：{e}")
