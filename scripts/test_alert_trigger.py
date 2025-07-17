import pandas as pd
import smtplib
from email.message import EmailMessage

def send_email(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = "isimm.ingenieure@gmail.com"
    msg["To"] = to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("isimm.ingenieure@gmail.com", "fedia")
        smtp.send_message(msg)

try:
    df = pd.read_csv("realtime_anomaly_log.csv")
    if len(df) > 0:
        print(f"✅ {len(df)} anomalies detected.")
        send_email(
            "🚨 Anomalies detected!",
            f"{len(df)} anomalies found in realtime logs.",
            "destination_email@example.com"
        )
    else:
        print("⚠️ No anomalies detected.")
except FileNotFoundError:
    print("❌ Log file not found.")

