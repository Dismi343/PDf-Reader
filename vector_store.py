
import chromadb
from typing import List, Dict
from embedding import embed_texts


chroma_client = chromadb.PersistentClient(path="./chroma_db")

COLLECTION_NAME = "pdf_semantic_search"

def get_collection():
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # optional, for cosine similarity
    )

def index_chunks(chunks: List[Dict]):
    """
    Add chunks to Chroma collection.
    """
    collection = get_collection()

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"page_num": c["page_num"], "source": c["source"]} for c in chunks]

    embeddings = embed_texts(texts)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )
  
