# PDF Chatbot med LlamaIndex, Flask og Ollama

Dette prosjektet er en enkel webbasert chatbot som lar deg stille spørsmål til innholdet i dine egne PDF-filer. Den bruker `LlamaIndex` til å indeksere dokumenter, `Ollama` som LLM-backend, og `Flask` som webserver.

## Funksjoner

- Last inn og indekser egne PDF-filer
- Still spørsmål i et enkelt webgrensesnitt
- Få svar generert av en språkmodell (Dolphin-Mistral via Ollama)
- Sanntids-strømming av svaret til siden

## Teknologier

- **Python 3.10+**
- **Flask** – enkel backend og API
- **LlamaIndex** – for dokumentindeksering og spørringer
- **Ollama** – lokal kjøring av LLM (dolphin-mistral)
- **HuggingFace Embeddings** – for tekstvektorer
- **HTML/JS** – frontend med støtte for sanntidsstrømming

## Prosjektstruktur

```text
pdf-chatbot/
├── LICENSE
├── README.md
├── pyproject.toml         # Poetry konfigurasjon
├── poetry.lock            # Låst avhengigheter for poetry
├── .gitignore
└── src/
    └── pdf_chatbot/
        ├── __init__.py
        ├── app.py
        ├── templates/
        │   └── index.html
        └── static/
            └── styles.css
        ├── pdf_folder/          # PDF-dokumenter for indeksering (opprettes automatisk ved behov)
        └── index_storage/      # Lagringsmappe for søkeindeksen (genereres automatisk)
```

## Kom i gang

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

## Gjenoppbygging av indeks

Hvis du oppdaterer innholdet i pdf_folder/, slett mappen index_storage/ for å bygge indeksen på nytt neste gang appen startes.
