from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from commands import other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    text = """
*Hello*
My commands:
/about
/osu or just "su"
/weather (city)(-a, -p)
Check my github for docs in /about
"""
    try:
        await bot.send_message(message.chat.id, text, "MARKDOWN")
    except:
        await bot.send_message(message.chat.id, text)

print("Cogs | start.py is ready")