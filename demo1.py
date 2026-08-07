import fitz
import faiss
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------
# LOAD PDF
# -----------------------------

pdf = fitz.open("demoschool.pdf")

all_text = ""

for page in pdf:
    all_text += page.get_text() + "\n\n"


# -----------------------------
# CREATE CHUNKS
# -----------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_text(all_text)


# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# CREATE EMBEDDINGS
# -----------------------------

embeddings = model.encode(chunks).astype("float32")

print("Embeddings Shape:", embeddings.shape)
print("Number of Chunks:", len(chunks))


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

    question_embedding = model.encode(
        [question]
    ).astype("float32")

    k = 2

    distances, indices = index.search(
        question_embedding,
        k
    )

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results