from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
import requests
import sqlite3
from commands.osu import init, topscores
from commands.osu.recent import recent, recentbest

OSU_USERS_DB = config.OSU_USERS_DB
OSU_SKIN_PATH = config.OSU_SKIN_PATH
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

all_modes = init.all_modes

async def main(call, osu_api):
    datasplit = call.data.split('@')
    if datasplit[0] in ['osu_skin_view']:
        issend = False
        skinid = datasplit[1]
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = """ SELECT osu_users.id, osu_skins.tg_id, osu_skins.file_name 
                        FROM osu_skins JOIN osu_users 
                        ON osu_skins.tg_id = osu_users.tg_id """
            cursor.execute(query)
            for user_skin in cursor.fetchall():
                if str(user_skin[0]) == skinid:
                    tempmsg = await bot.reply_to(call.message, 'Skin is uploading...')
                    with open(f'{OSU_SKIN_PATH}{user_skin[2]}', 'rb') as file:
                        await bot.send_document(call.message.chat.id, file, call.message.id, f'''@{call.from_user.username}, It's his skin''')
                        await bot.delete_message(tempmsg.chat.id, tempmsg.id)
                    issend = True
                    break
            if not issend:
                await bot.reply_to(call.message, "ERROR: he didn't added skin")
                
    elif datasplit[0] in ['osu_recent_prev', 'osu_recent_next', 'osu_recent_update'] and call.message.reply_to_message:
        if call.from_user.id == call.message.reply_to_message.from_user.id:
            offset = int(datasplit[1])
            if datasplit[0] == 'osu_recent_prev':
                offset = str(offset+1)
            elif datasplit[0] == 'osu_recent_next':
                offset = str(offset-1)

            msgsplit = call.message.reply_to_message.text.split(' ')
            msgsplit.pop(0)
            for i in range(3):
                msgsplit.append('$empty$')

            if datasplit[4] == '0':
                await recent.main(call.message.reply_to_message, msgsplit, all_modes, osu_api, offset=offset, isinline=True, botcall=call, osuid=datasplit[2], osumode=datasplit[3])
            elif datasplit[4] == '1':
                await recentbest.main(call.message.reply_to_message, msgsplit, all_modes, osu_api, offset=offset, isinline=True, botcall=call, osuid=datasplit[2], osumode=datasplit[3])
        else:
            await bot.answer_callback_query(call.id, '''you can't change offset here, you can change only own recent''')

    elif datasplit[0] in ['osu_topscores_update', 'osu_topscores_prev', 'osu_topscores_next'] and call.message.reply_to_message:
        page = int(datasplit[1])
        limit = int(datasplit[2])
        if datasplit[0] == 'osu_topscores_prev':
            page -= 1
        elif datasplit[0] == 'osu_topscores_next':
            page += 1

        msgsplit = call.message.reply_to_message.text.split(' ')
        msgsplit.pop(0)
        for i in range(3):
            msgsplit.append('$empty$')
        
        await topscores.main(call.message.reply_to_message, msgsplit, all_modes, osu_api, isinline=True, limit=limit, page=page, botcall=call, osuid=datasplit[3], osumode=datasplit[4])
    
    elif datasplit[0] in ['osu_del']:
        await bot.delete_message(call.message.chat.id, call.message.id)
