from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .settings import SettingsSchema, SettingsCreateSchema, SettingsUpdateSchema


class UserSchema(BaseModel):
    id: int
    user_id: int
    fullname: str
    username: Optional[str]
    type: str
    register_at: datetime
    balance: int
    settings: SettingsSchema


class UserCreateSchema(BaseModel):
    user_id: int
    fullname: str
    username: Optional[str] = None
    type: Optional[str] = "user"
    balance: int = 0


class UserUpdateSchema(BaseModel):
    fullname: Optional[str] = None
    username: Optional[str] = None
    type: Optional[str] = None
    balance: Optional[int] = None
