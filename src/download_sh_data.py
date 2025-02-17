import os
import requests
from bs4 import BeautifulSoup

# Basis-URL, an die relative Pfade angehängt werden
BASE_URL = "https://open.data.axpo.com/%24web/"

# URL der Seite mit den Datensätzen
PAGE_URL = "https://open.data.axpo.com/%24web/index.html"

# Zielordner, in den die heruntergeladenen Dateien gespeichert werden
OUTPUT_DIR = "data/raw-data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# HTML der Seite abrufen
response = requests.get(PAGE_URL)
response.raise_for_status()

# HTML parsen
soup = BeautifulSoup(response.text, "html.parser")

# Suche nach dem Bereich, der den Datensatz B enthält
dataset_b_panel = soup.find("div", id="dataset-b-panel")
if not dataset_b_panel:
    print("Datensatz B Panel nicht gefunden.")
    exit(1)

# In diesem Bereich die Tabelle mit der Klasse "table table-hover" finden
table = dataset_b_panel.find("table", class_="table table-hover")
if not table:
    print("Datensatz B Tabelle nicht gefunden.")
    exit(1)

# Alle Zeilen im <tbody> der Tabelle auslesen
tbody = table.find("tbody")
rows = tbody.find_all("tr")

# Für jede Zeile:
for row in rows:
    # Die erste Zelle enthält den Dateinamen (als <th scope="row">)
    file_cell = row.find("th", scope="row")
    if not file_cell:
        continue

    file_name = file_cell.get_text(strip=True)
    # Nur Dateien mit "ckw_opendata_smartmeter_dataset_b_" berücksichtigen
    if "ckw_opendata_smartmeter_dataset_b_" in file_name:
        # Der Download-Link befindet sich im <a>-Tag in der letzten Zelle
        a_tag = row.find("a")
        if not a_tag:
            continue

        href = a_tag.get("href")
        # Zusammensetzen der vollständigen URL
        download_url = BASE_URL + href

        print(f"Lade {file_name} von {download_url} herunter ...")
        try:
            file_response = requests.get(download_url)
            file_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Fehler beim Herunterladen von {file_name}: {e}")
            continue

        # Speichern im Zielordner
        file_path = os.path.join(OUTPUT_DIR, file_name)
        with open(file_path, "wb") as f:
            f.write(file_response.content)
        print(f"{file_name} erfolgreich gespeichert unter {file_path}")
