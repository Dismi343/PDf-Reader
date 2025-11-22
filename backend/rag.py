#from rag_retrieval import retrieve_relevant_chunks #chromadb retrieval
from llama_openrouter import answer_query_with_openrouter

from Mongo_db.rag_retrieval_mongo import retrieve_relevant_chunks  #mongo retrieval

def answer_query(query: str) -> str:
   
    contexts = retrieve_relevant_chunks(query, top_k=5)
    if not contexts:
        return "I couldn't find any relevant information in the indexed PDFs."

    return answer_query_with_openrouter(query, contexts)
