# eeg_kafka_producer.py
# Envoie les donnees EEG ligne par ligne dans Kafka

import pandas as pd
import time
import json
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

load_dotenv()

# === Parametres Kafka ===
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "eeg_data")

# === Chargement des donnees EEG ===
df = pd.read_csv("eeg_data_sample.csv")
print(f"Total lignes a envoyer : {len(df)}")

# === Configuration du Producer ===
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# === Envoi ligne par ligne ===
for i, row in df.iterrows():
    data = {
        "timestamp": row["timestamp"],
        "eeg_signal": row["eeg_signal"],
        "seizure": row["seizure"]  # 0 ou 1
    }
    producer.send(KAFKA_TOPIC, value=data)
    print(f"[Kafka] {data}")
    time.sleep(0.05)  # simule un flux temps reel (20 Hz)

producer.flush()
print("Envoi termine.")
