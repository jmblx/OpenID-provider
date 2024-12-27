import logging
import os
from contextlib import asynccontextmanager
from dataclasses import asdict

from dishka.integrations.fastapi import (
    setup_dishka,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

# import core.db.logs  # noqa: F401
from core.di.container import container
from infrastructure.log.main import configure_logging
from presentation.web_api.config import load_config
from presentation.web_api.endpoints.auth.router import auth_router
from presentation.web_api.endpoints.client.client_router import client_router
from presentation.web_api.exceptions import setup_exception_handlers
from presentation.web_api.endpoints.investments.router import inv_router
from presentation.web_api.endpoints.registration.router import reg_router
from presentation.web_api.endpoints.role.router import role_router
from presentation.web_api.endpoints.strategy.router import strategy_router
from presentation.web_api.endpoints.token_manage.router import token_manage_router
from presentation.web_api.middlewares import setup_middlewares


@asynccontextmanager  # type: ignore
async def lifespan(app: FastAPI) -> None:  # type: ignore
    yield
    await app.state.dishka_container.close()  # type: ignore


app = FastAPI(
    lifespan=lifespan, root_path="/api", default_response_class=ORJSONResponse
)

setup_dishka(container=container, app=app)

logger = logging.getLogger(__name__)

# logstash_handler = TCPLogstashHandler("logstash", 50000)
# logger.addHandler(logstash_handler)

app.include_router(reg_router)
app.include_router(client_router)
app.include_router(auth_router)
app.include_router(role_router)
app.include_router(token_manage_router)
app.include_router(inv_router)
app.include_router(strategy_router)
setup_exception_handlers(app)


config = load_config()
setup_middlewares(app)

if os.getenv("GUNICORN_MAIN", "false").lower() not in ("false", "0"):
    def main():
        from presentation.web_api.gunicorn.application import Application

        configure_logging(config.app_logging_config)

        gunicorn_app = Application(
            application=app,
            options=asdict(
                config.gunicorn_logging_config # type: ignore
            ),
        )
        logger.info("Launch app", extra={"config": {"ya": "ebal", "level": "DEBUG"}})
        gunicorn_app.run()

    if __name__ == "__main__":
        main()

else:
    configure_logging(config.app_logging_config)
    logger.info("Launch app", extra={"config": {"ya": "ebal", "level": "DEBUG"}})
