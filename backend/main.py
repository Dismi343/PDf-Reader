from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from vector_store import get_chroma_collection

from ingest_pdf import ingest_pdf
from rag import answer_query

app = FastAPI(
    title="PDF Semantic Search (Free Stack)",
    description="Upload PDFs and ask questions using local embeddings + Ollama.",
    version="1.0.0",
)

# CORS (adjust origins for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF, save it, and ingest it into the vector DB.
    """
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ingest into vector store
    ingest_pdf(str(file_path))

    return {"status": "ok", "filename": file.filename}

@app.post("/ask")
async def ask(payload: dict):
    """
    Ask a question over the indexed PDFs.
    Body: { "query": "your question" }
    """
    query = payload.get("query")
    if not query:
        return {"error": "query is required"}

    answer = answer_query(query)
    return {"answer": answer}


@app.get("/")
async def root():
    return {"message": "PDF RAG backend up. Use /upload-pdf and /ask."}
