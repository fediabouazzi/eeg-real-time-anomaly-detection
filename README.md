
# eeg-real-time-anomaly-detection
Real-time seizure detection using EEG signals – Kafka, Machine Learning, Streamlit, Docker

# 🚀 Real-Time Anomaly Detection Pipeline

📡 **Kafka + Python + ML + Streamlit + PostgreSQL + Docker Compose**

Ce projet simule et détecte en temps réel des anomalies dans des données de capteurs. Il est conçu pour apprendre les outils modernes utilisés en **data engineering**, **machine learning** et **monitoring temps réel**.

---

## 🧱 Architecture
```
(sensor_data.csv) → [Trainer] → model.pkl
                          ↓
                      Kafka ← producer
                          ↓
                  [Consumer] → detect anomalies
                          ↓
           [CSV + PostgreSQL] ← Store anomalies
                          ↓
                   [Streamlit] ← Dashboard live
```

---

## 🛠 Technologies utilisées
- **Kafka** : streaming temps réel
- **Scikit-learn (Isolation Forest)** : détection d’anomalies
- **Streamlit** : visualisation & alertes
- **PostgreSQL** : base de données pour stockage persistant
- **Docker Compose** : orchestration de l’architecture complète

---

## 📁 Structure du projet
```
├── data_generator.py            # Génère des données de capteurs (avec anomalies)
├── kafka_producer.py           # Envoie les données dans Kafka
├── kafka_real_time_detector.py # Détection d’anomalies en direct (consumer)
├── init_model.py               # Entraîne et sauvegarde le modèle Isolation Forest
├── preprocessing.py            # Nettoyage et mise en forme des données
├── streamlit_anomaly_dashboard.py # Dashboard local
├── realtime_anomaly_log.csv    # Historique des anomalies détectées
├── Dockerfile.*                # 3 images : trainer, consumer, streamlit
├── docker-compose.yml          # Lance toute l'architecture
├── Makefile                    # Commandes utiles
└── hf_space/                   # Version Streamlit pour Hugging Face Spaces
```

---

## ▶️ Lancer le projet (local avec Docker Compose)
```bash
git clone <repo>
cd anomaly_detection_project
make up
```

🌍 Accéder au dashboard : [http://localhost:8501](http://localhost:8501)

---

## 🧪 Tester l’envoi de données + détection automatique
```bash
make test
```

📬 Un email est envoyé si une anomalie est détectée (optionnel si SMTP configuré).

---

## 🛰 Déployer sur Hugging Face Spaces
1. Aller sur [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Créer un Space (SDK : Streamlit)
3. Copier le dossier `hf_space/`
4. Lancer :
```bash
make sync-hf
```

---
## 🔐 Configuration des variables sensibles

Le projet utilise un fichier `.env` pour stocker toutes les variables sensibles (base de données, Kafka, e-mail, etc.).

- Exemple :
```ini
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret123
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

- Ne jamais commiter ce fichier `.env`. Il est déjà ignoré via `.gitignore`
- Un fichier `.env.example` est fourni comme modèle. Pour l'utiliser :
```bash
cp .env.example .env
```
Puis remplissez-le avec vos vraies informations.

Toutes les applications (Python, Docker Compose, Streamlit) chargeront automatiquement les variables définies dans `.env`



## ✅ Idéal pour apprendre à :
- manipuler des flux de données
- intégrer machine learning en production
- automatiser un pipeline avec Docker
- exposer des résultats via un dashboard web
## 👤 Réalisé par Fedia BOUAZZI 
>>>>>>> ea78ea4 (Initial commit of EEG end-to-end anomaly detection project)
