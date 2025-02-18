from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
import sqlite3
from commands.osu import osuapi

OSU_ID = config.OSU_CLIENT_ID
OSU_SECRET = config.OSU_CLIENT_SECRET
X_API_VERSION = config.X_API_VERSION
OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

osu_api = osuapi.Osu(OSU_ID, OSU_SECRET, X_API_VERSION)

async def main(message, msgsplit, all_modes):
    if msgsplit[1] != '$empty$':
        osu_username = msgsplit[1]
        response = osu_api.profile(osu_username).json()
    else:
        await bot.reply_to(message, "ERROR: write username `\nsu nick <your username>`", parse_mode='MARKDOWN')

    if msgsplit[2] != '$empty$' and msgsplit[2] in all_modes:
        osu_mode = msgsplit[2]
    else:
        osu_mode = response['playmode']

    try:
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            osu_id = response['id']
            tg_id = message.from_user.id
            tg_username = message.from_user.username
            query = f""" REPLACE INTO osu_users (tg_id, tg_username, osu_id, osu_username, osu_mode) VALUES({tg_id}, '{tg_username}', {osu_id}, '{osu_username}', '{osu_mode}') """
            cursor.execute(query)
        await bot.reply_to(message, f'your username set, *{osu_username}*\nmode: *{osu_mode}*', parse_mode='MARKDOWN')
    except:
        await bot.reply_to(message, "ERROR: username is not exists")