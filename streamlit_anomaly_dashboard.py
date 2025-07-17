import pandas as pd
import streamlit as st
import time

st.set_page_config(page_title="Détection d'anomalies temps réel", layout="wide")
st.title("🔍 Détection d'anomalies capteurs (temps réel)")

# Rafraîchissement automatique
REFRESH_INTERVAL = 5  # secondes

# Boucle de mise à jour
while True:
    try:
        df = pd.read_csv("realtime_anomaly_log.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        
        st.subheader("📡 Dernière lecture")
        last = df.iloc[-1]
        status = "🔴 Anomalie" if last['anomaly'] == 1 else "🟢 Normal"
        st.metric(label="Température", value=f"{last['temperature']:.2f} °C", delta=status)

        st.subheader("📊 Évolution de la température")
        st.line_chart(
            df.set_index("timestamp")[["temperature"]]
        )

        st.subheader("🧯 Points anormaux détectés")
        st.dataframe(df[df['anomaly'] == 1].tail(10), use_container_width=True)

        time.sleep(REFRESH_INTERVAL)
        st.rerun()

    except Exception as e:
        st.warning(f"En attente de données... ({e})")
        time.sleep(REFRESH_INTERVAL)
        st.rerun()

