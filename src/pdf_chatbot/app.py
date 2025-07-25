from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from pdf_chatbot.core import ensure_pdf_folder, load_or_build_index, get_query_engine

app = Flask(__name__)

pdf_files = ensure_pdf_folder()
index = load_or_build_index(pdf_files)
query_engine = get_query_engine(index)

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
            if query_engine:
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