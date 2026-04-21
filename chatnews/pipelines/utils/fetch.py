import re

import feedparser
import requests
from fake_useragent import UserAgent
from justext import get_stoplist, justext

from chatnews.core.entities.models.document import Content, Document
from chatnews.pipelines.utils.langdetector import LangDetector


class Fetch:
    def __init__(self, url: str, user_id: str) -> None:
        self._url: str = url
        self._lang_detector: LangDetector = LangDetector()
        self._paywall_pattern: re.Pattern[bytes] = re.compile(
            b'"isAccessibleForFree": ?"(False|True)"'
        )
        self._user_id: str = user_id
        self._default_language: str = "English"

    def _find_lang(self, text: str) -> str | None:
        return self._lang_detector.detect(text)

    def _get_content_page(self, url: str) -> bytes:
        headers = {"User-Agent": UserAgent().firefox}
        response = requests.get(url, headers=headers, timeout=10)
        return response.content

    def _is_paywall(self, content: bytes) -> bool:
        return b"False" in self._paywall_pattern.findall(content)

    def _text_to_markdown(self, text: str, element: str) -> str:
        match element:
            case "h1":
                return f"# {text}"
            case "h2":
                return f"## {text}"
            case "h3":
                return f"### {text}"
            case _:
                return text

    def _get_body(self, content: bytes, language: str) -> str:
        paragraphs = justext(content, get_stoplist(language))
        body: str = ""
        body_full_page: str = ""
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                dom_path = paragraph.dom_path
                text = self._text_to_markdown(paragraph.text, dom_path.split(".")[-1])
                if "article" in paragraph.dom_path:
                    body += text
                body_full_page += text
        return body or body_full_page

    def _parse_document(self, document: dict, rss_feed: str) -> Document:
        content_page = self._get_content_page(document["link"])
        lang: str = (
            self._find_lang(document["summary"] or document["title"])
            or self._default_language
        )
        paywall: bool = self._is_paywall(content_page)

        body: str = self._get_body(content_page, language=lang)
        if not body and lang != self._default_language:
            body = self._get_body(content_page, language=self._default_language)
            lang = self._default_language

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

    def _fetch_url(self, url: str) -> list[Document]:
        documents = feedparser.parse(url)
        documents_format: list[Document] = []
        for document in documents["entries"]:
            document_format: Document = self._parse_document(document, url)
            documents_format.append(document_format)
        return documents_format

    def fetch(self) -> list[Document]:
        documents: list[Document] = self._fetch_url(self._url)
        return documents
