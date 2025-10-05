from datetime import datetime
import os, re, json, psycopg2
from pypdf import PdfReader
from docx import Document
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GIMINI_API_KEY")
postgres_url = os.getenv("POSTGRES_URL")

client = genai.Client(api_key=api_key)

def extract_pdf_text(file_path):
    texts = []
    for p in PdfReader(file_path).pages:
        txt = p.extract_text() # pypdf function
        if txt is None:
            return ""
        texts.append(txt)
    return "\n".join(texts)


def extract_docx_text(file_path):
    texts = []
    for p in Document(file_path).paragraphs:
        txt = p.text # docx function
        if txt is None:
            return ""
        texts.append(txt)
    return "\n".join(texts)


def extract_text(file_path):
    path = file_path.lower()
    if path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    elif path.endswith(".docx"):
        return extract_docx_text(file_path)
    else:
        return ""


def split_fixed(text, size = 500, overlap = 100):
    results = []
    i = 0
    while i < len(text):
        p = text[i:i+size]
        p = p.strip()
        if p:
            results.append(p)
        i += size - overlap
    return results


def split_sentence(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    results = []
    for p in parts:
        p = p.strip()
        if p:
            results.append(p)
    return results


def split_paragraph(text):
    parts = re.split(r'\n\s*\n+', text)
    results = []
    for p in parts:
        p = p.strip()
        if p:
            results.append(p)
    return results


def embed(text):
    r = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    
    if hasattr(r, "embedding"):           # single input
        return r.embedding.values         
    else:                                 
        return r.embeddings[0].values     # list of inputs


def insert_rows(rows):
    conn = psycopg2.connect(postgres_url)
    cur  = conn.cursor()
    cur.executemany(
        """
        INSERT INTO documents (chunk_text, embedding, filename, split_strategy, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        rows,
    )
    conn.commit()
    cur.close()
    conn.close()


def index_file(file_path, mode):
    text = extract_text(file_path)
    if mode == "fixed":
        chunk = split_fixed(text)
    elif mode == "sentence":
        chunk = split_sentence(text)
    elif mode == "paragraph":
        chunk = split_paragraph(text)

    rows = []
    time = datetime.now()
    for c in chunk:
        embedded_vector = embed(c)
        rows.append((
            c,
            json.dumps(embedded_vector),
            os.path.basename(file_path),
            mode,
            time
        ))
    insert_rows(rows)


if __name__ == "__main__":
    index_file("lorem.docx", "fixed")
    # index_file("lorem.docx", "sentence")
    # index_file("lorem.docx",  "paragraph")