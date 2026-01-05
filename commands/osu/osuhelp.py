from telebot.async_telebot import AsyncTeleBot
import asyncio
import config

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit):
    text = """
osu!bot commands: https://telegra.ph/osubot-by-xbox-in-tgXboXoffcBot-01-05
    """
    await bot.reply_to(message, text, parse_mode='MARKDOWN')