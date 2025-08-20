import pytest
from unittest.mock import AsyncMock

from app.repositories.schemas.user import UserSchema
from app.repositories.schemas.settings import SettingsSchema

from app.services.user.user import UserService
from app.services.gift.infrastructure.observer import Observer


@pytest.fixture
def data():
    return [
        UserSchema(
            id=1,
            user_id=123123123,
            fullname="Egor",
            username=None,
            type="user",
            register_at="2023-10-01T12:00:00",
            balance=1000,
            settings=SettingsSchema(
                user_id=123123123,
                auto_buy=True,
                price_min=0,
                price_max=500,
                supply_limit=500000,
                cycles=1,
                quantity=1
            )
        ),
        UserSchema(
            id=2,
            user_id=987654321,
            fullname="Anna Ivanova",
            username="anna_ivanova",
            type="user",
            register_at="2024-01-15T09:30:00",
            balance=2500,
            settings=SettingsSchema(
                user_id=987654321,
                auto_buy=False,
                price_min=100,
                price_max=1000,
                supply_limit=1000000,
                cycles=2,
                quantity=5
            )
        ),
        UserSchema(
            id=3,
            user_id=555666777,
            fullname="Bot Service",
            username="bot_777",
            type="bot",
            register_at="2025-03-01T18:45:00",
            balance=0,
            settings=SettingsSchema(
                user_id=555666777,
                auto_buy=True,
                price_min=10,
                price_max=9999,
                supply_limit=999999,
                cycles=10,
                quantity=100
            )
        ),
    ]


@pytest.mark.asyncio
async def test_observer_initialize(data):
    fake_user_service = AsyncMock()
    fake_user_service.get_all_users_by_autobuy.return_value = data

    observer = Observer(user_service=fake_user_service)
    
    await observer.initialize()
    print(f"sub count: {observer.subscribers_count}")
    assert observer.subscribers_count == 0