from bot.tools.plugins.config import config
import openai

# Ваш API-ключ OpenAI
openai.api_key = config['api_key']


async def ask_gpt(question):
    response = openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты хороший помощник. На все вопросы отвечай на русском"},
            {"role": "user", "content": question}
        ]
    )
    print(response)
    return response['choices'][0]['message']['content']


class AdvancedGPT:
    def __init__(self, config):
        self.api_key = config["api_key"]
        self.model = config['model']
        self.assistant_content = ""

    def ask_gpt(self, user: str):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты хороший помощник. На все вопросы отвечай на русском"},
                {"role": "user", "content": user},
                {"role": "assistant", "content": self.assistant_content}
            ]
        )
        return response['choices'][0]['message']['content']

    def add_assistant(self, text: str):
        self.assistant_content += text
