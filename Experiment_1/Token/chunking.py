import fitz 
import re

FILE = "hydrogen_coffee_mug"

# PDF einlesen und Text extrahieren
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Text in gleich große Chunks aufteilen
def chunk_text(text, chunk_size):
    words = text.split()  # Text in Wörter aufteilen
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def fix_hyphen_spacing(text):
    text = re.sub(r"-\s+", "-", text)
    text = re.sub(r"/\s+", "/", text)
    return text

# Hauptfunktion
def main():
    pdf_path = (f"../all_pdfs/{FILE}.pdf")
    chunk_size = 80  # Anzahl der Wörter pro Chunk
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size)

    
    with open(f"chunked_text/{FILE}.txt", "w") as datei:
        for chunk in chunks:
            cleaned_chunk = fix_hyphen_spacing(chunk)
            datei.write(cleaned_chunk + "\n\n")



if __name__ == "__main__":
    main()
