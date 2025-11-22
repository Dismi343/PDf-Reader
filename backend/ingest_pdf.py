from pdf_utils import extract_pdf_pages
from chunks_utils import chunk_text
#from vector_store_chroma import index_chunks    #when uploading to cloud db (chromadb)
#from vector_store import index_chunks              #local chromadb
from Mongo_db.vector_store_mongo import index_chunks   #mongo db

def ingest_pdf(pdf_path: str):
    """
    Extract text from PDF, chunk it, and index into vector store.
    """
    pages = extract_pdf_pages(pdf_path)
    if not pages:
        raise ValueError(f"No text extracted from: {pdf_path}")
        

    chunks = chunk_text(pages)
    if not chunks:
        print(f"No chunks created from: {pdf_path}")
        return

    index_chunks(chunks)
    print(f"Ingested {len(chunks)} chunks from {pdf_path}")

# Optional: run directly for testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ingest_pdf.py path/to/file.pdf")
    else:
        ingest_pdf(sys.argv[1])
