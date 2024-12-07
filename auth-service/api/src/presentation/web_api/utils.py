from typing import Any

from starlette.requests import Request

from domain.entities.client.model import Client
from presentation.web_api.auth.models import UserAuthRequest


def convert_request_to_render(client: Client, data: UserAuthRequest, request: Request) -> dict[str, Any]:
    return {
        "request": request,
        "redirect_url": data.redirect_url,
        "client_name": client.name.value,
        "client_id": client.id.value,
        "code_verifier": data.code_verifier,
        "code_challenge_method": data.code_challenge_method,
    }
