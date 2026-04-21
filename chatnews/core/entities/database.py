from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseCRUD[T: BaseModel](ABC):
    model: type[T]

    @abstractmethod
    def create(self, data: T) -> str:
        pass

    @abstractmethod
    def get(self, id: str | None = None, **kwargs) -> T | None:
        pass

    @abstractmethod
    def update(self, id: str, data: T) -> T | None:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    def _to_model(self, data: dict) -> T | None:
        if data is None:
            return None
        return self.model.model_validate(data)

    @classmethod
    def model_validate(cls, data: dict) -> T:
        if not hasattr(cls, "model") or cls.model is None:
            raise NotImplementedError(
                "Subclass must set `model` attribute to a pydantic model class"
            )
        return cls.model.model_validate(data)
