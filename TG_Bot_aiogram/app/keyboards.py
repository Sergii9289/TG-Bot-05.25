from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

menu = [
    [InlineKeyboardButton(text="Рандомне повідомлення", callback_data="random"),
     InlineKeyboardButton(text="Головне меню", callback_data="menu")],
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)

random_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу ще факт", callback_data="random"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])