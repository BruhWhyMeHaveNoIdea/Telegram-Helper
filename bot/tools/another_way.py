import requests
from bot.tools.plugins.gpt_config import gpt_config
import logging
import openai

# Ваш API-ключ OpenAI


async def ask_gpt(question):
    openai.api_key = gpt_config['api_key']
    message = [
        {'role': 'system', 'content': 'You are an assistant'},
        {'role': 'user', 'content': question}
        ]
    print('fffff', message, openai.api_key)
    response = openai.chat.completions.create(
        model=gpt_config['model']
        , messages=message
        , temperature=gpt_config['temperature']
    )
    print('fffff', message, response, openai.api_key)
    return response.choices[0].message['content']
