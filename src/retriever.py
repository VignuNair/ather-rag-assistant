import chromadb
from src.embedder import embed_texts 
from rank_bm25 import BM25Okapi 
from sentence_transformers import CrossEncoder

_client = chromadb.PersistentClient(path="data/store")
_col = _client.get_collection("docs")


def vector_search(query: str, k: int = 20) -> list[dict]:
    res = _col.query(
        query_embeddings=embed_texts([query]),
        n_results=k
    )

    return [
        {
            "id": i,
            "text": d,
            "meta": m,
            "score": 1 - dist
        }
        for i, d, m, dist in zip(
            res["ids"][0],
            res["documents"][0],
            res["metadatas"][0],
            res["distances"][0]
        )
    ]


_all = _col.get()

_corpus = [d.lower().split() for d in _all["documents"]]
_bm25 = BM25Okapi(_corpus)


def bm25_search(query: str, k: int = 20) -> list[dict]:
    scores = _bm25.get_scores(query.lower().split())

    top = sorted(
        range(len(scores)),
        key=lambda i: -scores[i]
    )[:k]

    return [
        {
            "id": _all["ids"][i],
            "text": _all["documents"][i],
            "meta": _all["metadatas"][i]
        }
        for i in top
    ]


def hybrid_search(query: str, k: int = 20, rrf_k: int = 60):
    v = vector_search(query, k)
    b = bm25_search(query, k)

    fused, seen = {}, {}

    for lst in (v, b):
        for rank, r in enumerate(lst):
            fused[r["id"]] = fused.get(r["id"], 0) + 1 / (rrf_k + rank)
            seen[r["id"]] = r

    order = sorted(
        fused,
        key=fused.get,
        reverse=True
    )[:k]

    return [
        {
            **seen[i],
            "score": fused[i]
        }
        for i in order
    ] 



_reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query: str, candidates: list[dict], k: int = 5):
    pairs = [(query, c["text"]) for c in candidates]

    scores = _reranker.predict(pairs)

    ranked = sorted(
        zip(candidates, scores),
        key=lambda x: -x[1]
    )[:k]

    return [
        {
            **c,
            "rerank_score": float(s)
        }
        for c, s in ranked
    ]


def retrieve(query: str, k: int = 5):
    candidates = hybrid_search(query, 20)
    return rerank(query, candidates, k)