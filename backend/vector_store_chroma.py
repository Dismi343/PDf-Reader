import chromadb
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection
from dotenv import load_dotenv
import os
from typing import List, Dict

#from requests import request
from embedding import embed_texts


load_dotenv()

_client: ClientAPI | None = None
_collection: Collection | None = None

def get_chroma_client() :
	global _client
	if _client is None:
		_client = chromadb.CloudClient(
            api_key=os.getenv("CHROMA_API_KEY"),
            tenant=os.getenv("CHROMA_TENANT"),
            database=os.getenv("CHROMA_DATABASE")
        )
	return _client

def get_chroma_collection() :
	global _collection
	client = get_chroma_client()  
	if _collection is None:
		_collection = client.get_or_create_collection(
		    name="pdf_semantic_search_collection",
            metadata={"hnsw:space": "cosine"}
		)
	return _collection


def index_chunks(chunks: List[Dict]):
    collection = get_chroma_collection()

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"page_num": c["page_num"], "source": c["source"]} for c in chunks]

    embeddings = embed_texts(texts)
    try:
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        return {"message": "Documents added successfully", "ids": ids}
    except Exception as e:
        print(f"Error indexing chunks: {e}")