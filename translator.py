from deep_translator import GoogleTranslator

class TranslatorService:
    def __init__(self, default_source="auto"):
        """
        TranslatorService manages translations.
        You can inject this class into other parts of the app.
        """
        self.default_source = default_source

    def translate_text(self, text: str, target_language: str = "en") -> str:
        """
        Translate text into target_language.
        If translation fails, return 'translation_failed'.
        """
        try:
            if target_language == "en":
                return text
            translator = GoogleTranslator(source=self.default_source, target=target_language)
            return translator.translate(text)
        except Exception as e:
            print(f"[TranslatorService] Translation failed: {e}")
            return "translation_failed"
