# 📚 PDF Chatbot med LlamaIndex, Flask og Ollama

Dette prosjektet er en enkel webbasert chatbot som lar deg stille spørsmål til innholdet i dine egne PDF-filer. Den bruker `LlamaIndex` til å indeksere dokumenter, `Ollama` som LLM-backend, og `Flask` som webserver.

## 🚀 Funksjoner

- Last inn og indekser egne PDF-filer
- Still spørsmål i et enkelt webgrensesnitt
- Få svar generert av en språkmodell (f.eks. Dolphin-Mistral via Ollama)
- Sanntids-strømming av svaret til siden

## 🧱 Teknologier

- **Python 3.10+**
- **Flask** – enkel backend og API
- **LlamaIndex** – for dokumentindeksering og spørringer
- **Ollama** – lokal kjøring av LLM (eks. dolphin-mistral)
- **HuggingFace Embeddings** – for tekstvektorer
- **HTML/JS** – frontend med støtte for sanntidsstrømming

## 🗂️ Prosjektstruktur

```text
pdf-chatbot/
├── app.py                 # Flask-app med API-endepunkt
├── pdf_folder/            # Legg dine PDF-filer her
├── index_storage/         # Lagret vektorindeks (auto-generert)
├── templates/
│   └── index.html         # Webgrensesnitt
├── pyproject.toml         # Administrert av Poetry
└── README.md
```

## ⚙️ Kom i gang

### 1. Installer avhengigheter med Poetry

```bash
poetry install
```

### 2. Legg til PDF-filer

Plasser én eller flere PDF-filer i `pdf_folder/`.

### 3. Kjør appen

```bash
poetry run python app.py
```

Besøk http://localhost:5000 i nettleseren for å chatte med PDF-ene dine.

## 🔁 Gjenoppbygging av indeks

Hvis du oppdaterer innholdet i pdf_folder/, slett mappen index_storage/ for å bygge indeksen på nytt neste gang appen startes.
