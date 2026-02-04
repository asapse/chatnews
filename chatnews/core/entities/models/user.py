from chatnews.core.entities.models.nosql import NoSQLDocument


class User(NoSQLDocument):
    first_name: str
    last_name: str

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
