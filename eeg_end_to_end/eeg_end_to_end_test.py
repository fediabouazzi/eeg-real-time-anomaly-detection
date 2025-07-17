# eeg_end_to_end_test.py
# Script de test end-to-end : generation CSV + envoi Kafka + detection en direct

import pandas as pd
import numpy as np
import time
import json
from kafka import KafkaProducer, KafkaConsumer
from joblib import load
from sklearn.preprocessing import StandardScaler
import os

# === Etape 1 : Generer un petit dataset EEG ===
def generate_sample_eeg(filename="/app/eeg_test.csv", samples=20):
    timestamps = pd.date_range(start="2025-01-01", periods=samples, freq="200ms")
    eeg_signal = np.random.normal(0, 1, samples)
    # Injecter des anomalies (simulées)
    eeg_signal[::7] += np.random.normal(5, 2, len(eeg_signal[::7]))
    seizure = [1 if abs(val) > 3 else 0 for val in eeg_signal]

    df = pd.DataFrame({
        "timestamp": timestamps.astype(str),
        "eeg_signal": eeg_signal,
        "seizure": seizure
    })
    df.to_csv(filename, index=False)
    print(f"✅ Fichier {filename} genere avec {samples} lignes.")
    return df

# === Etape 2 : Envoi dans Kafka ===
def send_to_kafka(df, topic="eeg_data", delay=0.1):
    producer = KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print("🔄 Envoi des donnees vers Kafka...")
    for _, row in df.iterrows():
        data = {
            "timestamp": row["timestamp"],
            "eeg_signal": row["eeg_signal"],
            "seizure": row["seizure"]
        }
        producer.send(topic, value=data)
        print(f"🟢 Envoye : {data}")
        time.sleep(delay)
    producer.flush()
    print("✅ Tous les signaux ont ete envoyes.")

# === Etape 3 : Detection temps reel ===
def detect_from_kafka(topic="eeg_data", count=20):
    model = load("/app/best_eeg_model.pkl")
    scaler = load("/app/eeg_scaler.pkl")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset='earliest',
        group_id='eeg_test_group',
        enable_auto_commit=False
    )
    print("👁️ Detection des crises EEG en temps reel...")
    i = 0
    for message in consumer:
        data = message.value
        signal_scaled = scaler.transform([[data["eeg_signal"]]])
        prediction = model.predict(signal_scaled)[0]
        alert = "🚨 CRISE" if prediction == 1 else "✅ OK"
        print(f"{data['timestamp']} | EEG: {data['eeg_signal']:.3f} | Pred: {prediction} | {alert}")
        i += 1
        if i >= count:
            break

# === MAIN ===
if __name__ == "__main__":
    df = generate_sample_eeg()
    send_to_kafka(df)
    detect_from_kafka()

