# train_models.py
# Entraine et compare deux modeles ML supervises sur les donnees EEG

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump

# === Chargement des donnees ===
df = pd.read_csv("eeg_data_sample.csv")
X = df[["eeg_signal"]]
y = df["seizure"]  # 0 ou 1

# === Normalisation ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Split Train/Test ===
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# === Modele 1 : Random Forest ===
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print("=== Random Forest ===")
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# === Modele 2 : Logistic Regression ===
lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
print("=== Logistic Regression ===")
print(confusion_matrix(y_test, y_pred_lr))
print(classification_report(y_test, y_pred_lr))

# === Sauvegarde du meilleur modele ===
dump(rf, "best_eeg_model.pkl")
dump(scaler, "eeg_scaler.pkl")
print("Modeles sauvegardes.")

