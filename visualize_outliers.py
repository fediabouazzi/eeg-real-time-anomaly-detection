import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données prétraitées
df = pd.read_csv("cleaned_sensor_data.csv")

# 1. Boxplots pour visualiser les outliers
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.boxplot(y=df['temperature'])
plt.title("Boxplot - Température")

plt.subplot(1, 2, 2)
sns.boxplot(y=df['pressure'])
plt.title("Boxplot - Pression")

plt.tight_layout()
plt.show()

# 2. Scatter plot dans le temps
plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(df['timestamp'], df['temperature'], color='red', label='Température')
plt.ylabel("°C")
plt.title("Température dans le temps")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(df['timestamp'], df['pressure'], color='blue', label='Pression')
plt.ylabel("bar")
plt.title("Pression dans le temps")
plt.grid(True)

plt.tight_layout()
plt.show()

