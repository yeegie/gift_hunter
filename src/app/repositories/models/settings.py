__all__ = ["Settings"]

from sqlalchemy import Column, Integer, String, Index, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.repositories.schemas.settings import SettingsSchema

from .base import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    auto_buy = Column(Integer, default=False)
    price_min = Column(Integer, default=15)
    price_max = Column(Integer, default=100)
    supply_limit = Column(Integer, default=500000)
    cycles = Column(Integer, default=1)
    quantity = Column(Integer, default=1)

    user_id = Column(BigInteger, ForeignKey("users.user_id"), unique=True, nullable=False)
    user = relationship("User", back_populates="settings")

    def to_schema(self) -> SettingsSchema:
        return SettingsSchema(
            user_id=self.user_id,
            auto_buy=self.auto_buy,
            price_min=self.price_min,
            price_max=self.price_max,
            supply_limit=self.supply_limit,
            cycles=self.cycles,
            quantity=self.quantity,
        )
