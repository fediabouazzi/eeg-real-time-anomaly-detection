import pandas as pd
from kafka import KafkaConsumer
import json
import joblib
from sklearn.preprocessing import StandardScaler
import csv
import os

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

# Charger le modèle
model = joblib.load("isoforest_model.pkl")

# Chargement du scaler d'origine (optionnel, sinon refaire un fit)
scaler = joblib.load("scaler.pkl")

# Préparer le consommateur
consumer = KafkaConsumer(
    'sensor-topic',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🟢 En attente de données Kafka...")

for msg in consumer:
    data = msg.value
    df = pd.DataFrame([data])

    # Normalisation dynamique (à adapter si besoin)
    df[['temperature', 'pressure']] = scaler.fit_transform(df[['temperature', 'pressure']])

    # Prédiction
    prediction = model.predict(df[['temperature', 'pressure']])[0]
    is_anomaly = 1 if prediction == -1 else 0
    data['anomaly'] = is_anomaly

    print("📡 Reçu :", data)

#sauvegarde dans un fichier csv tampon 
file_exists = os.path.isfile("realtime_anomaly_log.csv")
with open("realtime_anomaly_log.csv", mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["timestamp", "temperature", "pressure", "anomaly"])
    if not file_exists:
        writer.writeheader()
    writer.writerow({
        "timestamp": data['timestamp'],
        "temperature": data['temperature'],
        "pressure": data['pressure'],
        "anomaly": data['anomaly']
    })
