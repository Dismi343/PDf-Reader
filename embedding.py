from sentence_transformers import SentenceTransformer
from typing import List

# Free embedding model (downloaded once)
_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: List[str]) -> List[list]:
  
    embeddings = _embedding_model.encode(texts, convert_to_numpy=False)
    return [e.tolist() for e in embeddings]
