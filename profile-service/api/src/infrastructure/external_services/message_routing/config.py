import os

NATS_URL = os.environ.get("NATS_URL", "nats://localhost:4222")


class NatsConfig:
    def __init__(self, uri: str):
        self.uri = uri

    @staticmethod
    def from_env() -> "NatsConfig":
        return NatsConfig(uri=NATS_URL)
