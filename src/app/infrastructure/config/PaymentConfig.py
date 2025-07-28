__all__ = [
    "PaymentConfig"
]


from pydantic import BaseModel


class PaymentConfig(BaseModel):
    enabled: bool = False
    deposit_commission: float = 0.0
    withdrawal_commission: float = 0.0
