# vector_store_mongo.py
from typing import List, Dict
from .mongo_client import get_chunks_collection
from embedding import embed_texts
import numpy as np


def index_chunks(chunks: List[Dict]):
    """
    Take list of chunks (with text, chunk_id, page_num, source),
    embed them, and store in MongoDB.
    """
    collection = get_chunks_collection()

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]

    embeddings = embed_texts(texts)  # List[list[float]]

    docs_to_insert = []
    for chunk, emb, _id in zip(chunks, embeddings, ids):
        docs_to_insert.append(
            {
                "_id": _id,  # use chunk_id as _id
                "text": chunk["text"],
                "page_num": chunk["page_num"],
                "source": chunk["source"],
                "embedding": emb,  # store the vector as an array of floats
            }
        )

    if docs_to_insert:
        # upsert (in case same chunk_id exists)
        for doc in docs_to_insert:
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": doc},
                upsert=True
            )
        print(f"Indexed {len(docs_to_insert)} chunks into MongoDB.")
    else:
        print("No chunks to index.")


