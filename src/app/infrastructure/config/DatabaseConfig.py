__all__ = [
    "DatabaseConfig"
]

from pydantic import BaseModel, SecretStr


class DatabaseConfig(BaseModel):
    driver: str
    host: str
    port: int
    user: str
    password: SecretStr
    database: str
