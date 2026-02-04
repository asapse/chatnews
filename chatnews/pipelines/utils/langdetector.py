from lingua import Language, LanguageDetector, LanguageDetectorBuilder


class LangDetector:
    def __init__(self, languages: list[str] | None = None) -> None:
        if not languages:
            languages: list[str | Language] = [
                Language.ENGLISH,
                Language.FRENCH,
                Language.GERMAN,
                Language.SPANISH,
            ]
        self._detector: LanguageDetector = LanguageDetectorBuilder.from_languages(
            *languages
        ).build()

    def detect(self, text) -> str:
        lang: str = self._detector.detect_language_of(text).name.capitalize()
        return lang
