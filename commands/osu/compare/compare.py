from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import sqlite3
from commands.osu import osuapi
from commands.osu.utils.fetch import mode as modefetch
from commands.osu.utils.fetch import user as userfetch
from commands.osu import ii
from commands.osu.compare import templates

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message:types.Message, msgsplit:list, all_modes:list, osu_api:osuapi.Osu):
    osumode = 'osu'
    osuids = [None, None]
    profile_list = [None, None]
    top_list = [None, None]
    ii_list = [None, None]
    reply_state = message.reply_to_message

    osumode, osumode_index = await modefetch(osumode, msgsplit, all_modes, send_index=True)
    if osumode_index != None:
        msgsplit.pop(osumode_index)

    if reply_state:
        tg_id = message.from_user.id
        tg_reply_id = message.reply_to_message.from_user.id
    else:
        tg_id = message.from_user.id
        tg_reply_id = None


    if len(msgsplit) == 0:
        if reply_state:
            osuids[0], osuids[1] = await userfetch(tg_id, OSU_USERS_DB), await userfetch(tg_reply_id, OSU_USERS_DB)
            osuids[0], osuids[1] = osuids[0][3], osuids[1][3]

    elif len(msgsplit) == 1:
        if reply_state:
            osuids[0] = await userfetch(tg_reply_id, OSU_USERS_DB)
            res = await osu_api.profile(msgsplit[0], osumode)
            if 'error' not in res:
                osuids[1] = res['id']

        elif not reply_state:
            osuids[0] = await userfetch(tg_id, OSU_USERS_DB)
            res = await osu_api.profile(msgsplit[0], osumode)
            if 'error' not in res:
                osuids[1] = res['id']

    elif len(msgsplit) >= 2:
        for i in range(2):
            res = await osu_api.profile(msgsplit[i], osumode)
            if 'error' not in res:
                osuids[i] = res['id']


    if osuids[0] != None and osuids[1] != None:
        for i in range(2):
            profile_list[i] = await osu_api.profile(osuids[i], osumode, use_id=True)
            top_list[i] = await osu_api.user_scores(osuids[i], 'best', mode=osumode)
            ii_list[i] = await ii.calculate(osumode, profile_list[i]['statistics']['pp'], profile_list[i]['statistics']['play_time']//3600)
        markup = types.InlineKeyboardMarkup()
        butuser1 = types.InlineKeyboardButton(profile_list[0]['username'], f'https://osu.ppy.sh/users/{profile_list[0]['id']}')
        butuser2 = types.InlineKeyboardButton(profile_list[1]['username'], f'https://osu.ppy.sh/users/{profile_list[1]['id']}')
        markup.add(butuser1, butuser2)
        text = await templates.compare(profile_list, top_list, ii_list, osumode)
        await bot.reply_to(message, text, parse_mode='MARKDOWN', reply_markup=markup)

    elif len(msgsplit) == 0 and reply_state:
        text = 'ERROR: set nick `su nick <username>`'
        await bot.reply_to(message, text, parse_mode="MARKDOWN")

    elif len(msgsplit) == 0 and not reply_state:
        text = '''ERROR: add args or reply to other message'''
        await bot.reply_to(message, text)

    elif len(msgsplit) == 1:
        text = f'''ERROR: The user {msgsplit[0]} doesn't exist'''
        await bot.reply_to(message, text)
    
    elif len(msgsplit) >= 2:
        text = f'''ERROR: The user {msgsplit[0]} or {msgsplit[1]} doesn't exist'''
        await bot.reply_to(message, text)











