import os
import pandas as pd
from glob import glob
from collections import defaultdict

# Liste der Modellordner
model_dirs = [
    "Absatz/Unrelated",
    "DeepSeek-R1-Distill-Llama-8B/Unrelated",
    "DeepSeek-R1-Distill-Qwen-7B/Unrelated",
    "Mistral-7B-Instruct/Unrelated",
    "Qwen2.5-3B-Instruct/Unrelated",
    "Qwen2.5-7B-Instruct/Unrelated",
    "Token/Unrelated"
]

# Alle *_similarity_results.csv-Dateien in den Modellordnern sammeln
all_files = []
for model_dir in model_dirs:
    all_files.extend(glob(os.path.join(model_dir, "*_similarity_results.csv")))

# Dateien nach Basisnamen gruppieren
grouped_files = defaultdict(list)
for file_path in all_files:
    base_name = os.path.basename(file_path)
    grouped_files[base_name].append(file_path)

# Ausgabeordner erstellen
os.makedirs("U", exist_ok=True)

# Jede Datei-Gruppe verarbeiten
for base_name, file_paths in grouped_files.items():
    all_data = []

    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            model_name = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)

            df.insert(0, "Modell", model_name)
            df.insert(1, "Datei", file_name)

            numeric_cols = df.select_dtypes(include='number').columns
            df["Min"] = df[numeric_cols].min(axis=1)

            all_data.append(df)
        except Exception as e:
            print(f"Fehler beim Lesen von {file_path}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df["Mean of Mins per Model"] = combined_df.groupby("Modell")["Min"].transform("mean")

        # Spaltenreihenfolge anpassen
        cols = [col for col in combined_df.columns if col not in ["Min", "Mean of Mins per Model"]]
        cols += ["Min", "Mean of Mins per Model"]
        combined_df = combined_df[cols]

        output_path = os.path.join("Unrelated", base_name.replace(".csv", ".xlsx"))
        combined_df.to_excel(output_path, index=False)
        print(f"Erstellt: {output_path}")
    else:
        print(f"Keine Daten für {base_name}")
