import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

SYSTEM = """You are an assistant for House of Data.
Answer using ONLY the CONTEXT below.
If the context does not contain the answer, say
"I could not find that in the documents." Never guess.
Cite the source after every fact as [doc, p.N]."""

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def answer(query: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f'[{c["meta"]["doc"]}, p.{c["meta"]["page"]}]\n{c["text"]}'
        for c in chunks
    )

    r = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "openai/gpt-oss-20b"),
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"CONTEXT\n{context}\n\nQUESTION\n{query}"
            }
        ]
    )

    return r.choices[0].message.content