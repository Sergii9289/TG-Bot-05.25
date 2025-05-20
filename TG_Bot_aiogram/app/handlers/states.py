from aiogram.fsm.state import State, StatesGroup


class QuizState(StatesGroup):
    waiting_for_answer_quiz = State()


class GptState(StatesGroup):
    waiting_for_answer_gpt = State()


class TranslateState(StatesGroup):
    waiting_for_text = State()


class VoiceInputState(StatesGroup):
    waiting_for_voice = State()
