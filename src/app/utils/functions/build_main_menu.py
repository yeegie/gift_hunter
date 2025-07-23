__all__ = [
    "build_main_menu_text"
]


from app.repositories.schemas.user import UserSchema
import random


def build_main_menu_text(user: UserSchema) -> str:
    random_emoji = "⚙️ 🤖 💎 ⭐️ 🐍 🫡".split(' ')

    return (
        f"{random.choice(random_emoji)} <b>GiftHunter</b>\n"
        f"  └─ Авто-выкуп подарков\n"
        # f"\n"
        # f"🎁 <b>Выкуплено</b>\n"
        # f"  └─ {29}\n"
        f"\n"
        f"⭐️ <b>Баланс</b>\n"
        f"  └─ {user.balance}\n"
    )
