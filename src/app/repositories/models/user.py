__all__ = ["User"]

import datetime
from functools import partial

from sqlalchemy import Column, Integer, String, DateTime, Index, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import expression

from .base import Base
from .dataclasses import UserType

from ..schemas.user import UserSchema


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    # Telegram-related
    user_id = Column(BigInteger, unique=True)
    fullname = Column(String(64), nullable=False)
    username = Column(String(64), unique=True, nullable=True)

    # Role & metadata
    type = Column(String(32), default=UserType.USER, nullable=False)
    register_at = Column(DateTime, default=partial(
        datetime.datetime.utcnow), nullable=False)

    # App-specific
    balance = Column(Integer, default=0, nullable=False)
    settings = Column(
        MutableDict.as_mutable(JSONB),
        server_default=expression.text("'{}'::jsonb"),
        nullable=False,
        default={
            "auto_buy": False,
            "price_min": 15,
            "price_max": 100,
            "supply_limit": 100000,
            "cycles": 1,
            "quantity": 1,
        }
    )

    __table_args__ = (
        Index("ix_users_user_id", "user_id"),
    )

    def to_schema(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            user_id=self.user_id,
            fullname=self.fullname,
            username=self.username,
            type=self.type,
            register_at=self.register_at,
            balance=self.balance,
            settings=self.settings
        )

    @property
    def is_admin(self) -> bool:
        return self.type == UserType.ADMIN
