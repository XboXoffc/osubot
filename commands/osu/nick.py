from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
import sqlite3
from commands.other import isempty

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api):
    response = None
    osu_mode = None
    if msgsplit[-1] in all_modes:
        osu_mode = msgsplit[-1]
        msgsplit.pop(-1)
        
    if not isempty(msgsplit, 1):
        osu_username = '_'.join(msgsplit[1:])
        response = await osu_api.profile(osu_username)
    else:
        await bot.reply_to(message, "ERROR: write username `\nsu nick <your username>`", parse_mode='MARKDOWN')

    if 'error' not in response:
        osu_mode = response['playmode']
    else:
        await bot.reply_to(message, "ERROR: username is not exists")

    if osu_mode != None:
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            osu_id = response['id']
            tg_id = message.from_user.id
            tg_username = message.from_user.username
            query = f""" REPLACE INTO osu_users (tg_id, tg_username, osu_id, osu_username, osu_mode) VALUES({tg_id}, '{tg_username}', {osu_id}, '{osu_username}', '{osu_mode}') """
            cursor.execute(query)
        await bot.reply_to(message, f'your username set, *{osu_username}*\nmode: *{osu_mode}*', parse_mode='MARKDOWN')