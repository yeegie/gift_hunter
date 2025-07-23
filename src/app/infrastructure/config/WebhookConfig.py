__all__ = [
    "WebhookConfig"
]


from pydantic import BaseModel


class WebhookConfig(BaseModel):
    listen_address: str
    listen_port: int
    base_url: str
    bot_path: str
    debug: bool = False
