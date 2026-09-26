from transformers import pipeline

_tr = pipeline(
    "translation",
    model="facebook/nllb-200-distilled-600M"
)

def translate(text, src="tel_Telu", tgt="eng_Latn"):
    return _tr(
        text,
        src_lang=src,
        tgt_lang=tgt
    )[0]["translation_text"]