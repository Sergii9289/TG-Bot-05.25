from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart


import app.keyboards as kb
import app.database.requests as rq
import app.text as textfile
from app.main_API import PrivatAPI, MonoAPI

router = Router()


@router.message(CommandStart())  # перша функція після входу в бот /start
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)  # передаємо user.id для перевірки існування user
    await message.answer(textfile.greet.format(name=message.from_user.full_name),
                         reply_markup=kb.menu)


@router.message(F.text == "меню")
async def menu(message: Message):
    await message.answer(textfile.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "privat")
async def privat_info(callback: CallbackQuery):
    await callback.message.answer('Оберіть валюту:', reply_markup=kb.privat_menu)


@router.callback_query(F.data == "mono")
async def mono_info(callback: CallbackQuery):
    await callback.message.answer('Оберіть валюту:', reply_markup=kb.mono_menu)


@router.callback_query(F.data == "privat_USD")
async def privat_cur_usd(callback: CallbackQuery):
    curr_privat = PrivatAPI('PrivatBank', '', 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
    exchange_data = await curr_privat.get_currency('USD', 'UAH')

    if exchange_data:
        await callback.message.answer(f'Курс валют: {exchange_data}')
    else:
        await callback.message.answer("Не вдалося отримати курс валют.")
    await callback.answer()  # Закриваємо "вантаження" кнопки


@router.callback_query(F.data == "privat_EUR")
async def privat_cur_eur(callback: CallbackQuery):
    curr_privat = PrivatAPI('PrivatBank', '', 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
    exchange_data = await curr_privat.get_currency('EUR', 'UAH')

    if exchange_data:
        await callback.message.answer(f'Курс валют: {exchange_data}')
    else:
        await callback.message.answer("Не вдалося отримати курс валют.")
    await callback.answer()  # Закриваємо "вантаження" кнопки

@router.callback_query(F.data == "mono_EUR")
async def mono_cur_eur(callback: CallbackQuery):
    curr_mono = MonoAPI('Monobank', '', 'https://api.monobank.ua/bank/currency')
    exchange_data = await curr_mono.get_currency('EUR', 'UAH')

    if exchange_data:
        await callback.message.answer(f'Курс валют: {exchange_data}')
    else:
        await callback.message.answer("Не вдалося отримати курс валют.")
    await callback.answer()  # Закриваємо "вантаження" кнопки

@router.callback_query(F.data == "mono_USD")
async def mono_cur_usd(callback: CallbackQuery):
    curr_mono = MonoAPI('Monobank', '', 'https://api.monobank.ua/bank/currency')
    exchange_data = await curr_mono.get_currency('USD', 'UAH')

    if exchange_data:
        await callback.message.answer(f'Курс валют: {exchange_data}')
    else:
        await callback.message.answer("Не вдалося отримати курс валют.")
    await callback.answer()  # Закриваємо "вантаження" кнопки