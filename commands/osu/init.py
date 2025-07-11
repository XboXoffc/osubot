from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from commands.osu import osuapi, osuhelp, botinit, ii, nick, avatar, profile, skin, topscores
from commands.osu.recent import recent
from commands.osu.groups import grouptop, update
from commands.osu.compare import compare

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

all_modes = ['-std', '-osu', '-m', '-mania', '-t', '-taiko', '-c', '-ctb', '-catch', '-fruits']

async def main(message, osu_api):
    try:
        msgsplit = message.caption.split(' ')
    except:
        msgsplit = message.text.split(' ')
    msgsplit.pop(0)
    if len(msgsplit) > 0:
        flag = msgsplit[0].lower()

    ###  help
    if len(msgsplit) == 0 or flag in ['help']:
        await osuhelp.main(message, msgsplit)
    ###  profile
    elif flag in ['p', 'profile', 'з']:
        await profile.main(message, msgsplit, all_modes, osu_api)
    ###  skin
    elif flag in ['sk', 'skin', 'ыл']:
        await skin.main(message, msgsplit)
    ###  recent
    elif flag in ['r', 'recent', 'к']:
        await recent.main(message, msgsplit, all_modes, osu_api, 'recent')
    ###  recent best
    elif flag in ['rb', 'recentbest', 'ки']:
        await recent.main(message, msgsplit, all_modes, osu_api, 'recentbest')
    ###  user top scores
    elif flag in ['t', 'top', 'е']:
        await topscores.main(message, msgsplit, all_modes, osu_api)
    ###  set nick
    elif flag in ['nick', 'set', 'тшсл', 'ыуе']:
        await nick.main(message, msgsplit, all_modes, osu_api)
    ###  group top
    elif flag in ['chat', 'c', 'с']:
        await grouptop.main(message, msgsplit, all_modes)
    ###  update
    elif flag in ['update', 'up', 'гз']:
        await update.main(message, msgsplit, all_modes, osu_api)
    ###  avatar
    elif flag in ['avatar']:
        await avatar.main(message, msgsplit, osu_api)
    ###  ii
    elif flag in ['ii', 'шш']:
        await ii.main(message, msgsplit, all_modes, osu_api)
    ### compare
    elif flag in ['compare', 'com', 'сщьзфку', 'сщь']:
        msgsplit.pop(0)
        await compare.main(message, msgsplit, all_modes, osu_api)
    ###  init
    elif flag in ['init']:
        await botinit.main(message)
    else:
        await bot.reply_to(message, "Incorrect command format")