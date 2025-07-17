import pandas as pd
import matplotlib.pyplot as plt

# Charger les données CSV
df = pd.read_csv('sensor_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convertir en datetime

# Tracer les données
plt.figure(figsize=(14, 6))

# Température
plt.subplot(2, 1, 1)
plt.plot(df['timestamp'], df['temperature'], label='Température', color='tab:red')
plt.title("Température des capteurs")
plt.ylabel("Température (°C)")
plt.grid(True)

# Pression
plt.subplot(2, 1, 2)
plt.plot(df['timestamp'], df['pressure'], label='Pression', color='tab:blue')
plt.title("Pression des capteurs")
plt.ylabel("Pression (bar)")
plt.xlabel("Temps")
plt.grid(True)

plt.tight_layout()
plt.show()

