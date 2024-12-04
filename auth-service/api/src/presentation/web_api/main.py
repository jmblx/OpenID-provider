import logging
import os
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import (
    setup_dishka,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

import core.db.logs  # noqa: F401
from core.di.container import container
from presentation.web_api.auth.router import auth_router
from presentation.web_api.client.client_router import client_router
from presentation.web_api.exceptions import setup_exception_handlers
from presentation.web_api.registration.router import reg_router
from presentation.web_api.role.router import role_router
from presentation.web_api.token_manage.router import token_manage_router


@asynccontextmanager  # type: ignore
async def lifespan(app: FastAPI) -> None:  # type: ignore
    yield
    await app.state.dishka_container.close()  # type: ignore


app = FastAPI(
    lifespan=lifespan, root_path="/api", default_response_class=ORJSONResponse
)

setup_dishka(container=container, app=app)

logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)

# logstash_handler = TCPLogstashHandler("logstash", 50000)
# logger.addHandler(logstash_handler)

app.include_router(reg_router)
app.include_router(client_router)
app.include_router(auth_router)
app.include_router(role_router)
app.include_router(token_manage_router)
setup_exception_handlers(app)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if os.getenv("GUNICORN_MAIN", "false").lower() not in ("false", "0"):

    def main():
        from infrastructure.gunicorn.app_options import get_app_options
        from infrastructure.gunicorn.application import Application
        from infrastructure.gunicorn.config import app_settings
        Application(
            application=app,
            options=get_app_options(
                host=app_settings.gunicorn.host,
                port=app_settings.gunicorn.port,
                timeout=app_settings.gunicorn.timeout,
                workers=app_settings.gunicorn.workers,
                log_level=app_settings.logging.log_level,
            ),
        ).run()


    if __name__ == "__main__":
        main()
