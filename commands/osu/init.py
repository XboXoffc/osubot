from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from commands.osu import osuapi, osuhelp, botinit, ii, nick, avatar, profile, skin, recent, topscores

OSU_USERS_DB = config.OSU_USERS_DB
OSU_SKIN_PATH = config.OSU_SKIN_PATH
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

all_modes = ['-std', '-osu', '-m', '-mania', '-t', '-taiko', '-c', '-ctb', '-catch', '-fruits']

async def main(message, osu_api):
    try:
        msgsplit = message.caption.split(' ')
    except:
        msgsplit = message.text.split(' ')
    msgsplit.pop(0)
    for i in range(3):
        msgsplit.append('$empty$')
    flag = msgsplit[0]

    ###  help
    if flag is ('$empty$' or 'help'):
        await osuhelp.main(message, msgsplit)
    ###  profile
    elif flag in ['p', 'profile', 'з']:
        await profile.main(message, msgsplit, all_modes, osu_api)
    ###  skin
    elif flag in ['sk', 'skin', 'ыл']:
        await skin.main(message, msgsplit)
    ###  recent
    elif flag in ['r', 'recent', 'к']:
        await recent.main(message, msgsplit, all_modes, osu_api)
    ###  user top scores
    elif flag in ['t', 'top', 'е']:
        await topscores.main(message, msgsplit, all_modes, osu_api)
    ###  set nick
    elif flag in ['nick', 'set', 'тшсл', 'ыуе']:
        await nick.main(message, msgsplit, all_modes, osu_api)
    ###  avatar
    elif flag in ['avatar']:
        await avatar.main(message, msgsplit, osu_api)
    ###  ii
    elif flag in ['ii', 'шш']:
        await ii.main(message, msgsplit, osu_api)
    ###  init
    elif flag in ['init']:
        await botinit.main(message)
    else:
        await bot.reply_to(message, "Incorrect command format")