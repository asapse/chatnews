from lingua import Language, LanguageDetector, LanguageDetectorBuilder


LANG_MAPPING = {
    "English": Language.ENGLISH,
    "French": Language.FRENCH,
    "German": Language.GERMAN,
    "Spanish": Language.SPANISH,
}


class LangDetector:
    def __init__(
        self, languages: list[str] | None = None, threshold: float = 0.80
    ) -> None:
        self._languages: list[str | Language] = []
        if languages:
            self._languages = [
                LANG_MAPPING[lang] for lang in languages if lang in LANG_MAPPING
            ]
        if not languages and not self._languages:
            self._languages: list[str | Language] = list(LANG_MAPPING.values())

        self._detector: LanguageDetector = (
            LanguageDetectorBuilder.from_languages(*self._languages)
            .with_minimum_relative_distance(threshold)
            .build()
        )

    def detect(self, text) -> str | None:
        try:
            lang: str = self._detector.detect_language_of(text).name.capitalize()
        except AttributeError:
            return None
        return lang
