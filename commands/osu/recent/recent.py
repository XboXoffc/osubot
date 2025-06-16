from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import sqlite3
from commands.osu.recent import templates
from commands.other import isempty
from commands.osu.utils.fetch import mode as modefetch


OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api, mode, offset = '0', isinline=False, botcall=None, osuid=None, osumode=None):
    allflags = ['-offset', '-off']
    user_res = None
    recent_res = None
    recent_res_raw = None
    beatmap_res = None
    recent_top = []
    if not isempty(msgsplit, 1) and msgsplit[1] not in all_modes and msgsplit[1] not in allflags:
        response = await osu_api.profile(msgsplit[1])
        try:
            osuid = response['id']
            osumode = response['playmode']
        except:
            osuid = None
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
                osuid = dbresult[1]
                osumode = dbresult[2]
    

    if not isinline:
        for i in ['-offset', '-off']:
            if i in msgsplit:
                index = msgsplit.index(i) + 1
                offset = msgsplit[index] if not isempty(msgsplit, index) else '0'
    try:
        if int(offset) <= 0:
            offset = '0'
    except:
        offset = '0'


    osumode = await modefetch(osumode, msgsplit, all_modes)
    if osuid != None:
        recent_res_raw = await osu_api.user_scores(osuid, 'recent', mode=osumode, limit='10000', include_fails='1')
        if int(offset) < len(recent_res_raw):
            if mode == 'recent':
                recent_res = recent_res_raw[int(offset)]
            elif mode == 'recentbest':
                for i in range(len(recent_res_raw)):
                    recent_pp = recent_res_raw[i]['pp']
                    if recent_pp == None:
                        recent_pp = 0
                    recent_top.append(recent_pp)
                for i in range(int(offset)):
                    recent_top[recent_top.index(max(recent_top))] = -1
                recent_top_index = recent_top.index(max(recent_top))
                recent_res = recent_res_raw[recent_top_index]
        else:
            recent_res = None
        
        if recent_res != None:
            beatmap_res = await osu_api.beatmap(recent_res['beatmap']['id'])
            user_res = await osu_api.profile(osuid, mode=osumode, use_id=True)
    else:
        text = 'ERROR: set nick in bot with `su nick`'
        await bot.reply_to(message, text, parse_mode='MARKDOWN')


    markup = types.InlineKeyboardMarkup()
    buttonNext = types.InlineKeyboardButton('< Next', callback_data=f'osu_recent_next@{offset}@{osuid}@{osumode}@{mode}')
    buttonUpdate = types.InlineKeyboardButton('🔄', callback_data=f'osu_recent_update@{offset}@{osuid}@{osumode}@{mode}')
    buttonPrev = types.InlineKeyboardButton('Prev >', callback_data=f'osu_recent_prev@{offset}@{osuid}@{osumode}@{mode}')
    buttonPage = types.InlineKeyboardButton(f'{int(offset)+1}/{len(recent_res_raw)}  (to first page)', callback_data=f'osu_recent_0@{offset}@{osuid}@{osumode}@{mode}')
    if recent_res != None:
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
    elif recent_res == None and osuid != None:
        text = f'ERROR: no recent scores for 24 hours({osumode})\noffset = {offset}'
        if len(recent_res_raw) > 0:
            markup.add(buttonPage)

        if isinline:
            markup.add(buttonNext)
            await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', reply_markup=markup)
        else:
            await bot.reply_to(message, text, reply_markup=markup)