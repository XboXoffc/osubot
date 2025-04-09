from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import sqlite3

OSU_GROUPS_DB = config.OSU_GROUPS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes):
    all_sorts = ['-pp', '-rank', '-acc', '-pc', ]
    osumode = "osu"
    sortby = "osu_pp"
    tg_chat_id = str(message.chat.id)
    tg_chat_id = tg_chat_id.replace('-', '')
    table_name = "ID" + tg_chat_id

    sortby = next((m for m in msgsplit if m in set(all_sorts)), sortby)
    if sortby in ('-pp'):
        sortby = 'osu_pp'
    elif sortby in ('-rank'):
        sortby = 'osu_rank'
    elif sortby in ('-acc'):
        sortby = 'osu_acc'
    elif sortby in ('-pc'):
        sortby = 'osu_playcount'

    osumode = next((m for m in msgsplit if m in set(all_modes)), osumode)
    if osumode in ("-std", '-osu'):
        osumode = 'osu'
    elif osumode in ('-m', '-mania'):
        osumode = 'mania'
    elif osumode in ('-t', '-taiko'):
        osumode = 'taiko'
    elif osumode in ('-c' or '-ctb' or '-catch'):
        osumode = 'fruits'

    with sqlite3.connect(OSU_GROUPS_DB) as db:
        cursor = db.cursor()
        query = f""" SELECT * FROM {table_name} WHERE osu_mode='{osumode}' ORDER BY {sortby} """
        cursor.execute(query)
        MembersTop = cursor.fetchall()
    
    print(MembersTop)
    





