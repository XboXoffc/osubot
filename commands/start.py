from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from commands import other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    text = """
*Hello*,
It's my bot for osu!
osu! commands here: /osu
just weather: /weather <city> (-a)
and you can support me, in future updates I add you in credits: /support
there is all about bot and me /about
"""
    try:
        await bot.send_message(message.chat.id, text, "MARKDOWN")
    except:
        await bot.send_message(message.chat.id, text)

print("Cogs | start.py is ready")