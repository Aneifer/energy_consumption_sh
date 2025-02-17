import os
import glob
import pandas as pd

# Pfade definieren
RAW_DATA_DIR = "data/raw-data"
CLEANED_DATA_DIR = "data/cleaned-data"
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)

# Liste aller *.csv.gz-Dateien im RAW_DATA_DIR
csv_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv.gz"))

# Leere Liste für DataFrames
dfs = []

for file_path in csv_files:
    print(f"Lese Datei: {file_path}")
    # Mit Pandas direkt einlesen (kompression wird erkannt)
    df = pd.read_csv(file_path, compression="gzip")
    dfs.append(df)

# Alle DataFrames zu einem zusammenführen
combined_df = pd.concat(dfs, ignore_index=True)

# Pfad für das gemeinsame CSV
OUTPUT_PATH = os.path.join(CLEANED_DATA_DIR, "ckw_opendata_smartmeter_dataset_b_all.csv")

# Speichern als CSV (ohne Index)
combined_df.to_csv(OUTPUT_PATH, index=False)

print(f"Alle Dateien erfolgreich kombiniert und gespeichert unter {OUTPUT_PATH}")
