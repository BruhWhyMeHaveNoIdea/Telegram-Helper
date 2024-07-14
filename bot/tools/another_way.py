import openai
from bot.tools.plugins.gpt_config import gpt_config


async def ask_question(question: str):
    proxy = {
        'https': 'gmo6lq:iMXI0NWN4k@94.158.190.191:1050',
        'http': 'gmo6lq:iMXI0NWN4k@94.158.190.191:1050'
    }
    client = openai.AsyncOpenAI(api_key=gpt_config["api_key"], base_url=proxy.get('https'))
    responce = await client.chat.completions.create(
        model=gpt_config["model"],
        messages = [
            {"role": "system", "content": f"Ты хороший помощник. На все вопросы отвечай на русском"},
            {"role": "user", "content": f"{question}"}
        ]
    )
    print('хуйпизда', responce.choices[0].message.content, responce.usage.total_tokens)
    return responce.choices[0].message.content, responce.usage.total_tokens

