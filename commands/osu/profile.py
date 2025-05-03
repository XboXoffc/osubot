from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import requests
import sqlite3
from commands.osu.groups import groupdb

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api):
    text = ''
    osumode = 'osu'
    username = None
    response = None
    from_db = False
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
            from_db = True
            if message.reply_to_message:
                skin_username = message.reply_to_message.from_user.first_name
            else:
                skin_username = message.from_user.first_name
            button_for_skin = types.InlineKeyboardButton(f'''{skin_username}'s skin''', callback_data=f'osu_skin_view@{skinid}')

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
            while response == None:
                try:
                    response = osu_api.profile(username, osumode).json()
                except:
                    response = None
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('profile url', f'https://osu.ppy.sh/users/{response["id"]}')
            markup.add(button1)
            if 'button_for_skin' in locals():
                markup.add(button_for_skin)
            text += f"""[osu!Skills](https://osuskills.com/user/{response['username']}) | [osu!track](https://ameobea.me/osutrack/user/{response['username']})\n"""
            text += f"""ID: {response['id']}\n"""
            text += f"""Name: [{response['username']} ({osumode})]\n"""
            text += f"""Global rank: #{response['statistics']['global_rank']}\n"""
            text += f"""Country rank: #{response['statistics']['rank']['country']}({response['country_code']})\n"""
            text += f"""PP: {response['statistics']['pp']}\n"""
            text += f"""Accuracy: {round(response['statistics']['hit_accuracy'], 2)}%\n"""
            text += f"""Medals: {len(response['user_achievements'])}\n"""
            text += f"""Play count: {response['statistics']['play_count']}\n"""
            text += f"""Play time: {response['statistics']['play_time']//86400}days {response['statistics']['play_time']//3600%24}hour {response['statistics']['play_time']//60%60}min ({response['statistics']['play_time']//3600} hours)\n"""
            text += f"""*SSH*:{response['statistics']['grade_counts']['ssh']}  *SS*:{response['statistics']['grade_counts']['ss']}  *SH*:{response['statistics']['grade_counts']['sh']}  *S*:{response['statistics']['grade_counts']['s']}  *A*:{response['statistics']['grade_counts']['a']}\n"""
            await bot.send_photo(message.chat.id, response['cover']['url'],text , reply_to_message_id=message.id, reply_markup=markup, parse_mode='MARKDOWN')
        except Exception as e:
            print(e)
            await bot.reply_to(message, "ERROR: username is not exists")
    else:
        await bot.reply_to(message, 'ERROR: write username OR set nick `su nick <username>`', parse_mode="MARKDOWN")

    if response != None and message.chat.type in ["group", "supergroup"] and from_db:
        if message.reply_to_message:
            await groupdb.main("profile", message.chat.id, message.reply_to_message.from_user.id, message.reply_to_message.from_user.username,
                                response['id'], response['username'], osumode, 
                                response['statistics']['pp'], response['statistics']['global_rank'], response['statistics']['hit_accuracy'], response['statistics']['play_count'])
        elif not message.reply_to_message:
            await groupdb.main("profile", message.chat.id, message.from_user.id, message.from_user.username,
                                response['id'], response['username'], osumode, 
                                response['statistics']['pp'], response['statistics']['global_rank'], response['statistics']['hit_accuracy'], response['statistics']['play_count'])