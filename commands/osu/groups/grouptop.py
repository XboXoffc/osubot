from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import sqlite3

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main():
    pass