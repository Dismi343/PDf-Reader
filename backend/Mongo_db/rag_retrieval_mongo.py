from typing import List, Dict, Optional
import numpy as np
from Mongo_db.mongo_client import get_chunks_collection
from embedding import embed_texts


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two 1D vectors.
    """
    if a.ndim != 1 or b.ndim != 1:
        raise ValueError("cosine_similarity expects 1D vectors")

    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0

    return float(np.dot(a, b) / denom)


def retrieve_relevant_chunks(
    query: str,
    top_k: int = 5,
    source: Optional[str] = None,
) -> List[Dict]:
    """
    Retrieve top_k relevant chunks from MongoDB based on semantic similarity.

    - query: user question text
    - top_k: number of chunks to return
    - source: optional filter by PDF filename, e.g. "myfile.pdf"
    """
    collection = get_chunks_collection()

    # 1) Embed the query
    query_embedding = embed_texts([query])[0]
    query_vec = np.array(query_embedding, dtype=float)

    # 2) Get candidate chunks from MongoDB
    mongo_filter = {}
    if source:
        # Only chunks from a specific PDF
        mongo_filter["source"] = source

    docs = list(collection.find(mongo_filter))

    if not docs:
        return []

    # 3) Compute cosine similarity in Python
    scored_docs = []
    for d in docs:
        emb = np.array(d["embedding"], dtype=float)
        score = _cosine_similarity(query_vec, emb)
        scored_docs.append((score, d))

    # 4) Sort by similarity and take top_k
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top = scored_docs[:top_k]

    # 5) Convert to the same "contexts" structure you had before
    contexts: List[Dict] = []
    for score, d in top:
        contexts.append(
            {
                "id": str(d.get("_id")),  # Mongo _id
                "text": d.get("text", ""),
                "metadata": {
                    "page_num": d.get("page_num"),
                    "source": d.get("source"),
                    "similarity": score,
                },
            }
        )

    return contexts
