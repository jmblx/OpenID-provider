from application.client.get_client.client_queries import ValidateClientRequest
from application.common.services.pkce import PKCEData


class UserAuthRequest(ValidateClientRequest, PKCEData): ...
