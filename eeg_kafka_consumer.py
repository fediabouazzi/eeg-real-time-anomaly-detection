# eeg_kafka_consumer.py
# Consomme les donnees EEG depuis Kafka et predit les crises avec un modele supervise

from kafka import KafkaConsumer
import json
import joblib
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

# === Parametres Kafka ===
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "eeg_data")

# === Chargement du modele et scaler ===
model = joblib.load("best_eeg_model.pkl")
scaler = joblib.load("eeg_scaler.pkl")
print("Modele et scaler charges.")

# === Kafka Consumer ===
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='latest',
    group_id='eeg_anomaly_group',
    enable_auto_commit=True
)

print(f"En attente de donnees EEG sur le topic '{KAFKA_TOPIC}'...")

for message in consumer:
    data = message.value
    signal = np.array([[data["eeg_signal"]]])
    signal_scaled = scaler.transform(signal)

    prediction = model.predict(signal_scaled)[0]
    alert = "🚨 CRISE DETECTEE !" if prediction == 1 else "✅ Normal"

    print(f"[{data['timestamp']}] Signal: {data['eeg_signal']:.4f} | Pred: {prediction} -> {alert}")

