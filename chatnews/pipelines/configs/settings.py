from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mongodb_database: str
    mongodb_users_collection: str
    mongodb_articles_collection: str


PIPELINE_SETTINGS = PipelineSettings()
