def build_settings_text(
    auto_buy_current_status: bool,
    min_price: int,
    max_price: int,
    supply_limit: int,
    cycles: int
) -> str:
    return (
        f"⚙️ <b>Настройки</b>\n"
        f"\n"
        f"🤖 <b>Автопокупка</b>\n"
        f"  └─ {'работает' if auto_buy_current_status else 'не работает'}\n"
        f"\n"
        f"💰 <b>Лимит цены</b>\n"
        f"  └─ От {min_price} до {max_price} ⭐️\n"
        f"\n"
        f"💎 <b>Лимит саплая</b>\n"
        f"  └─ {supply_limit}\n"
        f"\n"
        f"🔄 <b>Количество циклов</b>\n"
        f"  └─ {cycles}\n"
    )
