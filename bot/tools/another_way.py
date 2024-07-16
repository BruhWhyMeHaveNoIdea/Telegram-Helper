import requests
from bot.tools.plugins.config import config
import logging
import openai

# Ваш API-ключ OpenAI
openai.api_key = gpt_config['api_key']

async def ask_gpt(question):
    response = openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты хороший помощник. На все вопросы отвечай на русском"},
            {"role": "user", "content": question}
        ]
    )
    print(response)
    return None
