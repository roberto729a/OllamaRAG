import streamlit as st
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from bs4 import BeautifulSoup
from config import (
    APP_TITLE, APP_ICON, ASSISTANT_NAME, 
    ASSISTANT_INTRO, INPUT_PLACEHOLDER, VECTOR_STORE_PATH, 
    EMBEDDING_MODEL, LLM_MODEL
)

# --- Page Configuration ---
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

# --- CSS for styling ---
st.markdown("""
    <style>
        .st-emotion-cache-1c7y2kd, .st-emotion-cache-4oy321 {
            border-radius: 10px;
        }
        header, footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text(separator='\n', strip=True)

def format_chat_history(messages):
    history = []
    for msg in messages[-4:]: 
        role = "Human" if msg["role"] == "user" else "Assistant"
        history.append(f"{role}: {msg['content']}")
    return "\n".join(history)

@st.cache_resource
def load_resources():
    print("Loading resources...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_store = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
    
    retriever = vector_store.as_retriever(search_kwargs={'k': 10})
    llm = ChatOllama(model=LLM_MODEL)
    
    print("Resources loaded successfully.")
    return retriever, llm

# --- Prompt Template ---
PROMPT_TEMPLATE = f"""
You are {ASSISTANT_NAME}, a helpful AI assistant. Your persona is direct, knowledgeable, and professional.
You are an expert on the information contained in the context documents provided.

Use the following conversation history to understand the context of the new question.
Your primary task is to answer the user's new question directly using ONLY the information from the provided context documents.

- Do NOT mention the context in your response. Answer straightforwardly as an expert.
- If the context does not contain the information needed to answer the question, you MUST reply with the single sentence: "I do not have enough information to answer that question."

Conversation History:
{{chat_history}}

Context Documents:
{{context}}

New Question:
{{question}}
"""
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# --- UI ---
st.title(APP_TITLE)

try:
    retriever, llm = load_resources()
except Exception as e:
    st.error("Failed to load the knowledge base. Please ensure 'chroma_db' exists. You may need to run ingest.py again.")
    st.stop()

generation_chain = (
    prompt
    | llm
    | StrOutputParser()
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": ASSISTANT_INTRO}]
if "processing" not in st.session_state:
    st.session_state.processing = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.processing:
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            try:
                user_question = st.session_state.messages[-1]['content']
                chat_history = format_chat_history(st.session_state.messages[:-1])
                
                retrieved_docs = retriever.invoke(user_question)
                
                raw_response = generation_chain.invoke({
                    "context": retrieved_docs,
                    "question": user_question,
                    "chat_history": chat_history
                })
                
                clean_response = clean_html(raw_response)
                
                st.markdown(clean_response)
                st.session_state.messages.append({"role": "assistant", "content": clean_response})
            except Exception as e:
                error_message = "Sorry, I encountered an error. Please try your question again."
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                print(f"Error during RAG chain invocation: {e}")
            
            st.session_state.processing = False
            st.rerun()

if user_question := st.chat_input(INPUT_PLACEHOLDER, disabled=st.session_state.processing):
    st.session_state.messages.append({"role": "user", "content": user_question})
    st.session_state.processing = True
    st.rerun()

