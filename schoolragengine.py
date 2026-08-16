import fitz
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# LOAD PDF
# -----------------------------

pdf = fitz.open("finaldemoschool.pdf")

all_text = ""

for page in pdf:
    all_text += page.get_text() + "\n\n"


# -----------------------------
# CREATE CHUNKS
# -----------------------------

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_text(all_text)

print("Number of Chunks:", len(chunks))


# -----------------------------
# CREATE LIGHTWEIGHT VECTORS
# -----------------------------

vectorizer = TfidfVectorizer()

embeddings = vectorizer.fit_transform(chunks).toarray().astype("float32")

print("Embeddings Shape:", embeddings.shape)


# -----------------------------
# CREATE FAISS INDEX
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


# -----------------------------
# ASK QUESTION
# -----------------------------

def ask_question(question):

    question_embedding = vectorizer.transform(
        [question]
    ).toarray().astype("float32")

    k = min(2, len(chunks))

    distances, indices = index.search(
        question_embedding,
        k
    )

    results = []

    for i in indices[0]:
        if i >= 0:
            results.append(chunks[i])

    return results