import streamlit as st
import pandas as pd
import psycopg2

# Configuration de la page
st.set_page_config(page_title="Dashboard Capteurs", layout="wide")

# Titre
st.title("📈 Dashboard temps réel - Données capteurs")

# Connexion à PostgreSQL
@st.cache_data(ttl=10)  # cache pendant 10 secondes
def get_data():
    conn = psycopg2.connect(
        dbname="capteur_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    query = "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.sort_values(by="timestamp")

# Charger les données
data = get_data()

# Affichage tableau
st.subheader("🧾 Données capteurs (les 100 dernières)")
st.dataframe(data, use_container_width=True)

# Graphiques
st.subheader("🌡️ Température")
st.line_chart(data=data, x="timestamp", y="temperature")

st.subheader("🔵 Pression")
st.line_chart(data=data, x="timestamp", y="pressure")

