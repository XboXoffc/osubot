from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import sqlite3
from commands.osu.groups import template

OSU_GROUPS_DB = config.OSU_GROUPS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes):
    all_sorts = ['-pp', '-rank', '-acc', '-pc', '-ts']
    MembersTop = None
    limit = 15
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
    elif sortby in ('-ts'):
        sortby = 'osu_topscore'

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
        query = f""" SELECT * FROM {table_name} WHERE osu_mode='{osumode}' ORDER BY {sortby} DESC NULLS LAST"""
        cursor.execute(query)
        MembersTop = cursor.fetchall()
    
    if MembersTop != None:
        text = await template.main(message, MembersTop, limit, osumode, sortby.replace('osu_', ''))
        await bot.reply_to(message, text, parse_mode="MARKDOWN", link_preview_options=types.LinkPreviewOptions(True))
    elif MembersTop == None:
        await bot.reply_to(message, "ERROR: no result in sql for any reason")
    





