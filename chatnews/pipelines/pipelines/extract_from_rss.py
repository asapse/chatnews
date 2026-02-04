from typing import Any

from zenml import pipeline

from chatnews.pipelines.steps.fetch_rss import fetch_links
from chatnews.pipelines.steps.get_or_create_user import get_or_create_user


@pipeline
def digital_data_etl(user_full_name: str, links: list[str]) -> str:
    user: Any = get_or_create_user(user_full_name)
    last_step = fetch_links(user, links=links)

    return last_step.invocation_id
