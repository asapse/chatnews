from typing import Annotated
from urllib.parse import urlparse

from loguru import logger
from tqdm import tqdm
from zenml import get_step_context, step

from chatnews.core.adapters.databases.mongodb import MongoDB
from chatnews.core.entities.models.document import Document
from chatnews.core.entities.models.user import User
from chatnews.pipelines.utils.fetch import Fetch


DATABASE: MongoDB[Document] = MongoDB[Document]("chatnews", "articles", Document)


@step
def fetch_links(user: User, links: list[str]) -> Annotated[list[str], "fetch_links"]:
    logger.info(f"Starting to crawl {len(links)} link(s).")

    metadata = {}
    successfull_crawls = 0
    for link in tqdm(links):
        successfull_crawl, crawled_domain, documents_insert, documents_not_insert = (
            _crawl_link(str(user.id), link)
        )
        successfull_crawls += successfull_crawl

        metadata = _add_to_metadata(
            metadata,
            crawled_domain,
            successfull_crawl,
            documents_insert,
            documents_not_insert,
        )

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="fetch_links", metadata=metadata)

    logger.info(f"Successfully crawled {successfull_crawls} / {len(links)} links.")

    return links


def _crawl_link(user_id: str, link: str) -> tuple[bool, str, int, int]:
    fetcher = Fetch(link, user_id)
    domain = urlparse(link).netloc
    insert = 0
    not_insert = 0
    try:
        documents: list[Document] = fetcher.fetch()
        insert, not_insert = _save_documents(documents)
        return (True, domain, insert, not_insert)
    except Exception as e:
        logger.error(f"An error occurred while crowling: {e!s}")

        return (False, domain, insert, not_insert)


def _save_documents(documents: list[Document]) -> tuple[int, int]:
    insert = 0
    not_insert = 0
    for document in documents:
        if DATABASE.get(**{"url": document.url}):
            not_insert += 1
            continue

        DATABASE.create(document)
        insert += 1
    return (insert, not_insert)


def _add_to_metadata(
    metadata: dict,
    domain: str,
    successfull_crawl: bool,
    documents_insert: int,
    documents_not_insert: int,
) -> dict:
    if domain not in metadata:
        metadata[domain] = {}
    metadata[domain]["successful"] = (
        metadata[domain].get("successful", 0) + documents_insert
    )
    metadata[domain]["error"] = metadata[domain].get("error", 0) + documents_not_insert
    metadata[domain]["total"] = (
        metadata[domain].get("total", 0) + documents_insert + documents_not_insert
    )

    return metadata
