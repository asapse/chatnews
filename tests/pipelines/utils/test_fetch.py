from unittest.mock import patch

import pytest

from chatnews.core.entities.models.document import Document
from chatnews.pipelines.utils.fetch import Fetch


@pytest.fixture(scope="module")
def user_id() -> str:
    return "123456789"


@pytest.fixture(scope="module")
def fetch(rss_url: str, user_id: str) -> Fetch:
    return Fetch(rss_url, user_id)


@pytest.fixture(scope="module")
def default_content(fetch: Fetch) -> bytes:
    return fetch._get_content_page(
        "https://www.ouest-france.fr/bretagne/plerin-22190/plerin-au-legue-le-mar-mousse-antre-de-la-biere-bretonne-5493870"
    )


def test_find_lang_default(fetch: Fetch) -> None:
    assert (
        fetch._find_lang(
            "Bonjour, je souhaiterai une galette saucisse, s'il vous plaît, merci"
        )
        == "French"
    )


def test_find_lang_unknow(fetch: Fetch) -> None:
    assert fetch._find_lang("Demat, ur silzig mo, mar plij, trugarez") is None


def test_get_content_page(fetch: Fetch) -> None:
    assert isinstance(
        fetch._get_content_page("https://br.wikipedia.org/wiki/Degemer"), bytes
    )


def test_is_paywall(fetch: Fetch) -> None:
    content = fetch._get_content_page(
        "https://www.ft.com/content/91bcf142-a1da-42ec-ac73-ba66ed12fb90"
    )
    assert fetch._is_paywall(content)


def test_is_not_paywall(fetch: Fetch, default_content: bytes) -> None:
    assert not fetch._is_paywall(default_content)


def test_get_body(fetch: Fetch, default_content: bytes) -> None:
    assert fetch._get_body(default_content, "French")


def test_get_body_no_extraction(fetch: Fetch, default_content: bytes) -> None:
    assert not fetch._get_body(default_content, "German")


def test_parse_document(fetch: Fetch, rss_document: dict, rss_url: str) -> None:
    document_format = fetch._parse_document(rss_document, rss_url)
    assert isinstance(document_format, Document)
    assert document_format.content.body != ""


def test_parse_document_bad_lang_detect(
    fetch: Fetch, rss_document: dict, rss_url: str
) -> None:
    with patch(
        "chatnews.pipelines.utils.fetch.Fetch._find_lang", return_value="French"
    ):
        document_format = fetch._parse_document(rss_document, rss_url)
        assert isinstance(document_format, Document)
        assert document_format.language == "English"
        assert document_format.content.body != ""


def test_fetch_url(fetch: Fetch) -> None:
    documents = fetch._fetch_url(fetch._url)
    assert len(documents) > 0
    assert isinstance(documents[0], Document)


def test_fetch_bad_url(fetch: Fetch) -> None:
    documents = fetch._fetch_url(fetch._url + "/abcd")
    assert len(documents) == 0


def test_fetch(fetch: Fetch) -> None:
    documents = fetch.fetch()
    assert len(documents) > 0
    assert isinstance(documents[0], Document)
