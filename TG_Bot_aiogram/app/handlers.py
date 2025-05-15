from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile, ForceReply
from aiogram.filters import CommandStart

import app.keyboards as kb
import app.database.requests as rq
import app.text as textfile
from gpt import chat_gpt_service
from app.utils import random_fact, talk_person

router = Router()

talk_with_pers = {}

@router.callback_query(F.data == "random")
async def random_ai(callback: CallbackQuery):
    await callback.answer()  # Підтверджуємо натискання кнопки
    prompt = "Ти AI-асистент, що надає випадкові цікаві факти користувачам."
    fact_prompt = random_fact()  # Генерація промпту для факту
    image = FSInputFile('app/resources/images/random_logo.png')
    # Надсилаємо зображення та повідомлення перед запитом до AI
    await callback.message.answer_photo(photo=image, caption=f"Ось випадковий факт:\n{fact_prompt}")
    # Запит до GPT
    fact = await chat_gpt_service.send_question(prompt, fact_prompt)
    # Надсилаємо відповідь користувачу
    await callback.message.answer(fact)

    await callback.message.answer('Що хочеш зробити далі?', reply_markup=kb.random_menu)


@router.callback_query(F.data == "gpt")
async def chat_gpt_interface(callback: CallbackQuery):
    await callback.answer()  # Підтверджуємо натискання кнопки
    global talk_with_pers
    talk_with_pers = {}
    image = FSInputFile('app/resources/images/gpt_logo.png')  # Підготовлене зображення
    # Надсилаємо зображення
    await callback.message.answer_photo(photo=image, caption="Запит до ChatGPT...")
    await callback.message.answer("Введіть ваше повідомлення для ChatGPT або stop:", reply_markup=ForceReply())


@router.callback_query(F.data == "gpt_next")
async def chat_gpt_interface_next(callback: CallbackQuery):
    await callback.answer()  # Підтверджуємо натискання кнопки
    await callback.message.answer("Введіть ваше повідомлення для ChatGPT або stop:", reply_markup=ForceReply())


@router.message(F.reply_to_message)
async def process_user_message(message: Message):
    # Переконуємось, що повідомлення є відповіддю на запит "Введіть ваше повідомлення..."
    if not message.reply_to_message or "Введіть ваше повідомлення для ChatGPT або stop:" not in message.reply_to_message.text:
        return  # Ігноруємо повідомлення, що не є відповіддю на наш запит

    user_message = message.text.strip().lower()  # Очищаємо текст від пробілів і робимо нечутливим до регістру

    if user_message == "stop":
        await message.answer("Повертаємось в головне меню...", reply_markup=kb.menu)
    else:
        prompt = talk_with_pers.get('prompt', "Ти AI-асистент, який відповідає на запити користувачів.")
        print(f'Prompt is: {prompt}')
        response = await chat_gpt_service.send_question(prompt, user_message)
        await message.answer(response)
        await message.answer('Що хочеш зробити далі?', reply_markup=kb.gpt_menu)


@router.callback_query(F.data == "talk")
async def talk(callback: CallbackQuery):
    await callback.answer()  # Підтверджуємо натискання кнопки
    image = FSInputFile('app/resources/images/talk_logo.png')  # Підготовлене зображення
    # Надсилаємо зображення
    await callback.message.answer_photo(photo=image)
    await callback.message.answer('Оберіть з ким спілкуватись:', reply_markup=kb.talk_keyboard)


@router.message(CommandStart())  # перша функція після входу в бот /start
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)  # передаємо user.id для перевірки існування user
    await message.answer(textfile.greet.format(name=message.from_user.full_name),
                         reply_markup=kb.menu)


@router.callback_query(F.data == "menu")
async def menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Оберіть дію:", reply_markup=kb.menu)


@router.callback_query()
async def process_personality_selection(callback: CallbackQuery):
    personalities = talk_person()
    name = callback.data
    prompt = personalities.get(name)
    global talk_with_pers
    talk_with_pers['prompt'] = prompt

    await callback.message.answer(f"Ви обрали: {name}\n\n{prompt}")
    await callback.message.answer("Введіть ваше повідомлення для ChatGPT або stop:", reply_markup=ForceReply())
