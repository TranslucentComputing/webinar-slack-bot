"""
This module provides the lifespan context manager function for the FastAPI application.

The lifespan context manager handles the setup and teardown of resources during
the lifespan of the application, specifically managing the connections for the Redis
database through the AsyncRedisDAOFactory.

It is used during the startup and shutdown events of the FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from ..daos.redis_dao_factory_async import AsyncRedisDAOFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for managing the lifespan of the FastAPI application.

    This function is responsible for setting up and tearing down resources during
    the lifespan of the app.
    It initializes the Redis connection pool at the beginning and closes the connection
    pool upon completion.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This function yields control back to the FastAPI event loop until
            the application is shut down.
    """
    if app.state.settings is None:
        raise ValueError("The app settings are not set.")

    # Access settings from app.state
    app_settings = app.state.settings

    # Set up resources using app_settings
    AsyncRedisDAOFactory.get_connection_pool(
        host=app_settings.redis_host,
        port=app_settings.redis_port,
        db=app_settings.redis_db,
        password=app_settings.redis_password,
        max_connections=app_settings.redis_max_connections,
    )

    # Yield back to the FastAPI event loop.
    yield

    # Tear down resources - here, we close the Redis connection pool.
    await AsyncRedisDAOFactory.reset_connection_pool()
