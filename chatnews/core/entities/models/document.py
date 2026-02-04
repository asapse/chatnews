from pydantic import BaseModel

from chatnews.core.entities.models.nosql import NoSQLDocument


class Content(BaseModel):
    title: str
    subtitle: str
    body: str


class Document(NoSQLDocument):
    content: Content
    url: str
    rss_feed: str
    author: str
    language: str
    paywall: bool
    user_id: str
