"""
ETL Job configuration module.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class ETLSettings(BaseSettings):
    """Configuration settings for Etl job."""

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    redis_max_connections: int = 10

    redis_search_index: str = ""

    model_config = SettingsConfigDict(env_file=os.environ.get("ENV_FILE_PATH"))
