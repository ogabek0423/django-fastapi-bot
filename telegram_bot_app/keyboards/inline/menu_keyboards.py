import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db

# CallbackData objects for different buttons
menu_cd = CallbackData("show_menu", "level", "category", "item_id")
buy_item = CallbackData("buy", "item_id")

# Generate callback data for menu items
def make_callback_data(level, category="0", item_id="0"):
    return menu_cd.new(level=level, category=category, item_id=item_id)

# Keyboard for categories
async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await db.get_categories()

    for category in categories:
        category_id = category['id']
        number_of_items = await db.count_products(category_id)
        button_text = f"{category['name']} ({number_of_items} dona)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category_id)
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    return markup

# Keyboard for items in a given category
async def items_keyboard(category_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    products = await db.get_products(category_id)

    for product in products:
        button_text = f"{product['name']} - ${product['price']}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category_id, item_id=product["id"])
        markup.insert(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup

# Keyboard for a single product with options to buy or go back
def item_keyboard(category_id, item_id):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="🛒 Xarid qilish", callback_data=buy_item.new(item_id=item_id)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category_id)
        )
    )
    return markup
