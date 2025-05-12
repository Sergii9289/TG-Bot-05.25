from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

menu = [
    [InlineKeyboardButton(text="Курс валют PrivatBank", callback_data="privat"),
     InlineKeyboardButton(text="Курс валют MonoBank", callback_data="mono")],
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)

privat_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Курс EUR > UAH Приват Банк", callback_data="privat_EUR"),
     InlineKeyboardButton(text="Курс USD > UAH Приват Банк", callback_data="privat_USD")]
])

mono_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Курс EUR > UAH Monobank", callback_data="mono_EUR"),
     InlineKeyboardButton(text="Курс USD > UAH Monobank", callback_data="mono_USD")]
])

