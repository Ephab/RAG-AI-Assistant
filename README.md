# RAG AI Assistant

A **Retrieval-Augmented Generation (RAG)** system that allows you to chat with your PDF documents using local AI. Ask questions about your PDFs and get intelligent, context-aware answers powered by Ollama and semantic search.

## Features

-  **Semantic Search**: Uses vector embeddings to find relevant content in your PDFs
-  **Interactive Chat**: Ask questions in natural language and get LLM powered responses
-  **100% Local**: Runs entirely on your machine using Ollama, no API keys or cloud services needed
-  **PDF Processing**: Automatically converts PDFs to markdown and chunks them
-  **Persistent Storage**: Uses ChromaDB to store embeddings for quick retrieval
-  **Dual Mode**: Chat with PDFs or use as a general AI assistant

##  Tech Stack

- **Ollama** - Local LLM inference (llama3.2 3b)
- **ChromaDB** - Vector database for embeddings
- **Sentence Transformers** - Embedding generation (`all-MiniLM-L6-v2`)
- **PyMuPDF4LLM** - PDF parsing and markdown conversion
- **TikToken** - Token counting for OpenAI-compatible models

## Prerequisites

Before running this project, you need to have:

1. **Python 3.8 or higher** installed
2. **Ollama** installed and running locally 
   - Download from [ollama.ai](https://ollama.ai)
   - Pull the llama3.2 model: `ollama pull llama3.2`
   - Ensure Ollama is running: `ollama serve` (MUST BE RUNNING IN THE BACKGROUND)

## Installation

1. **Clone the repository**


2. **Create a virtual environment**


3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make sure Ollama is running**
   ```bash
   ollama serve
   ```

## Usage

Run the assistant:

```bash
python main.py
```

### Workflow

1. **Choose Mode**:
   - Enter `y` to use PDF context mode
   - Enter `n` for general chat mode

2. **Select PDFs** (if using PDF mode):
   - A file dialog will open
   - Select one or more PDF files
   - PDFs will be processed and indexed automatically

3. **Ask Questions**:
   - Type your questions naturally
   - Get AI-powered answers based on your documents
   - Type `quit`, `exit`, or `q` to stop


## Project Structure

```
rag-pdf-assistant/
├── main.py              # Entry point and user interface
├── parse_pdf.py         # PDF to markdown conversion
├── chunking.py          # Text chunking
├── vector_store.py      # ChromaDB vector store management
├── retrieval.py         # Semantic search and context retrieval
├── llm_interface.py     # Ollama API integration
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── LICENSE             # GPL License
└── README.md           # This file

# Generated directories
├── pdfs/               # Uploaded PDF files
├── md_files/           # Converted markdown files
└── chroma_db/          # Vector database storage
```

## Configuration

### Chunk Size and Overlap

Modify chunking parameters in `main.py`:
```python
chunks = chunk_md_file(md_file, chunk_size=500, overlap=50)
```

### Number of Retrieved Chunks

Adjust `top_k` parameter in `main.py`:
```python
context = retriever.retrieve_and_format(query, top_k=3)
```

### LLM Model

Change the Ollama model in `llm_interface.py`:
```python
"model": "llama3.2"
```

### Embedding Model

Change the embedding model in `vector_store.py`:
```python
self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
```


## How It Works

1. **PDF Processing**: PDFs are converted to markdown using PyMuPDF4LLM
2. **Chunking**: Text is split into overlapping chunks (500 tokens each) for better context
3. **Embedding**: Each chunk is converted to a vector using Sentence Transformers
4. **Storage**: Vectors are stored in ChromaDB for similarity search
5. **Retrieval**: User queries are embedded and matched against stored chunks
6. **Generation**: Retrieved context is sent to the Ollama LLM to generate answers

## Troubleshooting

**Ollama connection error**:
- Ensure Ollama is running: `ollama serve`
- Check that the model is installed: `ollama pull llama3.2`
- Verify Ollama is listening on `localhost:11434`

## Verification
Run `python verify_setup.py` to verify all dependencies