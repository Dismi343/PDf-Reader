# 📄 PDF RAG – Ask Questions from Your PDFs with AI

This project is a **PDF Question-Answering system** built with a **FastAPI backend** and a **web frontend**.  
You can upload a PDF, ask a question, and the AI will answer **based only on the content of that PDF** using **RAG (Retrieval-Augmented Generation)**.

---

## 🚀 Features

- 📝 **PDF Upload from Frontend** – Upload any PDF through a web UI.
- 🧩 **Text Extraction & Chunking** – Extracts text from pages and splits it into semantic chunks.
- 🔢 **Vector Embeddings** – Uses a SentenceTransformer model (`all-MiniLM-L6-v2`) to generate embeddings.
- 📦 **Vector Store** – Stores chunks + embeddings in a vector database (ChromaDB / MongoDB).
- 🤖 **AI-Powered Answers** – Uses an LLM (via API like OpenRouter / HuggingFace / OpenAI) to answer questions using retrieved context.
- 🔍 **Semantic Search** – Finds the most relevant PDF chunks to the user’s question.
- 🗑️ **PDF Deletion (Optional)** – Endpoint to delete chunks related to a specific PDF.

---

## 🧱 Tech Stack

**Frontend**
- React / Next.js (TypeScript)
- Axios for API calls
- File upload via `FormData`
- UI icons with `lucide-react` (optional)

**Backend**
- FastAPI (Python)
- Uvicorn ASGI server
- Running in a **Conda environment**

**AI & Retrieval**
- `sentence-transformers` – `all-MiniLM-L6-v2` for embeddings
- ChromaDB (local or cloud) as vector database  
  > Optionally, MongoDB can be used to store embedded chunks.
- LLM provider (one of):
  - OpenRouter API
  - HuggingFace Router
  - OpenAI API (if available)

**PDF & Utilities**
- PyPDF2 / similar library for PDF text extraction
- Pydantic for models & settings
- `python-dotenv` or environment variables for secrets

---

## 🐍 Environment Setup (Conda)

```bash
# Create and activate environment
conda create -n pdf-rag python=3.12
conda activate pdf-rag
