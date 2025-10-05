import psycopg2, os
from dotenv import load_dotenv

load_dotenv()
postgres_url = os.getenv("POSTGRES_URL")

conn = psycopg2.connect(postgres_url)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    chunk_text TEXT,
    embedding  JSON,
    filename TEXT,
    split_strategy TEXT,
    created_at TIMESTAMP
)
""")
conn.commit()
cur.close()
conn.close()