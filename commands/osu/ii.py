from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import sqlite3
from commands.other import isempty

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api):
    username = None
    mode = 'osu'
    response = None

    if message.reply_to_message:
        tgid = message.reply_to_message.from_user.id
    elif not message.reply_to_message:
        tgid = message.from_user.id

    if (not isempty(msgsplit, 1)) and (msgsplit[1] not in all_modes):
        response = await osu_api.profile(msgsplit[1], mode)
        try:
            username = response['username']
            mode = response['playmode']
        except:
            username = None
    else:
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = ''' SELECT tg_id, osu_username, osu_mode FROM osu_users '''
            cursor.execute(query)
            users = cursor.fetchall()
            for user in users:
                if user[0] == tgid:
                    username = user[1]
                    mode = user[2]
                    break
                else:
                    username = None
                    mode = None
    
    mode = next((m for m in msgsplit if m in set(all_modes)), mode)
    if mode == "-std":
        mode = 'osu'
    elif mode == '-m':
        mode = 'mania'
    elif mode == '-t':
        mode = 'taiko'
    elif mode in ('-c' or '-ctb' or '-catch'):
        mode = 'fruits'
    
    if username != None and mode != None:
        response = await osu_api.profile(username, mode)
        pp = response['statistics']['pp']
        playtime = response['statistics']['play_time']//3600
        ii = await calculate(mode, pp, playtime)

        text = f'''{username}'s improvement indicator\n'''
        text += f'''ii: {ii} ({mode})'''
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('What is ii?', 'https://github.com/ferryhmm/oii')
        markup.add(button1)
        await bot.reply_to(message, text, reply_markup=markup)
    else:
        await bot.reply_to(message, 'ERROR: set your nick:\n`su nick <username>`', parse_mode="MARKDOWN")

async def calculate(mode, pp, playtime_hours):
    if mode == 'osu':
        expected_playtime = -4.49 + 0.0601 * pp + 0.00000966 * pp**2
    elif mode == 'mania':
        expected_playtime = 0.227 + 0.0306 * pp + 0.00000107 * pp**2
    elif mode == 'taiko':
        expected_playtime = -0.159 + 0.00891 * pp + 0.00000329 * pp**2
    elif mode == 'fruits':
        expected_playtime = -4.63 + 0.0564 * pp + 0.00000211 * pp**2
    ii = round(expected_playtime / playtime_hours, 2)

    return ii