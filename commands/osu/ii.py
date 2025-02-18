from telebot.async_telebot import AsyncTeleBot
from telebot import types
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

async def main(message, msgsplit):
    username = None
    if msgsplit[1] == '$empty$':
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = ''' SELECT tg_id, osu_username, osu_mode FROM osu_users '''
            cursor.execute(query)
            users = cursor.fetchall()
            for user in users:
                if user[0] == message.from_user.id:
                    username = user[1]
                    mode = user[2]
                    break
                else:
                    username = None
                    mode = None
    if mode == "std":
        mode = 'osu'
    elif mode == 'm':
        mode = 'mania'
    elif mode == 't':
        mode = 'taiko'
    elif mode is ('c' or 'ctb' or 'catch'):
        mode = 'fruits'
    response = osu_api.profile(username, mode).json()
    
    if username != None:
        pp = response['statistics']['pp']
        playtime = response['statistics']['play_time']//3600
        expected_playtime = -3.94 + (0.067 * pp) + ((6.78 * 0.000001) * (pp*pp))
        ii = round(expected_playtime / playtime, 2)

        text = f'''{username}'s improvement indicator\n'''
        text += f'''ii: {ii} ({mode})'''
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('What is ii?', 'https://github.com/ferryhmm/oii')
        markup.add(button1)
        await bot.reply_to(message, text, reply_markup=markup)
    else:
        await bot.reply_to(message, 'ERROR: set your nick:\n`su nick <username>`', parse_mode="MARKDOWN")