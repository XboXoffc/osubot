from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import sqlite3
from commands.osu.groups import templates
from commands.osu.fetch import mode as modefetch
from commands.osu.fetch import sort as sortfetch


OSU_GROUPS_DB = config.OSU_GROUPS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes):
    all_sorts = ['-pp', '-rank', '-acc', '-pc', '-ts', '-ii']
    MembersTop = None
    limit = 15
    osumode = "osu"
    sortby = "osu_pp"
    tg_chat_id = str(message.chat.id)
    tg_chat_id = tg_chat_id.replace('-', '')
    table_name = "ID" + tg_chat_id

    sortby = sortfetch(sortby, msgsplit, all_sorts)
    osumode = modefetch(osumode, msgsplit, all_modes)
    with sqlite3.connect(OSU_GROUPS_DB) as db:
        cursor = db.cursor()
        query = f""" SELECT * FROM {table_name} WHERE osu_mode='{osumode}' ORDER BY {sortby} DESC NULLS LAST"""
        cursor.execute(query)
        MembersTop = cursor.fetchall()
    
    if MembersTop != None:
        text = await templates.grouptop(message, MembersTop, limit, osumode, sortby.replace('osu_', ''))
        await bot.reply_to(message, text, parse_mode="MARKDOWN", link_preview_options=types.LinkPreviewOptions(True))
    elif MembersTop == None:
        await bot.reply_to(message, "ERROR: no result in sql for any reason")
    





