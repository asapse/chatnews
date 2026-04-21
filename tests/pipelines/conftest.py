import json

import pytest

from chatnews.core.entities.models.document import Document


@pytest.fixture(scope="session")
def document() -> dict:
    with open("tests/resources/document.json") as fp:
        document = json.load(fp)
    return document


@pytest.fixture(scope="session")
def rss_document() -> dict:
    with open("tests/resources/rss_document.json") as fp:
        document = json.load(fp)
    return document


@pytest.fixture(scope="session")
def document_format(document: dict) -> Document:
    document_format = Document(**document)
    return document_format


@pytest.fixture(scope="session")
def rss_url() -> str:
    return "http://feeds.rssboard.org/rssboard"
