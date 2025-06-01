# translation_logic.py
from deep_translator import GoogleTranslator
from deep_translator.exceptions import NotValidPayload, TranslationNotFound

SUPPORTED_LANGUAGES_GOOGLE = GoogleTranslator().get_supported_languages(as_dict=True)
SORTED_LANGUAGES_GOOGLE = dict(sorted(SUPPORTED_LANGUAGES_GOOGLE.items(), key=lambda item: item[1]))

class LanguageTranslatorApp:
    def __init__(self):
        pass # Using GoogleTranslator directly

    def get_available_languages(self):
        return SORTED_LANGUAGES_GOOGLE

    def translate_text(self, text_to_translate, target_language_code, source_language_code="auto"):
        if not text_to_translate.strip():
            return "Error: No text provided."

        try:
            translator = GoogleTranslator(source=source_language_code, target=target_language_code)
            translated_text = translator.translate(text_to_translate)
            
            if translated_text is None:
                return "Translation failed or no result."
            return translated_text

        except NotValidPayload:
            return "Error: Text is too long or invalid."
        except TranslationNotFound:
            return f"Error: Translation not found for {source_language_code}->{target_language_code}."
        except ConnectionError:
            return "Error: Connection issue. Check internet."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"