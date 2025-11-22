from typing import List, Dict

def chunk_text(
    pages: List[Dict],
    max_chars: int = 800,
    overlap: int = 150
) -> List[Dict]:
  
    chunks = []
    chunk_id = 0

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + max_chars
            chunk = text[start:end].strip()
            if chunk:
                chunks.append({
                    "chunk_id": f"{page['source']}_p{page['page_num']}_c{chunk_id}",
                    "text": chunk,
                    "page_num": page["page_num"],
                    "source": page["source"],
                })
                chunk_id += 1

            start = end - overlap  # move with overlap

    return chunks
