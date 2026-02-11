from datetime import datetime

from zenml import pipeline

from chatnews.pipelines.steps.get_or_create_user import get_or_create_users
from chatnews.pipelines.steps.query_data_warehouse import query_data_warehouse


@pipeline
def features_store(users_full_name: list[str], last_run: datetime) -> str:
    users = get_or_create_users(users_full_name)
    raw_documents = query_data_warehouse(users, last_run)

    return raw_documents.invocation_id
