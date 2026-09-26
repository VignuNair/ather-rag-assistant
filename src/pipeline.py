from src.retriever import retrieve
from src.generator import answer


def ask(query: str) -> str:
    chunks = retrieve(query, k=5)
    return answer(query, chunks) 


from src.speech import transcribe_api, speak
from src.translate import translate 


def ask_telugu_voice(audio_path: str) -> tuple[str, str, str]:
    # 1. Telugu voice → Telugu text
    telugu_question = transcribe_api(audio_path)

    # 2. Telugu text → English text
    english_question = translate(
        telugu_question,
        src="tel_Telu",
        tgt="eng_Latn"
    ) 

    print("ENGLISH QUESTION:", english_question)

    # 3. English question → existing RAG pipeline
    english_answer = ask(english_question)

    # 4. English answer → Telugu text
    telugu_answer = translate(
        english_answer,
        src="eng_Latn",
        tgt="tel_Telu"
    )

    # 5. Telugu text → Telugu voice
    audio_reply = speak(
        telugu_answer,
        lang="te",
        out="audio/telugu_reply.mp3"
    )

    return telugu_question, telugu_answer, audio_reply