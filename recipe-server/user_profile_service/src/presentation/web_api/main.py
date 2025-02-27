import logging
import os
from contextlib import asynccontextmanager
from dataclasses import asdict

from dishka.integrations.fastapi import (
    setup_dishka,
)
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

# import core.db.logs  # noqa: F401
from src.core import container
from infrastructure.log.main import configure_logging
from presentation.web_api.config import load_config
from presentation.web_api.exceptions import setup_exception_handlers
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


setup_exception_handlers(app)


config = load_config()
setup_middlewares(app)

if os.getenv("GUNICORN_MAIN", "false").lower() not in ("false", "0"):

    def main():
        from presentation.web_api.gunicorn.application import Application

        configure_logging(config.app_logging_config)

        gunicorn_app = Application(
            application=app,
            options={
                **asdict(config.gunicorn_config),  # Опции Gunicorn
                "logconfig_dict": config.app_logging_config,  # Конфиг логирования
            },
        )
        logger.info(
            "Launch app", extra={"config": {"ya": "kros", "level": "DEBUG"}}
        )
        gunicorn_app.run()

    if __name__ == "__main__":
        main()

else:
    configure_logging(config.app_logging_config)
    logger.info(
        "Launch app", extra={"config": {"ya": "ebal", "level": "DEBUG"}}
    )
