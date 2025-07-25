import os
from llama_index.core import (
    VectorStoreIndex,         # Hovedindeks for lagring og søk
    StorageContext,           # Håndtering av indekseringens lagringskontekst
    load_index_from_storage,  # Laste indeksen fra disk
    SimpleDirectoryReader     # Leser PDF-er fra en mappe
)
from llama_index.llms.ollama import Ollama  # Lokal språkmodell via Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # Embeddings fra HuggingFace

# 📁 Konfigurerte mappeplasseringer
PDF_FOLDER = "pdf_folder"       # Mappe der bruker legger inn PDF-er
INDEX_DIR = "index_storage"     # Mappe hvor indeksen lagres

# 🔧 Initialiser modeller én gang ved oppstart
# Liten, rask embedding-modell for tekstlikhet
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
# Lokal språkmodell, f.eks. Dolphin Mistral via Ollama
llm = Ollama(model="dolphin-mistral")


def ensure_pdf_folder():
    """
    Sørg for at 'pdf_folder' finnes.
    Returnerer en liste over PDF-filer i mappen.
    Hvis ingen PDF-er finnes, returneres tom liste.
    """
    os.makedirs(PDF_FOLDER, exist_ok=True)  # Opprett mappe hvis den mangler
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]  # Filtrer kun PDF-er
    return pdf_files


def load_or_build_index(pdf_files):
    """
    Håndterer lastingen eller byggingen av indeksen:
    - Hvis indeksmappe finnes, last indeks fra disk.
    - Hvis det finnes PDF-er, bygg ny indeks og lagre den.
    - Hvis ingen PDF-er finnes, start uten indeks.
    
    Returnerer: Index eller None (hvis ingen PDF-er og ingen indeks finnes).
    """
    if os.path.exists(INDEX_DIR):
        print("🔄 Laster indeksen fra disk ...")
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)  # Bruk lagret kontekst
        index = load_index_from_storage(storage_context, embed_model=embed_model)
        return index

    elif pdf_files:
        print(f"📄 Fant {len(pdf_files)} PDF-fil(er), bygger indeks ...")
        documents = SimpleDirectoryReader(PDF_FOLDER).load_data()  # Last inn alle PDF-er
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)  # Bygg indeks
        index.storage_context.persist(persist_dir=INDEX_DIR)  # Lagre til disk
        print("✅ Indeks bygget og lagret.")
        return index

    else:
        # Ingen PDF-er og ingen indeks: ingen kontekst
        print(f"[INFO] Ingen PDF-er funnet i '{PDF_FOLDER}'. Starter uten kontekst.")
        return None


def get_query_engine(index):
    """
    Hvis det finnes en indeks, returner en spørringsmotor (query_engine)
    som bruker modellen og støtter streaming av svar.
    
    Returnerer: query_engine eller None.
    """
    if index:
        return index.as_query_engine(llm=llm, streaming=True)
    return None