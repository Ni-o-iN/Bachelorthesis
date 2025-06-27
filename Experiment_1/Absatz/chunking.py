import fitz  # PyMuPDF

FILE = "thunder_violin"

# PDF einlesen und Absätze extrahieren
def extract_paragraphs_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    paragraphs = []

    for page in doc:
        blocks = page.get_text("blocks")  # Gibt Textblöcke mit Koordinaten zurück
        for block in blocks:
            text = block[4].strip()
            if text:
                paragraphs.append(text)

    return paragraphs

# Hauptfunktion
def main():
    pdf_path = f"../Experiment_1/all_pdfs/{FILE}.pdf"
    paragraphs = extract_paragraphs_from_pdf(pdf_path)

    # Absätze in Datei speichern
    with open(f"./absatz_chunked_text/{FILE}.txt", "w", encoding="utf-8") as datei:
        for i, paragraph in enumerate(paragraphs, 1):
            datei.write(f"{paragraph}\n\n")

if __name__ == "__main__":
    main()
