from kafka import KafkaProducer
import pandas as pd
import time
import json
from dotenv import load_dotenv
import os
load_dotenv()
KAFKA_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Charger les données
df = pd.read_csv("sensor_data.csv")

# Initialiser le producteur
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Envoyer les données ligne par ligne
for _, row in df.iterrows():
    message = {
        'timestamp': row['timestamp'],
        'temperature': row['temperature'],
        'pressure': row['pressure']
    }
    producer.send('sensor-topic', message)
    print("Message envoyé :", message)
    time.sleep(1)  # simule un capteur en temps réel

producer.flush()

