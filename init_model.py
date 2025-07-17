import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Charger les données
df = pd.read_csv("cleaned_sensor_data.csv")

# Sélection des colonnes utiles
features = df[['temperature', 'pressure']]

# Standardisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# Entraînement du modèle Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
model.fit(X_scaled)

# Sauvegarde du modèle
joblib.dump(model, "isoforest_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Modèle Isolation Forest et scaler sauvegardés.")

