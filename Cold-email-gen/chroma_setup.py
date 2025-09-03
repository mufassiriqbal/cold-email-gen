# chroma_setup.py
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
import os

CHROMA_PATH = "./chroma_db"
PDF_PATH = "Mufassir iqbal.pdf"  # place your resume here

# Initialize Chroma persistent client
client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_func = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="portfolio",
    embedding_function=embedding_func
)

# Read PDF
reader = PdfReader(PDF_PATH)
resume_text = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        resume_text += text + "\n"

# Split text into chunks for better retrieval
def split_text(text, chunk_size=150):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i+chunk_size])

chunks = list(split_text(resume_text, chunk_size=150))

# Upsert to chroma
for i, chunk in enumerate(chunks):
    collection.upsert(
        documents=[chunk],
        ids=[f"resume_{i}"]
    )

print(f"Inserted {len(chunks)} resume chunks into ChromaDB at {CHROMA_PATH}")
