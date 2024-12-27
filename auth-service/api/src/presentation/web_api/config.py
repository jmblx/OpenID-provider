import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from infrastructure.log.main import AppLoggingConfig
from presentation.web_api.gunicorn.config import GunicornConfig

load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
API_ADMIN_PWD = os.environ.get("API_ADMIN_PWD")
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent.parent / "config" / "config.toml"


@dataclass
class PresentationConfig:
    gunicorn_logging_config: GunicornConfig
    app_logging_config: AppLoggingConfig


def read_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)

data = read_toml(str(DEFAULT_CONFIG_PATH))


def load_config(path: str | None = None) -> PresentationConfig:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    data = read_toml(path)

    gunicorn_config = GunicornConfig(**data.get("gunicorn"))
    app_logging_config = AppLoggingConfig(**data.get("logging"))
    return PresentationConfig(gunicorn_config, app_logging_config)
