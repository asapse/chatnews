from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import (
    UUID4,
    AliasChoices,
    BaseModel,
    Field,
    SerializerFunctionWrapHandler,
    field_serializer,
)


class NoSQLDocument(BaseModel):
    id: UUID4 = Field(
        default_factory=uuid4, alias="_id", validation_alias=AliasChoices("id", "_id")
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False

        return self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id)

    @field_serializer("id", mode="wrap")
    def uuid_to_str(self, value: Any, handler: SerializerFunctionWrapHandler) -> str:
        return str(handler(value))
