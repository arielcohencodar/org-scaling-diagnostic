# translator.py
from deep_translator import GoogleTranslator

def translate(text, target_language):
    try:
        if target_language != "en":
            return GoogleTranslator(source='auto', target=target_language).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
    return text