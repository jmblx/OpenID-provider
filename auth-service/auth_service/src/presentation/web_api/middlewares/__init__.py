from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .metrics import add_metrics_middleware
from ..config import TRACING


def setup_middlewares(app: FastAPI):
    if TRACING:
        add_metrics_middleware(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
