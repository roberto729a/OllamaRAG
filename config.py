# ----------------------------------------------------------------------------
# CONFIGURATION FOR THE WEBSITE RAG AI ASSISTANT FRAMEWORK
# ----------------------------------------------------------------------------
# This is the only file you need to edit to create a new AI assistant.
# ----------------------------------------------------------------------------

# 1. SCRAPER & DATA CONFIGURATION
#    The URL of the website you want the AI to learn from.
#    It will start crawling from this page.
#    Examples: "https://en.wikipedia.org/", "https://www.geeksforgeeks.org/"
START_URL = "https://en.wikipedia.org/"

# The local file path where the scraped website content will be saved.
SCRAPED_DATA_PATH = "scraped_content.json"

# 2. VECTOR DATABASE CONFIGURATION
#    The local directory where the vector database (ChromaDB) will be stored.
VECTOR_STORE_PATH = "./chroma_db"

# 3. AI MODEL CONFIGURATION
#    The embedding model to use for converting text into vectors.
#    'nomic-embed-text' is a great lightweight default.
EMBEDDING_MODEL = "nomic-embed-text"

#    The main language model for generating answers.
#    'phi3' is recommended for its balance of speed and reliability for general tasks.
#    Other fast options: 'gemma:2b', 'mistral'
LLM_MODEL = "phi3"

# 4. CHATBOT UI & PERSONA CONFIGURATION
#    The title that will appear in the browser tab and at the top of the app.
APP_TITLE = "Scrat - A RAG AI Assistant"

#    The icon for the browser tab.
APP_ICON = "🤖"

#    The name of the topic, company, or organization the bot represents.
#    Example: "Wikipedia", "GeeksForGeeks"
SUBJECT_NAME = "Wikipedia"

#    The name of your AI assistant.
ASSISTANT_NAME = "Scrat"

#    The introductory message the AI will greet the user with.
ASSISTANT_INTRO = f"Hello! I'm {ASSISTANT_NAME}. I can answer questions based on information from {SUBJECT_NAME}. How can I help you today?"

#    The placeholder text in the user input box.
INPUT_PLACEHOLDER = "Ask your question here..."

