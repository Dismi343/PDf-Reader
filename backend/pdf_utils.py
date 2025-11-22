from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader

def extract_pdf_pages(pdf_path: str) -> List[Dict]:


    """
    Reads a PDF and returns a list of:
    { 'page_num': int, 'text': str, 'source': str }
    """
    path = Path(pdf_path)
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        pages.append({
            "page_num": i + 1,
            "text": text,
            "source": path.name
        })

    return pages
