# Website RAG AI Assistant Framework

This project provides a complete, general-purpose framework for creating a conversational AI assistant that learns from any website. It uses a RAG (Retrieval-Augmented Generation) pipeline with local AI models powered by Ollama.

## How It Works

The project is broken down into three main stages:

1.  **Crawl (`scraper.py`):** An automated script starts at a specified URL and crawls through the website, extracting all the clean, textual content from each page.

2.  **Ingest (`ingest.py`):** The scraped text is broken down into smaller chunks, converted into numerical vector embeddings, and stored in a local vector database (`ChromaDB`). This database acts as the AI's "brain."

3.  **Chat (`app.py`):** A Streamlit web application provides a user-friendly chat interface. When a user asks a question, the app retrieves the most relevant information from the database and uses an AI language model to generate a context-aware answer.

## How to Use

### Step 1: Prerequisites

* **Ollama**: Make sure Ollama is installed and running. You can get it from <https://ollama.com/>.

* **AI Models**: Pull the necessary models by running the following commands in your terminal:
    ```bash
    ollama pull nomic-embed-text
    ollama pull phi3
    ```

* **Python**: Ensure you have Python 3.9 or newer.

### Step 2: Setup

1.  **Clone the Repository**: Get the project files onto your local machine.

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Configure Your Assistant

Open the `config.py` file. This is the only file you need to edit.

* Set the `START_URL` to the homepage of the website you want the bot to learn from.

* Customize the `APP_TITLE`, `SUBJECT_NAME`, `ASSISTANT_NAME`, etc., to define your bot's identity.

### Step 4: Build the Knowledge Base

Run the data processing scripts in order. **This only needs to be done once** for each new website.

1.  **Run the Scraper**: This will crawl the website defined in your config and create `scraped_content.json`.
    ```bash
    python scraper.py
    ```

2.  **Run the Ingestion Script**: This will process the JSON file and create the `chroma_db` vector store.
    ```bash
    python ingest.py
    ```

### Step 5: Launch the Chatbot

Now you can start the web application.
```bash
streamlit run app.py
```
