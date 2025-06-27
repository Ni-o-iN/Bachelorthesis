import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import re

FILE = "glowing_cat"
MODEL_NAME = "all-mpnet-base-v2"

def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_chunks(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="cp1252") as f:
            content = f.read()
    content = re.sub(r"^.*?</think>", "", content, flags=re.DOTALL)
    return [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]

def read_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        questions = f.readlines()
    return [q.strip() for q in questions if q.strip()]

def cosine_similarity(emb1, emb2):
    return util.pytorch_cos_sim(emb1, emb2).item()

def process_file(file_name):
    print(f"Verarbeite Datei: {file_name}")

    # load text, chunks and questions
    original_text = read_text_file(f"../Experiment_1/original_text/{file_name}.txt")
    chunks = read_chunks(f"../Experiment_1/DeepSeek-R1-Distill-Qwen-7B/chunked_text/{file_name}.txt")
    #questions = read_questions(f"./questions/{file_name}.txt")
    questions = read_questions(f"./questions/unrelated.txt")

    # load model
    model = SentenceTransformer(MODEL_NAME)

    # create embeddings
    original_text_embedding = model.encode(original_text, convert_to_tensor=True)
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    question_embeddings = model.encode(questions, convert_to_tensor=True)

    # calculate similarity
    results = []
    for i, question in enumerate(questions):
        question_embedding = question_embeddings[i]
        row = {
            "Frage": question,
            "Similarity (Gesamter Text)": round(cosine_similarity(question_embedding, original_text_embedding), 4)
        }
        for j, chunk_embedding in enumerate(chunk_embeddings):
            row[f"Similarity (Chunk {j+1})"] = round(cosine_similarity(question_embedding, chunk_embedding), 4)
        results.append(row)

    # Ergebnisse speichern
    df = pd.DataFrame(results)
    df.to_csv(f"DeepSeek-R1-Distill-Qwen-7B/Unrelated/{FILE}_unrelated_similarity_results.csv", index=False, encoding="utf-8")
    print(f"Ergebnisse gespeichert unter: DeepSeek-R1-Distill-Qwen-7B/{file_name}_similarity_results.csv")

# === Ausführung ===
if __name__ == "__main__":
    process_file(FILE)
