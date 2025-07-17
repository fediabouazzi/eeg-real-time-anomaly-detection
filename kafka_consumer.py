from kafka import KafkaConsumer
import json
import psycopg2

# Connexion à la base PostgreSQL
conn = psycopg2.connect(
    dbname="capteur_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Initialisation du consommateur Kafka
consumer = KafkaConsumer(
    'sensor-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🟢 En attente de messages depuis Kafka...\n")

# Boucle de consommation
for message in consumer:
    data = message.value
    print("✅ Message reçu :", data)

    # Insertion dans PostgreSQL
    try:
        cursor.execute(
            """
            INSERT INTO sensor_data (timestamp, temperature, pressure)
            VALUES (%s, %s, %s)
            """,
            (data['timestamp'], data['temperature'], data['pressure'])
        )
        conn.commit()
        print("📝 Données insérées dans PostgreSQL.\n")
    except Exception as e:
        print("❌ Erreur d'insertion :", e)
        conn.rollback()


