import os
import pandas as pd

FILE = "paper_eclipse"

# Liste der konkreten CSV-Dateipfade
files = [
    f"Absatz/Related/{FILE}_similarity_results.csv",
    f"DeepSeek-R1-Distill-Llama-8B/Related/{FILE}_similarity_results.csv",
    f"DeepSeek-R1-Distill-Qwen-7B/Related/{FILE}_similarity_results.csv",
    f"Mistral-7B-Instruct/Related/{FILE}_similarity_results.csv",
    f"Qwen2.5-3B-Instruct/Related/{FILE}_similarity_results.csv",
    f"Qwen2.5-7B-Instruct/Related/{FILE}_similarity_results.csv",
    f"Token/Related/{FILE}_similarity_results.csv"
]

# Liste für alle Daten
all_data = []

# Durchlaufe alle Dateipfade
for file_path in files:
    if not os.path.exists(file_path):
        print(f"Datei nicht gefunden: {file_path}")
        continue

    try:
        df = pd.read_csv(file_path)
        model_name = os.path.dirname(file_path)  # Ordnername als Modellname
        file_name = os.path.basename(file_path)  # Dateiname

        df.insert(0, "Modell", model_name)
        df.insert(1, "Datei", file_name)

        all_data.append(df)
    except Exception as e:
        print(f"Fehler beim Lesen von {file_path}: {e}")

# Zusammenführen und speichern
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.to_excel(f"Vergleiche/{FILE}.xlsx", index=False)
    print(f"Excel-Datei '{FILE}.xlsx' wurde erfolgreich erstellt.")
else:
    print("Keine Daten gefunden. Bitte überprüfe die Dateipfade.")
