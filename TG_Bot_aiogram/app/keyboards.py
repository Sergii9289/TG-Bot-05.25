from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from app.utils import talk_person

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Випадковий факт", callback_data="random")],
    [InlineKeyboardButton(text="ChatGPT інтерфейс", callback_data="gpt")],
    [InlineKeyboardButton(text="Діалог з відомою особистістю", callback_data="talk")],
    [InlineKeyboardButton(text="Головне меню", callback_data="menu")]
])

# ----------------------------------------------------------------------------
personalities = talk_person()

# Отримуємо список кнопок
buttons = [
    [InlineKeyboardButton(text=name, callback_data=name)]
    for name, prompt in personalities.items()
]

# Передаємо список кнопок у клавіатуру
talk_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

# -------------------------------------------------------------------------------------

random_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу ще факт", callback_data="random"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])

gpt_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу ще спитати", callback_data="gpt_next"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])

# personalities = talk_person()
#
# talk_keyboard = InlineKeyboardMarkup()
# for name in personalities.keys():
#     talk_keyboard.add(InlineKeyboardButton(text=name, callback_data=name.lower().replace(" ", "_")))

