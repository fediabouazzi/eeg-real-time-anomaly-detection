# eeg_to_csv.py
# Ce script extrait les signaux EEG d'un fichier .edf (CHB-MIT dataset)
# et les convertit en CSV avec timestamp.

import mne
import pandas as pd
import os

# === Parametres ===
edf_file = "chb01_01.edf" 
output_csv = "eeg_data_sample.csv"

# === Lecture du fichier EEG ===
print("Chargement du fichier EEG...")
raw = mne.io.read_raw_edf(edf_file, preload=True, verbose=False)

# === Filtrage d'un canal (ex : 'FP1-F7') ===
# Pour simplifier, on ne garde qu'un seul canal ici
canal = raw.ch_names[0]  # ou choisir un canal specifique comme 'FP1-F7'
print(f"Canal utilise : {canal}")

signal, times = raw[canal]
signal = signal[0]  # extraire le tableau 1D

# === Conversion en DataFrame ===
df = pd.DataFrame({
    "timestamp": times,
    "eeg_signal": signal
})

# Ajout d'un flag d'anomalie factice (0 = normal, 1 = crise)
df["seizure"] = 0

# === Export CSV ===
df.to_csv(output_csv, index=False)
print(f"Done. Donnees EEG sauvegardees dans {output_csv}")
