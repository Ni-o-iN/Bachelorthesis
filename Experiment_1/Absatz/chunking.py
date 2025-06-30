import fitz  # PyMuPDF
import re

FILE = "hydrogen_coffee_mug"

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

def fix_hyphen_spacing(text):
    # Entfernt Leerzeichen nach Bindestrichen, z. B. "eco- friendly" → "eco-friendly"
    return re.sub(r"-\s+", "-", text)

# Hauptfunktion
def main():
    pdf_path = f"../all_pdfs/{FILE}.pdf"
    paragraphs = extract_paragraphs_from_pdf(pdf_path)

    # Absätze in Datei speichern
    with open(f"chunked_text/{FILE}.txt", "w", encoding="utf-8") as datei:
        for i, paragraph in enumerate(paragraphs, 1):
            cleaned_paragraph = fix_hyphen_spacing(paragraph)
            datei.write(f"{cleaned_paragraph}\n\n")

if __name__ == "__main__":
    main()
