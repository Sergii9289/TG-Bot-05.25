from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
import app.database.requests as rq
import app.text as textfile

router = Router()  # Оголошуємо router в цьому файлі

@router.message(CommandStart())  # перша функція після входу в бот /start
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)  # Передаємо user.id для перевірки існування user
    await message.answer(textfile.greet.format(name=message.from_user.full_name),
                         reply_markup=kb.menu)

@router.callback_query(F.data == "menu")
async def menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Оберіть дію:", reply_markup=kb.menu)