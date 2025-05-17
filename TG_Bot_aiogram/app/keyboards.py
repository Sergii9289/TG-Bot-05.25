from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from app.utils import talk_person

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Випадковий факт", callback_data="random")],
    [InlineKeyboardButton(text="ChatGPT інтерфейс", callback_data="gpt")],
    [InlineKeyboardButton(text="Діалог з відомою особистістю", callback_data="talk")],
    [InlineKeyboardButton(text="Вікторина", callback_data="quiz")],
    [InlineKeyboardButton(text="Перекладач", callback_data="translate")],
])

# ----------------------------------talk------------------------------------------
personalities = talk_person()

# Отримуємо список кнопок talk
buttons = [
    [InlineKeyboardButton(text=name, callback_data=name)]
    for name, prompt in personalities.items()
]

# Передаємо список кнопок у клавіатуру
talk_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

# ------------------------------------quiz-------------------------------------------------
# Отримуємо список кнопок quiz
quiz_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Наука", callback_data="quiz_handler:наука"),
    InlineKeyboardButton(text="Техніка", callback_data="quiz_handler:техніка"),
    InlineKeyboardButton(text="Космос", callback_data="quiz_handler:космос"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])


# -------------------------------------translate------------------------------------------------

# Отримуємо список кнопок translate
translate_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="English", callback_data="translate_handler:english"),
    InlineKeyboardButton(text="Spain", callback_data="translate_handler:spain"),
    InlineKeyboardButton(text="Deutsch", callback_data="translate_handler:deutsch"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])

# ----------------------------------------------------------------------------------------------

random_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу ще факт", callback_data="random"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])

gpt_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу ще спитати", callback_data="gpt_next"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])

quiz_next_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Хочу ще спитати", callback_data="quiz"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])

translate_next_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Перекласти ще...", callback_data="translate"),
     InlineKeyboardButton(text="Закінчити", callback_data="menu")]
])



