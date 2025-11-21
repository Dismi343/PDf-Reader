import chromadb

chroma = chromadb.Client()
collection = chroma.create_collection("pdf_chunks")
