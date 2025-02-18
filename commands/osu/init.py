from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from commands.osu import osuapi, osuhelp, botinit, ii, nick, avatar, profile, skin, recent


OSU_ID = config.OSU_CLIENT_ID
OSU_SECRET = config.OSU_CLIENT_SECRET
X_API_VERSION = config.X_API_VERSION
OSU_USERS_DB = config.OSU_USERS_DB
OSU_SKIN_PATH = config.OSU_SKIN_PATH
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    osu_api = osuapi.Osu(OSU_ID, OSU_SECRET, X_API_VERSION)
    try:
        msgsplit = message.caption.split(' ')
    except:
        msgsplit = message.text.split(' ')
    msgsplit.pop(0)
    for i in range(3):
        msgsplit.append('$empty$')
    all_modes = ['std', 'osu', 'm', 'mania', 't', 'taiko', 'c', 'ctb', 'catch', 'fruits']
    flag = msgsplit[0]

    ###  help
    if flag is ('$empty$' or 'help'):
        await osuhelp.main(message, msgsplit)
    ###  profile
    elif flag in ['p', 'profile', 'з']:
        await profile.main(message, msgsplit, all_modes)
    ###  skin
    elif flag in ['sk', 'skin', 'ыл']:
        await skin.main(message, msgsplit)
    ###  recent
    elif flag in ['r', 'recent', 'к']:
        await recent.main(message, msgsplit, all_modes)
    ###  set nick
    elif flag in ['nick', 'set']:
        await nick.main(message, msgsplit, all_modes)
    ###  avatar
    elif flag in ['avatar']:
        await avatar.main(message, msgsplit)
    ###  ii
    elif flag in ['ii', 'шш']:
        await ii.main(message, msgsplit)
    ###  init
    elif flag in ['init']:
        await botinit.main(message)
    else:
        await bot.reply_to(message, "Incorrect command format")