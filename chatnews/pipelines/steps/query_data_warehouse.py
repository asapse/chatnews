from datetime import datetime
from typing import Annotated

from loguru import logger
from zenml import get_step_context, step

from chatnews.core.adapters.databases.mongodb import MongoDB
from chatnews.core.entities.models.document import Document
from chatnews.core.entities.models.nosql import NoSQLDocument
from chatnews.core.entities.models.user import User
from chatnews.pipelines.configs.settings import PIPELINE_SETTINGS


DATABASE_NAME: str = PIPELINE_SETTINGS.mongodb_database
COLLECTION_NAME: str = PIPELINE_SETTINGS.mongodb_articles_collection


DATABASE: MongoDB[Document] = MongoDB[Document](
    DATABASE_NAME, COLLECTION_NAME, Document
)


@step
def query_data_warehouse(
    users: list[User], last_run: datetime
) -> Annotated[list[NoSQLDocument], "raw_documents"]:
    documents: list[NoSQLDocument] = []

    for user in users:
        logger.info("Querying data warehouse for user: %s", user.full_name)

        user_documents = fetch_all_data(user, last_run)
        documents.extend(user_documents)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="raw_documents", metadata=_get_metadata(documents)
    )

    return documents


def _filter(user_id: str, last_run: datetime) -> dict:
    query_filter = {"user_id": user_id, "updated_at": {"$gt": last_run}}
    return query_filter


def fetch_all_data(user: User, last_run: datetime) -> list[NoSQLDocument]:
    user_id = str(user.id)
    query_filter = _filter(user_id, last_run)
    logger.info(f"{query_filter}")
    documents = DATABASE.find(query_filter)
    logger.info(f"NB DOCUMENTS: {len(documents)}")
    return documents


def _get_metadata(documents: list[NoSQLDocument]) -> dict:
    metadata = {
        "num_documents": len(documents),
    }
    for document in documents:
        user_id = document.user_id
        if user_id not in metadata:
            metadata[user_id] = {}

        metadata[user_id][document.rss_feed] = (
            metadata[user_id].get(document.rss_feed, 0) + 1
        )

        metadata[user_id]["num_documents"] = (
            metadata[user_id].get("num_documents", 0) + 1
        )

    return metadata
