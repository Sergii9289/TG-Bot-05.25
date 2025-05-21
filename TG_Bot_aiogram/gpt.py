from dotenv import load_dotenv
import os
import base64
import openai
import httpx
from openai import OpenAIError
from app.logger import log_to_file


load_dotenv(dotenv_path='config.env')
TG_TOKEN = os.getenv('TG_TOKEN')
AI_TOKEN = os.getenv('AI_TOKEN')


class ChatGptService:
    def __init__(self, token):
        self._client = openai.OpenAI(
            api_key=AI_TOKEN, http_client=httpx.Client(proxy="http://18.199.183.77:49232")
        )
        self.message_list = []

    async def send_question(self, prompt_text: str, message_text: str) -> str:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})
        self.message_list.append({"role": "user", "content": message_text})

        try:
            completion = self._client.chat.completions.create(
                model="gpt-4o", messages=self.message_list, max_tokens=200, temperature=0.7
            )
            log_to_file('ChatGptService.send_question')  # Логуємо виклик функції
            return completion.choices[0].message.content
        except OpenAIError as e:
            log_to_file('ChatGptService.send_question', str(e))  # Логуємо помилку
            print(f'Error in: {self.send_question.__name__}. Error is: {e}')

    async def send_question_with_image(self, prompt_text: str, message_text: str, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")  # Кодую у Base64

        completion = self._client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": message_text},
                {"role": "user", "content": f"![Image](data:image/jpeg;base64,{encoded_image})"}
                # Передача зображення у правильному форматі
            ],
            max_tokens=300,
            temperature=0.9
        )

        return completion.choices[0].message.content


# Ініціалізація GPT сервісу
chat_gpt_service = ChatGptService(AI_TOKEN)
