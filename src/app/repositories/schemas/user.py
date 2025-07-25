from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserSettingsSchema(BaseModel):
    auto_buy: bool = False
    price_min: int = 0
    price_max: int = 0
    supply_limit: int = 0
    cycles: int = 0
    quantity: int = 0

class UserSettingsUpdateSchema(BaseModel):
    auto_buy: Optional[bool] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    supply_limit: Optional[int] = None
    cycles: Optional[int] = None
    quantity: Optional[int] = None


class UserSchema(BaseModel):
    id: int
    user_id: int
    fullname: str
    username: Optional[str]
    type: str
    register_at: datetime
    balance: int
    settings: UserSettingsSchema


class UserCreateSchema(BaseModel):
    user_id: int
    fullname: str
    username: Optional[str] = None
    type: Optional[str] = "user"
    balance: int = 0
    settings: Optional["UserSettingsSchema"] = None


class UserUpdateSchema(BaseModel):
    fullname: Optional[str] = None
    username: Optional[str] = None
    type: Optional[str] = None
    balance: Optional[int] = None
    settings: Optional[UserSettingsSchema] = None
