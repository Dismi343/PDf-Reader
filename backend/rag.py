from rag_retrieval import retrieve_relevant_chunks
from llama_openrouter import answer_query_with_openrouter

def answer_query(query: str) -> str:
   
    contexts = retrieve_relevant_chunks(query, top_k=5)
    if not contexts:
        return "I couldn't find any relevant information in the indexed PDFs."

    return answer_query_with_openrouter(query, contexts)
