import requests
from bot.tools.plugins.gpt_config import gpt_config
import logging

# Ваш API-ключ OpenAI


async def ask_gpt(question):
    api_key = 'sk-proj-ZUTU7HWB6Tr10myx9nucT3BlbkFJRTcwSE3wLdfrpF4MDmrx'

    # Заголовки запроса
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Тело запроса
    data = {
        "model": gpt_config['model'],
        "prompt": "Hello, OpenAI!",
        "max_tokens": gpt_config['max_tokens']
    }

    # Отправка запроса
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    # Проверка статуса ответа
    if response.status_code == 200:
        logging.info("Получен ответ от GPT")
        print()
        return response.json()["choices"]["text"], response.json()["usage"]["total_tokens"]
    else:
        print("Произошла ошибка.")
        print("Статус код:", response.status_code)
        print("Ответ:", response.json())