from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

VECTOR_STORE_PATH = "./chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"

def verify_knowledge_base():
    print("--- Starting Knowledge Base Verification ---")
    
    try:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        vector_store = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
        print(f"Successfully loaded vector store from '{VECTOR_STORE_PATH}'")
    except Exception as e:
        print(f"\nERROR: Could not load the vector store. Did you run ingest.py?")
        print(f"Details: {e}")
        return

    test_query = "What is Amadis Global?"
    print(f"\nPerforming test search with query: '{test_query}'")
    
    try:
        results = vector_store.similarity_search(test_query, k=3)
        
        if not results:
            print("\n!!! VERIFICATION FAILED !!!")
            print("The search returned NO results. The knowledge base is likely empty or corrupt.")
            print("Please delete the 'chroma_db' directory and run 'ingest.py' again.")
        else:
            print("\n*** VERIFICATION SUCCESSFUL ***")
            print("The search returned the following relevant chunks from the database:")
            for i, doc in enumerate(results):
                print(f"\n--- Result {i+1} ---")
                print(f"Source: {doc.metadata.get('source', 'N/A')}")
                print(f"Content: {doc.page_content[:500]}...")
    
    except Exception as e:
        print(f"\nERROR: An error occurred during the similarity search.")
        print(f"Details: {e}")

if __name__ == '__main__':
    verify_knowledge_base()