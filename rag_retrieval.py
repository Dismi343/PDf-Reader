from typing import List, Dict
from vector_store import get_collection
from embedding import embed_texts

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[Dict]:
 
    collection = get_collection()
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    contexts = []
    if not results["ids"]:
        return contexts

    for i in range(len(results["ids"][0])):
        contexts.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
        })

    return contexts
