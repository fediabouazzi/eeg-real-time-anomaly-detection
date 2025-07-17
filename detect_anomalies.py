import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
# Charger les données prétraitées
df = pd.read_csv("cleaned_sensor_data.csv")

# Sélection des features normalisées
X = df[['temperature_scaled', 'pressure_scaled']]

# Création du modèle
model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
df['anomaly'] = model.fit_predict(X)

# Mapping résultat (-1 = anomalie, 1 = normal)
df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

# Nombre d’anomalies détectées
print(f"✅ Nombre total d’anomalies détectées : {df['anomaly'].sum()}")

# Affichage des anomalies dans le temps
plt.figure(figsize=(14, 6))
sns.scatterplot(data=df, x="timestamp", y="temperature", hue="anomaly", palette=["blue", "red"])
plt.title("Détection d'anomalies - Température")
plt.xlabel("Temps")
plt.ylabel("Température")
plt.legend(title="Anomalie", labels=["Normal", "Anomalie"])
plt.grid(True)
plt.tight_layout()
plt.show()

# Sauvegarde des résultats
df.to_csv("sensor_data_with_anomalies.csv", index=False)


# Sauvegarde du modèle
joblib.dump(model, "isoforest_model.pkl")
print("✅ Modèle Isolation Forest sauvegardé.")
