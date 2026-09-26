from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def transcribe_api(path: str) -> str:
    with open(path, "rb") as f:
        r = Groq().audio.transcriptions.create(
    file=f,
    model="whisper-large-v3-turbo",
    language="te"
)
    return r.text 


from gtts import gTTS

def speak(text: str, lang: str = "te",
          out: str = "reply.mp3") -> str:
    gTTS(text=text, lang=lang).save(out)
    return out