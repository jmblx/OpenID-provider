import os

from pydantic import BaseModel


class AdminSettings(BaseModel):
    admin_passwords: str = os.getenv('API_ADMIN_PASSWORDS')
    admin_emails: str = os.getenv('API_ADMIN_EMAILS')
