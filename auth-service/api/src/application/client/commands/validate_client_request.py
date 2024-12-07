from pydantic import BaseModel

class ValidateClientRequest(BaseModel):
    client_id: int
    redirect_url: str
