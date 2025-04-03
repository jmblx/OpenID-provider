from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .metrics import add_metrics_middleware
from ..config import TRACING


def setup_middlewares(app: FastAPI):
    if TRACING:
        add_metrics_middleware(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://menoitami.ru"],  # или "*" для разработки
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["menoitami.ru"]
    )
