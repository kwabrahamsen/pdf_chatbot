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

# 📁 Indeks-lagring
INDEX_DIR = "index_storage"

# 🔧 Modelloppsett
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Ollama(model="dolphin-mistral")

# 🧠 Last eller bygg indeks
if os.path.exists(INDEX_DIR):
    print("🔄 Laster indeksen fra disk ...")
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
    index = load_index_from_storage(storage_context, embed_model=embed_model)
else:
    print("📄 Leser PDF-er og bygger indeks ...")
    documents = SimpleDirectoryReader("pdf_folder").load_data()
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    index.storage_context.persist(persist_dir=INDEX_DIR)
    print("✅ Indeks lagret.")

# 🎯 Spørringsmotor med streaming aktivert
query_engine = index.as_query_engine(llm=llm, streaming=True)

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    def generate():
        try:
            response = query_engine.query(query)
            for token in response.response_gen:
                yield token  # Du kan også: yield f"data: {token}\n\n"
        except Exception as e:
            yield f"[FEIL]: {str(e)}"

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)