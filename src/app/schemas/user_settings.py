from pydantic import BaseModel


class UserSettings(BaseModel):
    price_min: int
    price_max: int
    supply_limit: int
    cycles: int
    quantity: int
