import json
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from config import VECTOR_STORE_PATH, SCRAPED_DATA_PATH, EMBEDDING_MODEL

def ingest_data():
    print("--- Starting data ingestion with metadata ---")

    try:
        with open(SCRAPED_DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {SCRAPED_DATA_PATH} not found. Run scraper.py first.")
        return

    documents = []
    for item in data:
        metadata = {
            "source": item['url'],
            "title": item['title'] 
        }
        documents.append(Document(page_content=item['content'], metadata=metadata))
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"Split content into {len(docs)} metadata-rich chunks.")

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    print("Creating embeddings...")

    db = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=VECTOR_STORE_PATH
    )
    print(f"Successfully created enhanced vector store at {VECTOR_STORE_PATH}")

if __name__ == '__main__':
    ingest_data()

