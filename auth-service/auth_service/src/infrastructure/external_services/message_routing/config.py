import os

NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")
EMAIL_RESET_PWD_SUB = os.getenv("EMAIL_RESET_PWD_SUB", "email.reset_password")
EMAIL_CONFIRMATION_SUB = os.getenv(
    "EMAIL_CONFIRMATION_SUB", "email.confirmation"
)


class NatsConfig:
    def __init__(
        self, uri: str, reset_pwd_email_sub: str, email_confirmation_sub: str
    ):
        self.uri = uri
        self.reset_pwd_email_sub = reset_pwd_email_sub
        self.email_confirmation_sub = email_confirmation_sub

    @staticmethod
    def from_env() -> "NatsConfig":
        return NatsConfig(
            uri=NATS_URL,
            reset_pwd_email_sub=EMAIL_RESET_PWD_SUB,
            email_confirmation_sub=EMAIL_CONFIRMATION_SUB,
        )
