import pandas as pd
from sklearn.preprocessing import StandardScaler
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
 
# Charger les données capteurs depuis un fichier CSV
df = pd.read_csv("sensor_data.csv")

# Garder les colonnes nécessaires
df = df[['timestamp', 'temperature', 'pressure']]
df = df.dropna()
df = df.sort_values(by="timestamp")

# Normalisation
scaler = StandardScaler()
scaled = scaler.fit_transform(df[['temperature', 'pressure']])
df[['temperature_scaled', 'pressure_scaled']] = scaled

# Sauvegarde
df.to_csv("cleaned_sensor_data.csv", index=False)
print("✅ Données prétraitées et sauvegardées.")

