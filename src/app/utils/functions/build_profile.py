from app.repositories.schemas.user import UserSchema


def build_profile_text(user: UserSchema) -> str:
    return (
        f"👤 <b>Профиль</b>\n"
        f"\n"
        f"<b>{user.fullname}</b>\n"
        f"⭐️ {user.balance}\n"
        f"🕜 Дата регистрации: {user.register_at}\n"
    )
