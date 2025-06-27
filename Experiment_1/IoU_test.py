from difflib import SequenceMatcher
import re
import csv
import os

FOLDER = "Token"

def load_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="cp1252") as f:
            content = f.read()
    content = re.sub(r"^.*?</think>", "", content, flags=re.DOTALL)
    return content


def compute_word_alignment_metrics(original_text, chunked_text):
    original_words = original_text.split()
    chunked_words = chunked_text.split()

    matcher = SequenceMatcher(None, original_words, chunked_words)
    matching_blocks = matcher.get_matching_blocks()

    intersection = []
    for block in matching_blocks:
        if block.size > 0:
            intersection.extend(original_words[block.a:block.a + block.size])

    union = len(original_words) + len(chunked_words) - len(intersection)
    iou = len(intersection) / union if union else 0

    diffs_original = []
    diffs_chunked = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            diffs_original.extend(original_words[i1:i2])
            diffs_chunked.extend(chunked_words[j1:j2])

    return original_words, chunked_words, intersection, union, iou, diffs_original, diffs_chunked


def analyze_chunks(text):
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    num_chunks = len(chunks)
    avg_words = sum(len(chunk.split()) for chunk in chunks) / num_chunks if num_chunks else 0
    return num_chunks, avg_words


def write_results_to_csv(filename, original_words, chunked_words, num_chunks, avg_words, intersection, union, iou, only_in_original, only_in_chunked):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Metrik", "Wert"])
        writer.writerow(["Wörter im Originaltext", len(original_words)])
        writer.writerow(["Wörter im Gechunkten Text", len(chunked_words)])
        writer.writerow(["Anzahl der Chunks", num_chunks])
        writer.writerow(["Durchschnittliche Wortanzahl pro Chunk", f"{avg_words:.2f}"])
        writer.writerow(["Übereinstimmende Wörter (Intersection)", len(intersection)])
        writer.writerow(["Union", union])
        writer.writerow(["IoU", f"{iou:.4f}"])
        writer.writerow(["Nur im Original", " ".join(only_in_original)])
        writer.writerow(["Nur im Gechunkten", " ".join(only_in_chunked)])

def main():
    original_dir = "original_text"
    chunked_dir = f"{FOLDER}/chunked_text"
    output_dir = f"{FOLDER}/IoU_results"

    for filename in os.listdir(original_dir):
        if filename.endswith(".txt"):
            file_base = os.path.splitext(filename)[0]
            original_path = os.path.join(original_dir, filename)
            chunked_path = os.path.join(chunked_dir, f"{file_base}.txt")

            if not os.path.exists(chunked_path):
                print(f"Chunked file for {file_base} not found. Skipping.")
                continue

            original_text = load_text(original_path)
            chunked_text = load_text(chunked_path)

            original_words, chunked_words, intersection, union, iou, only_in_original, only_in_chunked = compute_word_alignment_metrics(original_text, chunked_text)
            num_chunks, avg_words = analyze_chunks(chunked_text)

            output_path = os.path.join(output_dir, f"{file_base}_results.csv")
            write_results_to_csv(output_path, original_words, chunked_words, num_chunks, avg_words, intersection, union, iou, only_in_original, only_in_chunked)

if __name__ == "__main__":
    main()