# Write chunk_records(records, size=900, overlap=150). Split text by paragraphs and pack them into chunks. Preserve metadata and add chunk_id.
def chunk_text(text: str, size: int = 900,
               overlap: int = 150) -> list[str]:
    """Split on paragraphs, then pack to ~size chars."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], ""

    for para in paras:
        if len(cur) + len(para) <= size:
            cur += ("\n\n" if cur else "") + para
        else:
            if cur:
                chunks.append(cur)
            cur = (cur[-overlap:] + "\n\n" + para) if cur else para

    if cur:
        chunks.append(cur)

    return chunks


def chunk_records(records: list[dict]) -> list[dict]:
    out = []

    for r in records:
        for j, c in enumerate(chunk_text(r["text"])):
            out.append({
                **r,
                "text": c,
                "chunk_id": f'{r["doc_id"]}#{r["page"]}#{j}'
            })

    return out