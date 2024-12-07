from application.auth.services.pkce import PKCEData
from application.client.commands.validate_client_request import ValidateClientRequest


class UserAuthRequest(ValidateClientRequest, PKCEData): ...
