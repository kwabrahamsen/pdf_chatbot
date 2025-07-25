import os
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    SimpleDirectoryReader
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

PDF_FOLDER = "pdf_folder"
INDEX_DIR = "index_storage"

# Opprett mappe om den ikke finnes
os.makedirs(PDF_FOLDER, exist_ok=True)

# Finn PDF-er
pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]

# Modelloppsett
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Ollama(model="dolphin-mistral")

# Indeksbygging eller lasting
if os.path.exists(INDEX_DIR):
    print("🔄 Laster indeksen fra disk ...")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
    index = load_index_from_storage(storage_context, embed_model=embed_model)
elif pdf_files:
    print(f"📄 Fant {len(pdf_files)} PDF-fil(er), bygger indeks ...")
    documents = SimpleDirectoryReader(PDF_FOLDER).load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    index.storage_context.persist(persist_dir=INDEX_DIR)
    print("✅ Indeks bygget og lagret.")
else:
    print(f"[INFO] Ingen PDF-er funnet i '{PDF_FOLDER}'. Starter uten kontekst.")
    index = None

# Spørringsmotor
if index:
    query_engine = index.as_query_engine(llm=llm, streaming=True)

# CLI Loop
print("📢 CLI Chatbot klar. Skriv 'exit' for å avslutte.")

while True:
    user_input = input("Du: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Avslutter.")
        break
    if not user_input:
        continue

    if index:
        try:
            response = query_engine.query(user_input)
            print("Bot: ", end="", flush=True)
            for token in response.response_gen:
                print(token, end="", flush=True)
            print()
        except Exception as e:
            print(f"[FEIL]: {str(e)}")
    else:
        print(f"[INFO] Du spurte: '{user_input}', men ingen PDF-kontekst er tilgjengelig.")