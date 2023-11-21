"""
This module provides a Pydantic-based settings configuration.

It reads the configuration values from environment variables,
with a fallback to a `.env` file.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for Slack integration."""

    slack_bot_token: str
    slack_signing_secret: str

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    redis_max_connections: int = 10

    redis_search_index: str = ""

    host: str = "0.0.0.0"
    port: int = 3000

    server_log_level: str = "info"
    app_log_level: str = "debug"
    logging_path: str = "logging.json"

    model_config = SettingsConfigDict(env_file=".env")
