from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import requests
import sqlite3

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api):
    text = ''
    osumode = ''
    username = None
    if message.reply_to_message:
        tg_id = message.reply_to_message.from_user.id
    elif not message.reply_to_message:
        tg_id = message.from_user.id

    if (msgsplit[1] not in all_modes) and (msgsplit[1] != '$empty$'):
        username = msgsplit[1]
    else:
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = """ SELECT tg_id, osu_username, id, osu_mode FROM osu_users """
            cursor.execute(query)
            users = cursor.fetchall()
            for i in users:
                if i[0] == tg_id:
                    username = i[1]
                    osumode = i[3]
                    skinid = i[2]
                    break
        if username != None:
            button_for_skin = types.InlineKeyboardButton(f'''{message.from_user.first_name}'s skin''', callback_data=f'osu_skin_view@{skinid}')

    osumode = next((m for m in msgsplit if m in set(all_modes)), osumode)
    if osumode in ("-std", '-osu'):
        osumode = 'osu'
    elif osumode in ('-m', '-mania'):
        osumode = 'mania'
    elif osumode in ('-t', '-taiko'):
        osumode = 'taiko'
    elif osumode in ('-c' or '-ctb' or '-catch'):
        osumode = 'fruits'

    if username != None:
        try:
            response = osu_api.profile(username, osumode).json()
            if osumode == '':
                osumode = response['playmode']
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('profile url', f'https://osu.ppy.sh/users/{response["id"]}')
            markup.add(button1)
            if 'button_for_skin' in locals():
                markup.add(button_for_skin)
            text += f"""ID: {response['id']}\n"""  
            text += f"""Name: {response['username']} ({osumode})\n"""
            text += f"""Global rank: #{response['statistics']['global_rank']}\n"""
            text += f"""Country rank: #{response['statistics']['rank']['country']}({response['country_code']})\n"""
            text += f"""PP: {response['statistics']['pp']}\n"""
            text += f"""Accuracy: {round(response['statistics']['hit_accuracy'], 2)}%\n"""
            text += f"""Medals: {len(response['user_achievements'])}\n"""
            text += f"""Play count: {response['statistics']['play_count']}\n"""
            text += f"""Play time: {response['statistics']['play_time']//86400}days {response['statistics']['play_time']//3600%24}hour {response['statistics']['play_time']//60%60}min ({response['statistics']['play_time']//3600} hours)\n"""
            text += f"""*SSH*:{response['statistics']['grade_counts']['ssh']}  *SS*:{response['statistics']['grade_counts']['ss']}  *SH*:{response['statistics']['grade_counts']['sh']}  *S*:{response['statistics']['grade_counts']['s']}  *A*:{response['statistics']['grade_counts']['a']}\n"""
            await bot.send_photo(message.chat.id, response['cover']['url'],text , reply_to_message_id=message.id, reply_markup=markup, parse_mode='MARKDOWN')
        except:
            await bot.reply_to(message, "ERROR: username is not exists")
    else:
        await bot.reply_to(message, 'ERROR: write username OR set nick `su nick <username>`', parse_mode="MARKDOWN")