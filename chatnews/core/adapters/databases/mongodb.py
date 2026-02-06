from typing import TypeVar

from pydantic import BaseModel
from pymongo import MongoClient, collection, database, errors

from chatnews.core.entities.database import BaseCRUD


T = TypeVar("T", bound=BaseModel)


class MongoDB(BaseCRUD[T]):
    def __init__(
        self, database_name: str, collection_name: str, model: type[T]
    ) -> None:
        self._database: database.Database = MongoClient().get_database(database_name)
        self._collection: collection.Collection = self._database.get_collection(
            collection_name
        )
        self.model = model

    def create(self, data: T) -> str:
        try:
            response = self._collection.insert_one(data.model_dump(by_alias=True))
        except errors.WriteError as err:
            raise err
        return str(response.inserted_id)

    def get(self, id: str | None = None, **kwargs) -> T | None:
        filter = {"_id": id} if id else kwargs
        try:
            result = self._collection.find_one(filter)
        except errors.PyMongoError as err:
            raise err
        return self._to_model(result)

    def update(self, id: str, data: T) -> T | None:
        try:
            result = self._collection.update_one(
                {"_id": id}, update=data.model_dump(by_alias=True)
            )
        except errors.PyMongoError as err:
            raise err
        return self._to_model(result)

    def delete(self, id: str) -> bool:
        try:
            result = self._collection.delete_one({"_id": id})
        except errors.PyMongoError as err:
            raise err
        return result.deleted_count == 1
