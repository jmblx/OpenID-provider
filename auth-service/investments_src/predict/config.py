import os
from dataclasses import dataclass, field
from email.policy import default
from typing import Literal

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class GigaChatSettings:
    credentials: str
    model: Literal["GigaChat", "GigaChat Pro", "GigaChat Max"]
    scope: str

    @staticmethod
    def from_env() -> "GigaChatSettings":
        credentials = os.environ.get("GIGACHAT_CREDENTIALS", None)
        model = os.environ.get("GIGACHAT_MODEL", "GigaChat")
        scope = os.environ.get("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")

        if not credentials:
            raise RuntimeError("Missing GIGACHAT_CREDENTIALS environment variable")
        return GigaChatSettings(credentials=credentials, model=model, scope=scope)
