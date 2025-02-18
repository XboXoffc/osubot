from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
import requests
import sqlite3
from commands.osu import osuapi, recent, init

OSU_ID = config.OSU_CLIENT_ID
OSU_SECRET = config.OSU_CLIENT_SECRET
X_API_VERSION = config.X_API_VERSION
OSU_USERS_DB = config.OSU_USERS_DB
OSU_SKIN_PATH = config.OSU_SKIN_PATH
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

osu_api = osuapi.Osu(OSU_ID, OSU_SECRET, X_API_VERSION)

async def main(call):
    datasplit = call.data.split('@')
    if datasplit[0] in ['osu_skin_view']:
        userid = call.message.caption.split('\n')[0][1:]
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = """ SELECT osu_users.id, osu_skins.tg_id, osu_skins.file_name 
                        FROM osu_skins JOIN osu_users 
                        ON osu_skins.tg_id = osu_users.tg_id """
            cursor.execute(query)
            for user_skin in cursor.fetchall():
                if str(user_skin[0]) == userid:
                    with open(f'{OSU_SKIN_PATH}{user_skin[2]}', 'rb') as file:
                        await bot.send_document(call.message.chat.id, file, call.message.id, f'''@{call.from_user.username},\nIt's his skin''')
                    msg_sent = True
                    break
            if 'msg_sent' not in locals():
                await bot.reply_to(call.message, "ERROR: he didn't added skin")
                
    elif datasplit[0] in ['osu_recent_prev', 'osu_recent_next']:
        offset = int(datasplit[1])
        if datasplit[0] == 'osu_recent_prev':
            offset = str(offset+1)
        elif datasplit[0] == 'osu_recent_next':
            offset = str(offset-1)
        all_modes = ['std', 'osu', 'm', 'mania', 't', 'taiko', 'c', 'ctb', 'catch', 'fruits']
        msgsplit = call.message.reply_to_message.text.split(' ')
        msgsplit.pop(0)
        for i in range(3):
            msgsplit.append('$empty$')
        await recent.main(call.message.reply_to_message, msgsplit, all_modes, offset=offset, isinline=True, delmsgid=call.message.id, delchatid=call.message.chat.id)