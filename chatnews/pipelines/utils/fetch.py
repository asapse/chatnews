import re

import feedparser
import requests
from justext import get_stoplist, justext

from chatnews.core.entities.models.document import Content, Document
from chatnews.pipelines.utils.langdetector import LangDetector


class Fetch:
    def __init__(self, url: str, user_id: str) -> None:
        self._url: str = url
        self._lang_detector: LangDetector = LangDetector()
        self._paywall_pattern: re.Pattern[bytes] = re.compile(
            b'"isAccessibleForFree": "(False|True)"'
        )
        self._user_id: str = user_id

    def _find_lang(self, text: str) -> str:
        return self._lang_detector.detect(text)

    def _get_content_page(self, url: str) -> bytes:
        response = requests.get(url, timeout=10)
        return response.content

    def _is_paywall(self, content: bytes) -> bool:
        is_paywall: bool = False
        paywall_matchs = self._paywall_pattern.match(content) or []
        if b"True" in paywall_matchs:
            is_paywall = True

        return is_paywall

    def _get_body(self, content: bytes, language: str) -> str:
        paragraphs = justext(content, get_stoplist(language))
        body: str = ""
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate and "article" in paragraph.dom_path:
                body += paragraph.text
        return body

    def _parse_document(self, document: dict, rss_feed: str) -> Document:
        content_page = self._get_content_page(document["link"])
        lang: str = self._find_lang(document["summary"] or document["title"])
        paywall: bool = self._is_paywall(content_page)
        body: str = self._get_body(content_page, language=lang)

        if not body:
            body = self._get_body(content_page, language="English")
            if body:
                lang = "English"

        content = Content(
            title=document["title"], subtitle=document["summary"] or "", body=body
        )
        author: str = document["author"] or document["credit"] or "Unknow"
        document_format: Document = Document(
            content=content,
            url=document["link"],
            rss_feed=rss_feed,
            author=author,
            language=lang,
            paywall=paywall,
            user_id=self._user_id,
        )
        return document_format

    def _fetch_url(self, url) -> list[Document]:
        documents = feedparser.parse(url)
        documents_format: list[Document] = []
        for document in documents["entries"]:
            document_format: Document = self._parse_document(document, url)
            documents_format.append(document_format)
        return documents_format

    def fetch(self) -> list[Document]:
        documents: list[Document] = self._fetch_url(self._url)
        return documents
