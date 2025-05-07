from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import sqlite3
from commands.osu.recent import templates

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api, offset = '0', isinline=False, botcall=None, osuid=None, osumode=None):
    text = ''
    isSended = False
    osuuser = None
    allflags = ['-offset', '-off']
    user_res = None
    recent_res = None
    recent_res_raw = None
    beatmap_res = None
    if (msgsplit[1] not in all_modes) and (msgsplit[1] != '$empty$') and (msgsplit[1] not in allflags):
        response = osu_api.profile(msgsplit[1]).json()
        try:
            osuid = response['id']
            osuuser = response['username']
            osumode = response['playmode']
        except:
            osuid = None
            osuuser = None
            osumode = None
    elif osuid == None and not isinline:
        with sqlite3.connect(OSU_USERS_DB) as db:
            if message.reply_to_message:
                tgid = message.reply_to_message.from_user.id
            elif not message.reply_to_message:
                tgid = message.from_user.id
            cursor = db.cursor()
            queue = f''' SELECT tg_id, osu_id, osu_mode, osu_username FROM osu_users WHERE tg_id={tgid}'''
            cursor.execute(queue)
            dbresult = cursor.fetchone()
            if dbresult != None:
                osuuser = dbresult[3]
                osuid = dbresult[1]
                osumode = dbresult[2]
    

    if osumode != None:
        osumode = next((m for m in msgsplit if m in set(all_modes)), osumode)
        if osumode in ("-std", '-osu'):
            osumode = 'osu'
        elif osumode in ('-m', '-mania'):
            osumode = 'mania'
        elif osumode in ('-t', '-taiko'):
            osumode = 'taiko'
        elif osumode in ('-c' or '-ctb' or '-catch'):
            osumode = 'fruits'


    if not isinline:
        for i in ['-offset', '-off']:
            if i in msgsplit:
                index = msgsplit.index(i) + 1
                offset = msgsplit[index] if msgsplit[index] != '$empty$' else '0'
    try:
        if int(offset) <= 0:
            offset = '0'
    except:
        offset = '0'


    if osuid != None:
        while recent_res_raw == None:
            try:
                recent_res_raw = osu_api.user_scores(osuid, 'recent', mode=osumode, limit='10000', include_fails='1').json()
            except:
                recent_res_raw == None
            await asyncio.sleep(0.1)

        if int(offset) < len(recent_res_raw):
            recent_res = recent_res_raw[int(offset)]
        else:
            recent_res = None

        while beatmap_res == None and recent_res != None:
            try:
                beatmap_res = osu_api.beatmap(recent_res['beatmap']['id']).json()
            except:
                beatmap_res == None
            await asyncio.sleep(0.1)

        while user_res == None:
            try:
                user_res = osu_api.profile(osuid, mode=osumode, use_id=True).json()
            except:
                user_res == None
            await asyncio.sleep(0.1)
    else:
        text = 'ERROR: set nick in bot with `su nick`'
        await bot.reply_to(message, text, parse_mode='MARKDOWN')


    try:
        markup = types.InlineKeyboardMarkup()
        buttonNext = types.InlineKeyboardButton('< Next', callback_data=f'osu_recent_next@{offset}@{osuid}@{osumode}')
        buttonPage = types.InlineKeyboardButton(f'{int(offset)+1}/{len(recent_res_raw)}', callback_data='.')
        buttonUpdate = types.InlineKeyboardButton('🔄', callback_data=f'osu_recent_update@{offset}@{osuid}@{osumode}')
        buttonPrev = types.InlineKeyboardButton('Prev >', callback_data=f'osu_recent_prev@{offset}@{osuid}@{osumode}')
    except:
        pass
    if type(recent_res) == dict and type(beatmap_res) == dict and type(user_res) == dict:
        text = await templates.main(osumode, recent_res, beatmap_res, user_res, offset)
        markup.add(buttonPage)
        markup.add(buttonNext, buttonUpdate, buttonPrev)
        if isinline:
            try:
                await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', reply_markup=markup, link_preview_options=types.LinkPreviewOptions(False, beatmap_res['beatmapset']['covers']['card@2x'], prefer_large_media=True, show_above_text=True))
            except:
                await bot.answer_callback_query(botcall.id, 'no updates')
        else:
            await bot.reply_to(message, text, parse_mode='MARKDOWN', reply_markup=markup, link_preview_options=types.LinkPreviewOptions(False, beatmap_res['beatmapset']['covers']['card@2x'], prefer_large_media=True, show_above_text=True))
    elif type(recent_res) != dict and osuid != None:
        text = f'ERROR: no recent scores for 24 hours\noffset = {offset}'
        if isinline:
            markup.add(buttonNext)
            await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', reply_markup=markup)
        else:
            await bot.reply_to(message, text)