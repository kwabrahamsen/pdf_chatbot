import os
from llama_index.core import (
    VectorStoreIndex,         # Builds and queries vector index
    StorageContext,           # Manages index persistence
    load_index_from_storage,  # Loads existing index from disk
    SimpleDirectoryReader     # Reads documents (PDFs) from folder
)
from llama_index.llms.ollama import Ollama  # Local LLM via Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # Embeddings via HuggingFace

# 📁 Folder configuration
PDF_FOLDER = "pdf_folder"       # User uploads PDFs here
INDEX_DIR = "index_storage"     # Index is stored here

# 🔧 Load models once at startup
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")  # Lightweight embedding model

# Set up local language model with strict Markdown formatting rules
llm = Ollama(
    model="dolphin-mistral",
    system_prompt=(
        "You must respond using Markdown formatting. "
        "Whenever you include code, use triple backticks with the correct language tag. "
        "Example: ```python ... ``` for Python code. "
        "Never respond with code outside of proper code blocks. "
        "Be concise, clear, and always make your responses easy to read."
    )
)


def ensure_pdf_folder():
    """
    Ensure that 'pdf_folder' exists.
    Returns a list of PDF files found in the folder.
    """
    os.makedirs(PDF_FOLDER, exist_ok=True)
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]
    return pdf_files


def load_or_build_index(pdf_files):
    """
    Load the index from disk if available, or build it from PDFs if present.
    
    Returns:
        - A valid index if found or created.
        - None if no PDFs exist and no index is stored.
    """
    if os.path.exists(INDEX_DIR):
        print("🔄 Loading index from disk ...")
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context, embed_model=embed_model)
        return index

    elif pdf_files:
        print(f"📄 Found {len(pdf_files)} PDF file(s), building index ...")
        documents = SimpleDirectoryReader(PDF_FOLDER).load_data()
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
        index.storage_context.persist(persist_dir=INDEX_DIR)
        print("✅ Index built and saved.")
        return index

    else:
        print(f"[INFO] No PDFs found in '{PDF_FOLDER}'. Starting without context.")
        return None


def get_query_engine(index):
    """
    If index is available, return a query engine that streams responses.
    """
    if index:
        return index.as_query_engine(llm=llm, streaming=True)
    return None