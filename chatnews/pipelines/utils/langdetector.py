from lingua import Language, LanguageDetector, LanguageDetectorBuilder


class LangDetector:
    def __init__(
        self, languages: list[str] | None = None, threshold: float = 0.80
    ) -> None:
        self._languages_mapping = {
            "English": Language.ENGLISH,
            "French": Language.FRENCH,
            "German": Language.GERMAN,
            "Spanish": Language.SPANISH,
        }
        self._languages: list[str | Language] = []
        if languages:
            self._languages = [
                self._languages_mapping[lang]
                for lang in languages
                if lang in self._languages_mapping
            ]
        if not languages and not self._languages:
            self._languages: list[str | Language] = list(
                self._languages_mapping.values()
            )

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
