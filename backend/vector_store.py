# vector_store.py

import chromadb
from typing import List, Dict
from embedding import embed_texts

COLLECTION_NAME = "pdf_semantic_search"

def get_chroma_client() -> chromadb.Client:
    return chromadb.PersistentClient(path="./chroma_db")


def get_chroma_collection():
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def index_chunks(chunks: List[Dict]):
    collection = get_chroma_collection()

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"page_num": c["page_num"], "source": c["source"]} for c in chunks]

    embeddings = embed_texts(texts)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )
