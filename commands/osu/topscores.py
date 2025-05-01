from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import asyncio
from commands import other
import sqlite3
import math
import time

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def template(message, res_scores, offset, limit, osumode, osu_api):
    scores_limit = len(res_scores)
    res_beatmap = None
    text = ''
    text += f'''[{res_scores[0]['user']['username']}'s] top scores [[{osumode}]]:\n'''
    for i in range(scores_limit):
        while res_beatmap == None:
            try:
                res_beatmap = osu_api.beatmap(res_scores[i]['beatmap']['id']).json()
            except:
                res_beatmap = None

        text += f'''#{i+offset+1} '''
        artist_title = f'''{res_scores[i]['beatmapset']['artist']} - {res_scores[i]['beatmapset']['title']}'''
        artist_title = artist_title.replace('[', '')
        artist_title = artist_title.replace(']', '')
        text += f'''[{artist_title}]({res_scores[i]['beatmap']['url']}) '''
        text += f'''[[{res_scores[i]['beatmap']['version']}, {res_scores[i]['beatmap']['difficulty_rating']}✩]] by [{res_scores[i]['beatmapset']['creator']}] \n'''

        beatmapmods = ''.join(res_scores[i]['mods'][j]['acronym'] for j in range(len(res_scores[i]['mods'])))
        beatmapmin = res_scores[i]['beatmap']['total_length']//60
        beatmapsec = str(res_scores[i]['beatmap']['total_length']%60)
        if len(beatmapsec) == 1:
            beatmapsec = f"""0{beatmapsec}"""
        beatmaptime = f'''{beatmapmin}:{beatmapsec}'''
        text += f'''{beatmaptime} | AR:{res_scores[i]['beatmap']['ar']} OD:{res_scores[i]['beatmap']['accuracy']} CS:{res_scores[i]['beatmap']['cs']} HP:{res_scores[i]['beatmap']['drain']}  {round(res_scores[i]['beatmap']['bpm'])}BPM | +{beatmapmods}\n'''

        text += f'''Score: {res_scores[i]['classic_total_score']} | Combo: {res_scores[i]['max_combo']}/{res_beatmap['max_combo']} | Accuracy: {round(res_scores[i]['accuracy']*100, 2)}%\n'''

        if isinstance(res_scores[i]['pp'], (int, float)):
            pp = round(res_scores[i]['pp'], 2)
        else:
            pp = 'no pp'
        text += f'''PP: {pp} | '''

        hits = ['great', 'ok', 'meh', 'miss']
        great = ok = meh = miss = '0'
        for hit in hits:
            value = res_scores[i]['statistics'].get(hit, '0')
            match hit:
                case 'great':
                    great = str(value)
                case 'ok':
                    ok = str(value)
                case 'meh':
                    meh = str(value)
                case 'miss':
                    miss = str(value)
        text += f'''*300*: {great}  *100*: {ok}  *50*: {meh}  *Miss*:{miss}\n'''

        datetime = other.time(res_scores[i]['ended_at'])
        datetime = datetime['day'] + '.' + datetime['month'] + '.' + datetime['year'] + ' ' + datetime['hour'] + ':' + datetime['min']
        text += f'''{datetime}\n\n'''

    return text

async def main(message, msgsplit, all_modes, osu_api, isinline=False, limit = 3, page = 0, botcall=None, osuid = None, osumode = None):
    osuuser = None
    offset = 0
    res_scores = None
    allflags = ['-p', '-page', '-l', '-limit']
    if message.reply_to_message:
        tgid = message.reply_to_message.from_user.id
    elif not message.reply_to_message:
        tgid = message.from_user.id

    if (msgsplit[1] not in all_modes) and (msgsplit[1] != '$empty$') and (msgsplit[1] not in allflags):
        response = osu_api.profile(msgsplit[1]).json()
        osuid = response['id']
        osuuser = response['username']
        osumode = response['playmode']
    elif osuid == None and not isinline:
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            queue = ''' SELECT tg_id, osu_id, osu_mode, osu_username FROM osu_users '''
            cursor.execute(queue)
            dbresult = cursor.fetchall()
            for users in dbresult:
                if tgid == users[0]:
                    osuuser = users[3]
                    osuid = users[1]
                    osumode = users[2]
                    break
    
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
        for i in ['-p', '-page']:
            if i in msgsplit:
                index = msgsplit.index(i) + 1
                page = int(msgsplit[index]) if msgsplit[index] != '$empty$' and other.isint(msgsplit[index]) else 0
                page -= 1
        for i in ['-l', '-limit']:
            if i in msgsplit:
                index = msgsplit.index(i) + 1
                limit = int(msgsplit[index]) if msgsplit[index] != '$empty$' and other.isint(msgsplit[index]) else 3
    
    if limit > 15:
        limit = 3

    offset = page * limit
    if offset < 0:
        offset = 0
    maxpage = math.ceil(200/limit)

    if osuid != None:
        while res_scores == None:
            try:
                res_scores = osu_api.user_scores(osuid, 'best', mode=osumode, limit=str(limit), offset=str(offset)).json()
            except:
                res_scores = None
    else:
        text = 'ERROR: set nick in bot with `su nick`'
        await bot.reply_to(message, text, parse_mode='MARKDOWN')

    markup = types.InlineKeyboardMarkup()
    ButtonCounter = types.InlineKeyboardButton(f'''{page+1}/{maxpage}''', callback_data=f'osu_topscores_update@{page}@{limit}@{osuid}@{osumode}')
    ButtonPrev = types.InlineKeyboardButton('< Prev', callback_data=f'osu_topscores_prev@{page}@{limit}@{osuid}@{osumode}')
    ButtonNext = types.InlineKeyboardButton('Next >', callback_data=f'osu_topscores_next@{page}@{limit}@{osuid}@{osumode}')
    if len(res_scores) != 0 and page <= maxpage:
        text = await template(message, res_scores, offset, limit, osumode, osu_api)
        if page <= 0:
            markup.add(ButtonCounter, ButtonNext)
        elif page > maxpage:
            markup.add(ButtonPrev, ButtonCounter)
        else:
            markup.add(ButtonPrev, ButtonCounter, ButtonNext)
    elif len(res_scores) == 0 or page > maxpage:
        text = f'ERROR: this page({page+1}) is not exist'
        markup.add(ButtonPrev, ButtonCounter)

    if isinline:
        try:
            await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', link_preview_options=types.LinkPreviewOptions(True), reply_markup=markup)
        except:
            temp = await bot.reply_to(message, f'ERROR: no updates or max page reached, {botcall.from_user.first_name}(@{botcall.from_user.username})')
            await asyncio.sleep(10)
            await bot.delete_message(temp.chat.id, temp.id)
    else:
        await bot.reply_to(message, text, parse_mode='MARKDOWN', link_preview_options=types.LinkPreviewOptions(True), reply_markup=markup)