# README

## Installation

### Python libraries

Install all required libraries in one command:

python3 -m pip install pypdf python-docx psycopg2-binary python-dotenv google-genai

### PostgreSQL

Install and start PostgreSQL (macOS with Homebrew):

brew install postgresql
brew services start postgresql
psql --version  

By default PostgreSQL creates a database with the same name as your macOS username.
You can list databases and owners with:

psql
\l

## Environment Setup

Create a file named .env in the project root.

### PostgreSQL connection
POSTGRES_URL=postgresql://<YOUR_USERNAME>@localhost:5432/<YOUR_DB_NAME>

- Replace <YOUR_USERNAME> with your macOS user (or any Postgres user you created).
- Replace <YOUR_DB_NAME> with your database name.

To see existing DBs and owners:

psql
\l

If you want a custom user, password, or port — follow the Postgres docs.

### Gemini API key
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>

so your .env file should look like this:
POSTGRES_URL=postgresql://{" Enter Your Username Here "}@localhost:5432/{ " Enter Your Database Name Here "}
GIMINI_API_KEY={" Enter Your Gemini Api Key Here "}

- Get a key: https://ai.google.dev/gemini-api/docs/api-key
- Learn about embeddings: https://ai.google.dev/gemini-api/docs/embeddings

## Database Setup

Run the script to create the documents table (must be done once):

python3 create_db.py

This creates the table and required fields.
If you skip this step, the other scripts won't work because there's no table to store data.

To check that the table exists:

psql
\dt

## Indexing Documents

Put your PDF/DOCX files in the same folder as the scripts.

Edit index_documents.py (in the __main__ section):

- Set the file name you want to index.
- Choose the split mode: fixed, sentence, or paragraph.
- (For fixed, you can adjust chunk size and overlap inside split_fixed() function)

Run:

python3 index_documents.py

To verify data was inserted:

psql
SELECT * FROM documents LIMIT 5;

## Searching Documents

Edit search_documents.py (in the __main__ section):

- Set the query you want to search for.
- Set top_k for number of results.

Run:

python3 search_documents.py

The script prints the top-K results directly in the terminal.