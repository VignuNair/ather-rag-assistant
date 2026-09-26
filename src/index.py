import chromadb

from src.ingest import load_pdfs
from src.chunker import chunk_records
from src.embedder import embed_texts


def build(pdf_dir="data/pdfs", store="data/store"):
    client = chromadb.PersistentClient(path=store)

    client.delete_collection("docs") if "docs" in [
        c.name for c in client.list_collections()
    ] else None

    col = client.create_collection(
        "docs",
        metadata={"hnsw:space": "cosine"}
    )

    chunks = chunk_records(load_pdfs(pdf_dir))

    col.add(
        ids=[c["chunk_id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embed_texts([c["text"] for c in chunks]),
        metadatas=[
            {"doc": c["doc_id"], "page": c["page"]}
            for c in chunks
        ],
    )

    print("indexed", col.count(), "chunks")


if __name__ == "__main__":
    build()