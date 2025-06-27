import fitz 

FILE = "thunder_violin"

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

# Hauptfunktion
def main():
    pdf_path = (f"../Experiment_1/chunked_text/{FILE}.txt")
    chunk_size = 80  # Anzahl der Wörter pro Chunk
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size)

    with open(f"./token_length_chunked_text/{FILE}.txt", "w") as datei:
        for chunk in chunks:
            datei.write(chunk + "\n\n")


if __name__ == "__main__":
    main()
