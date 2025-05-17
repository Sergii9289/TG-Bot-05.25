import random
import openai
import gtts
from io import BytesIO

async def convert_text_to_speech(text):
    tts = gtts.gTTS(text, lang="uk")  # Синтезуємо українську мову
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)  # Переміщаємо курсор у початок

    return audio_file

async def convert_speech_to_text(voice_file):
    response = openai.Audio.transcriptions.create(
        file=voice_file,
        model="whisper-1"
    )
    return response["text"]



def random_fact():
    with open('app/resources/prompts/facts.txt', 'r', encoding='utf-8') as file:
        prompts = file.read().splitlines()
    return random.choice(prompts)  # Вибирає випадковий факт


def talk_person():
    prompts_dict = {}
    with open('app/resources/prompts/talk.txt', 'r', encoding='UTF_8') as file:
        for line in file:
            key_value = line.strip().split(' | ', maxsplit=1)
            if len(key_value) == 2:
                prompts_dict[key_value[0].strip()] = key_value[1].strip()
    return prompts_dict



def quiz_prompt(topic):
    with open('app/resources/prompts/quiz.txt', 'r', encoding='UTF_8') as file:
        for line in file:
            key, prompt = line.strip().split('|', maxsplit=1)
            if key == topic:
                print(prompt)
                return prompt
    return ('Створи цікаве запитання для квізу на довільну тему. '
            'Запитання має бути у форматі тесту або відкритої відповіді. '
            'Тема може бути будь-якою: історія, '
            'спорт, література, технології або щось нестандартне.')
