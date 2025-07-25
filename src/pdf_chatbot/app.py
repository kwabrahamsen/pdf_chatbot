import os
from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    SimpleDirectoryReader
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

app = Flask(__name__)

# 📁 Mappestier
PDF_FOLDER = "pdf_folder"
INDEX_DIR = "index_storage"

# ✅ Opprett pdf_folder hvis den ikke finnes
os.makedirs(PDF_FOLDER, exist_ok=True)

# 🔍 Finn PDF-filer
pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]

# 🔧 Modelloppsett
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Ollama(model="dolphin-mistral")

# 🧠 Indekshåndtering
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
    print(f"[INFO] Ingen PDF-er funnet i '{PDF_FOLDER}'. Starter app uten kontekst.")
    index = None  # Ingen indeks foreløpig

# 🎯 Spørringsmotor (kun hvis indeks finnes)
if index:
    query_engine = index.as_query_engine(llm=llm, streaming=True)

@app.route("/")
def index_page():
    return render_template("index.html", pdf_files=pdf_files)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    def generate():
        try:
            if index:
                response = query_engine.query(query)
                for token in response.response_gen:
                    yield token
            else:
                yield f"[INFO] Du spurte: '{query}', men ingen PDF-kontekst er tilgjengelig."
        except Exception as e:
            yield f"[FEIL]: {str(e)}"

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)