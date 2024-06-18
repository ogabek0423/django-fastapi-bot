import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

# Turli tugmalar uchun CallbackData-obyektlarni yaratib olamiz
menu_cd = CallbackData("show_menu", "level", "category", "item_id")
buy_item = CallbackData("buy", "item_id")


# Quyidagi funksiya yordamida menyudagi har bir element uchun calbback data yaratib olinadi
# Agar mahsulot kategoriyasi va id raqami berilmagan bo'lsa 0 ga teng bo'ladi
def make_callback_data(level, category="0", item_id="0"):
    return menu_cd.new(
        level=level, category=category, item_id=item_id
    )


# Bizning menu 3 qavat (LEVEL) dan iborat
# 0 - Kategoriyalar
# 1 - Mahsulotlar
# 2 - Yagona mahsulot


# Kategoriyalar uchun keyboard yasab olamiz
async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await db.get_categories()

    for category in categories:
        number_of_items = await db.count_products(category["id"])
        button_text = f"{category['name']} ({number_of_items} dona)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category["id"])
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    return markup


# Berilgan kategoriya ostidagi mahsulotlarni qaytaruvchi keyboard
async def items_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    products = await db.get_products(category)

    for product in products:
        button_text = f"{product['name']} - ${product['price']}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category, item_id=product["id"])
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


# Berilgan mahsulot uchun Xarid qilish va Ortga yozuvlarini chiqaruvchi tugma keyboard
def item_keyboard(category, item_id):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text=f"🛒 Xarid qilish", callback_data=buy_item.new(item_id=item_id)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category)
        )
    )
    return markup