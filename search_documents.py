import os, json, psycopg2
from google import genai
from dotenv import load_dotenv

load_dotenv()
GIMINI_API_KEY = os.getenv("GIMINI_API_KEY")
POSTGRES_URL   = os.getenv("POSTGRES_URL")

client = genai.Client(api_key=GIMINI_API_KEY)

def embed(text):
    r = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    
    if hasattr(r, "embedding"):           # single input
        return r.embedding.values         
    else:                                 
        return r.embeddings[0].values     # list of inputs


def search(query, top_k):
    q_vec = embed(query)

    conn = psycopg2.connect(POSTGRES_URL)
    cur = conn.cursor()
    cur.execute("SELECT chunk_text, embedding FROM documents")
    rows = cur.fetchall() # return a list of tuples
    conn.close()

    scored = []
    for txt, emb in rows:

        if isinstance(emb, str):
            vec = json.loads(emb)
        else:
            vec = emb

        score = 0
        for x, y in zip(q_vec, vec):
            score += x * y

        scored.append((score, txt))

    scored.sort(reverse=True, key=lambda x: x[0])
    result = []
    for pair in scored[:top_k]:
        result.append(pair[1])
    return result


if __name__ == "__main__":
    top_k = 5
    result = search("exmaple text",top_k) 
    for r in result:
        print("-",r)

