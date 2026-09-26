# Write load_pdfs(folder) using PyMuPDF. One record per page as a dict with doc_id, page, text and source. Skip pages with under 30 characters and collect them in a skipped list. Print a summary. Type hints and a docstring.
import fitz  # pymupdf
from pathlib import Path


def load_pdfs(folder: str) -> list[dict]:
    """Read every PDF; one record per page."""
    records, skipped = [], []

    for path in sorted(Path(folder).glob("*.pdf")):
        doc = fitz.open(path)

        for i, page in enumerate(doc):
            text = page.get_text().strip()

            if len(text) < 30:
                skipped.append((path.name, i))
                continue

            records.append({
                "doc_id": path.stem,
                "page": i + 1,
                "text": text,
                "source": str(path),
            })

    print(f"{len(records)} pages, {len(skipped)} skipped")
    return records

