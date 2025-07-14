import os
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 📁 Hvor vi lagrer eller henter den eksisterende vektorindeksen
INDEX_DIR = "index_storage"

# 🧠 Sett opp embeddings-modellen
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 🤖 Sett opp språkmodellen med støtte for streaming
llm = Ollama(model="dolphin-mistral")

# 📦 Last indeksen hvis den finnes, ellers bygg den fra PDF-er
if os.path.exists(INDEX_DIR):
    print("🔄 Laster eksisterende indeks ...")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
    index = load_index_from_storage(storage_context, embed_model=embed_model)
else:
    print("📄 Leser PDF-er og lager ny indeks ...")
    documents = SimpleDirectoryReader("pdf_folder").load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    index.storage_context.persist(persist_dir=INDEX_DIR)
    print("✅ Indeks lagret.")

# 🔍 Gjør klar en query engine med streaming aktivert
query_engine = index.as_query_engine(llm=llm, streaming=True)

# 💬 Interaktiv kommandolinje
print("\n🧠 Klar! Skriv inn spørsmål. Skriv 'exit' for å avslutte.\n")

while True:
    try:
        query = input("❓ Spørsmål: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("👋 Avslutter...")
            break
        if not query:
            continue

        print("\n💬 Svar:\n")
        response_stream = query_engine.query(query)

        # 📡 Stream token-for-token
        for token in response_stream.response_gen:
            print(token, end="", flush=True)
        print("\n")

    except KeyboardInterrupt:
        print("\n👋 Avslutter...")
        break
    except Exception as e:
        print(f"\n⚠️ Feil: {e}\n")