import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Paramètres
N = 1000  # Nombre de lignes
start_time = datetime.now()
time_interval = timedelta(seconds=10)

timestamps = [start_time + i * time_interval for i in range(N)]
temperature = np.random.normal(loc=25, scale=2, size=N)  # Moyenne 25°C, écart 2°C
pressure = np.random.normal(loc=1.0, scale=0.05, size=N)  # 1.0 bar

# Ajout d’anomalies
for i in random.sample(range(N), 10):
    temperature[i] += random.uniform(10, 20)  # Températures très élevées
for i in random.sample(range(N), 5):
    pressure[i] -= random.uniform(0.3, 0.5)  # Pression très basse

# Création DataFrame
df = pd.DataFrame({
    'timestamp': timestamps,
    'temperature': temperature,
    'pressure': pressure
})

# Sauvegarde CSV
df.to_csv('sensor_data.csv', index=False)

print("✅ Données générées dans 'sensor_data.csv'")

