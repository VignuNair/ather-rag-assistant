import csv
from src.retriever import retrieve


def evaluate(path="eval/queries.csv", keep=8):
    hits = total = 0
    misses = []

    for row in csv.DictReader(open(path)):
        total += 1

        got = retrieve(row["question"], k=keep)

        pages = {
            (c["meta"]["doc"], str(c["meta"]["page"]))
            for c in got
        }

        want = (row["source_doc"], row["source_page"])

        if want in pages:
            hits += 1
        else:
            misses.append(row["question"])

    print(f"recall@{keep} = {hits}/{total} = {hits/total:.2f}")

    print("\nMissed:")
    [print(" -", m) for m in misses[:10]]


if __name__ == "__main__":
    evaluate()