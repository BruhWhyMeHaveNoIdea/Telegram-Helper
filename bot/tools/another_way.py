import openai
from bot.tools.plugins.gpt_config import gpt_config


async def ask_question(question: str):
    client = openai.AsyncOpenAI(api_key=gpt_config["api_key"])
    responce = await client.chat.completions.create(
        model=gpt_config["model"],
        messages = [
            {"role": "system", "content": f"Ты хороший помощник. На все вопросы отвечай на русском"},
            {"role": "user", "content": f"{question}"}
        ]
    )
    return responce.choices[0].message.content, responce.usage.total_tokens

