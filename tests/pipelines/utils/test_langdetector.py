from chatnews.pipelines.utils.langdetector import LangDetector


def test_detect_default():
    lang_detector = LangDetector()
    assert (
        lang_detector.detect("Je suis un test de détection de langue en français.")
        == "French"
    )


def test_detection_language_not_found():
    lang_detector = LangDetector(languages=["English", "German"])
    assert (
        lang_detector.detect("Je suis un test de détection de langue en français.")
        is None
    )
