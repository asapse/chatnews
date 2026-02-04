import os
from typing import Annotated

from loguru import logger
from zenml import get_step_context, step

from chatnews.core.adapters.databases.mongodb import MongoDB
from chatnews.core.entities.models.user import User


DATABASE_NAME: str = os.getenv("MONGODB_DATABASE", "chatnews")
COLLECTION_NAME: str = os.getenv("MONGODB_USERS_COLLECTION", "users")

DATABASE: MongoDB[User] = MongoDB[User](DATABASE_NAME, COLLECTION_NAME, User)


@step
def get_or_create_user(user_full_name: str) -> Annotated[User, "user"]:
    logger.info(f"Getting or creating user: {user_full_name}")

    first_name, last_name = user_full_name.split(" ")

    user_data = {"first_name": first_name, "last_name": last_name}
    user = DATABASE.get(**user_data)
    if user is None:
        user = DATABASE.create(User(**user_data))

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="user", metadata=_get_metadata(user_full_name, user)
    )

    return user


def _get_metadata(user_full_name: str, user: User) -> dict:
    return {
        "query": {
            "user_full_name": user_full_name,
        },
        "retrieved": {
            "user_id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }
