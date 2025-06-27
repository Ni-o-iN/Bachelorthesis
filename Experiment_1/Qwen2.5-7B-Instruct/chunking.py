import os
import platform
import requests
import urllib.parse
import fitz
import re

URL_LLM = "http://10.104.199.118:30002/query-stream/?"
FILE = "thunder_violin"

def _clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def read_file(dir_doc):
    with open(dir_doc, "rb") as f:
        pdf_stream = f.read()
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        all_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            all_text += page.get_text()
        chunks = re.split(r"(?<=[.!?])\s*\n", all_text)
    return chunks
# ----------------------------------------------------

def main():
    seed = 42
    # _clear_screen()

    clear_url = "http://10.104.199.118:30002/clear-history/"
    requests.get(clear_url)

    text = read_file(f"all_pdfs/{FILE}.pdf")

    single_string = " ".join(text)

    
    single_line_string = single_string.replace("\n", "")

    with open(f"original_text/{FILE}.txt", "w") as datei:
        datei.write(single_line_string)

    query = f"""Task: Extract Knowledge Chunks
            Please split the following text into separte chunks based on its semantic meaning.
            Each Chunk should group together sentences or parts that discuss the same idea or concept.
            Do not change or paraphrase the original text, only insert line breaks to seperate the chunks.
            Keep chunks short: Smaller chunks generally improve focus and coherence.
            But remember that they don't necessarily have to be short, because some sentences build on each other and individually it looks like something completely different.

            
            Example 1: 
            Input:
            Apples are a fruit. They are sweet and chrunchy. Sometimes they can be red and sometimes they can be green. Bananas are another popular fruit. They are rich in potassium.

            Output:
            Apples are a fruit. They are sweet and chrunchy. Sometimes they can be red and sometimes they can be green.

            Bananas are another popular fruit. They are rich in potassium.

            
            Example 2:
            Input:
            Ants are fascinating insects that belong to the family Formicidae. They are social creatures, living in colonies that can range from a few dozen to millions of individuals. Each colony
            has a complex social structure, typically consisting of a queen, workers, and sometimes males. The queen's primary role is to reproduce, while the workers maintain the nest,
            forage for food, and care for the young. Males usually have a short lifespan and are primarily involved in mating. Ants communicate through chemical signals known as pheromones. These pheromones
            help them coordinate activities such as foraging, defense, and nest building. Ants are known for their remarkable ability to work together and solve problems. For example, they
            can form bridges with their bodies to cross gaps and can carry objects many times their own weight.

            Output:
            Ants are fascinating insects that belong to the family Formicidae. They are social creatures, living in colonies that can range from a few dozen to millions of individuals. Each colony
            has a complex social structure, typically consisting of a queen, workers, and sometimes males. The queen's primary role is to reproduce, while the workers maintain the nest,
            forage for food, and care for the young. Males usually have a short lifespan and are primarily involved in mating.

            Ants communicate through chemical signals known as pheromones. These pheromones help them coordinate activities such as foraging, defense, and nest building. Ants are known for their 
            remarkable ability to work together and solve problems. For example, they can form bridges with their bodies to cross gaps and can carry objects many times their own weight.

            
            Now split this following text:
            {single_string}
            """
        
    partial_text = ""

    # request to server:
    url_ = URL_LLM + "query={" + urllib.parse.quote(query.replace("\n", "")) + "}"
 
    req = requests.get(url_, stream=True)

    for chunk in req.iter_content(1024): 
        new_text = chunk.decode()
        partial_text += new_text

    with open(f"chunked_text/{FILE}.txt", "w") as datei:
        datei.write(partial_text)

if __name__ == "__main__":
    main()

