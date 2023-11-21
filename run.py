"""
Run FastAPI server.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from fastapi import FastAPI

from src.slack_bot import create_app

application: FastAPI = create_app()
if __name__ == "__main__":
    import uvicorn

    settings = application.state.settings
    uvicorn.run(
        "run:application",
        reload=True,
        host=settings.host,
        port=settings.port,
        log_level=settings.server_log_level,
        log_config="logging.json",
        use_colors=True,
    )
