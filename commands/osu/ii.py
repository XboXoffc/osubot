from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import sqlite3
from commands import other
from commands.osu.utils.fetch import mode as modefetch
from commands.osu.utils.fetch import user as userdb

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

    if (not await other.isempty(msgsplit, 1)) and (msgsplit[1] not in all_modes):
        response = await osu_api.profile(msgsplit[1], mode)
        try:
            username = response['username']
            mode = response['playmode']
        except:
            username = None
    else:
        user = await userdb(tgid, OSU_USERS_DB)
        if user != None:
            username = user[4]
            mode = user[5]

    mode = await modefetch(mode, msgsplit, all_modes)
    if username != None:
        response = await osu_api.profile(username, mode)
    else:
        await bot.reply_to(message, 'ERROR: set your nick:\n`su nick <username>`', parse_mode="MARKDOWN")

    if 'error' not in response:
        pp = response['statistics']['pp']
        playtime_hours = response['statistics']['play_time']//3600
        ii = await calculate(mode, pp, playtime_hours)

        text = f'''{username}'s improvement indicator\n'''
        text += f'''ii: {ii} ({mode})'''
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('What is ii?', 'https://github.com/ferryhmm/oii')
        markup.add(button1)
        await bot.reply_to(message, text, reply_markup=markup)
    else:
        await bot.reply_to(message, 'ERROR: no info, try other mode', parse_mode="MARKDOWN")

async def calculate(mode, pp, playtime_hours):
    if mode == 'osu':
        expected_playtime = -12 + 0.0781 * pp + 6.01e-6 * (pp**2)
    elif mode == 'mania':
        expected_playtime = -0.601 + 0.0321 * pp + 7.69e-7 * (pp**2)
    elif mode == 'taiko':
        expected_playtime = -1.08 + 0.0179 * pp + 1.65e-6 * (pp**2)
    elif mode == 'fruits':
        expected_playtime = -4.14 + 0.0458 * pp + 2.38e-6 * (pp**2)
    ii = round(expected_playtime / playtime_hours, 2)

    return ii