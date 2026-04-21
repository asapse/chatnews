from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from pymongo import errors

from chatnews.core.entities.models.document import Document
from chatnews.pipelines.steps import fetch_rss


@pytest.fixture(scope="module")
def default_metadata() -> dict:
    metadata = {"abc.com": {"successful": 0, "error": 0, "total": 0}}
    return metadata


def test_add_metadata(default_metadata: dict) -> None:
    metadata = fetch_rss._add_to_metadata(default_metadata, "abc.com", 1, 1)
    assert len(metadata.keys()) == 1
    assert metadata["abc.com"]["successful"] == 1
    assert metadata["abc.com"]["error"] == 1
    assert metadata["abc.com"]["total"] == 2


def test_add_empty_metadata() -> None:
    metadata = fetch_rss._add_to_metadata({}, "abc.com", 1, 1)
    assert len(metadata.keys()) == 1
    assert metadata["abc.com"]["successful"] == 1
    assert metadata["abc.com"]["error"] == 1
    assert metadata["abc.com"]["total"] == 2


def test_save_documents(document_format: Document) -> None:
    insert, not_insert = fetch_rss._save_documents([document_format])
    assert insert == 1
    assert not_insert == 0


def test_save_documents_not_insert(document_format: Document) -> None:
    insert, not_insert = fetch_rss._save_documents([document_format])
    assert insert == 0
    assert not_insert == 1


def test_crawl_link(rss_url: str) -> None:
    result, domain, insert, not_insert = fetch_rss._crawl_link("acbd", rss_url)
    assert result
    assert domain == urlparse(rss_url).netloc
    assert insert > 0
    assert not_insert == 0


def test_crawl_link_error(rss_url: str) -> None:
    with patch(
        "chatnews.core.adapters.databases.mongodb.MongoDB.get",
        side_effect=errors.PyMongoError,
    ):
        result, domain, insert, not_insert = fetch_rss._crawl_link("acbd", rss_url)
    assert not result
    assert domain == urlparse(rss_url).netloc
    assert insert == 0
    assert not_insert == 0
