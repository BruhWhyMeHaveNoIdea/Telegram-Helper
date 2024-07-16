from aiogram import Bot
from bot.tools.plugins.config import config

bot = Bot(token=config["bot_token"])
