from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
import sqlite3

OSU_SKIN_PATH = config.OSU_SKIN_PATH
OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    try:
        text = ''
        ## for general db
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = """  CREATE TABLE IF NOT EXISTS osu_users(
                id INTEGER PRIMARY KEY UNIQUE,
                tg_id INTEGER UNIQUE,
                tg_username TEXT,
                osu_id INTEGER,
                osu_username TEXT,
                osu_mode TEXT
                )  """
            query1 = ''' REPLACE INTO osu_users(tg_id, tg_username, osu_id, osu_username, osu_mode) VALUES (-1, 'NONE', -1, 'NONE', 'NONE') '''
            cursor.execute(query)
            cursor.execute(query1)
            text = text + '\n1.general initialization succesful'
        ## for skins
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = """ CREATE TABLE IF NOT EXISTS osu_skins(
                tg_id INTEGER UNIQUE,
                file_name TEXT
                ) """
            query1 = """ REPLACE INTO osu_skins(tg_id, file_name) VALUES(-1, 'NONE') """
            cursor.execute(query)
            cursor.execute(query1)
            text = text + '\n2.skins initialization succesful'
        await bot.reply_to(message, text)
    except Exception as e:
        print(e)
