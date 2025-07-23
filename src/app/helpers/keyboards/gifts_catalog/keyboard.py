from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, Gift
from typing import List

from app.helpers.fabric.gift import GiftCallback


def gift_catalog_keyboard(gifts: List[Gift]):
    builder = InlineKeyboardBuilder()
    
    for gift in gifts:
        price = gift.star_count
        total = gift.total_count
        remaining = gift.remaining_count
        count = f"[{total}/{remaining}]" if total else '∞'

        # !!! ЦЕНА В CALLBACK ЧЕРЕЗ ДЕФИС value=gift_id-PRICE
        builder.row(InlineKeyboardButton(text=f"{gift.sticker.emoji} — {price} ⭐️ {count}", callback_data=GiftCallback(action="buy_gift", value=f"{gift.id}-{gift.star_count}").pack()))

    return builder.as_markup(resize_keyboard=True)
