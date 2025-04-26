from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import sqlite3
from commands import other
from commands.osu.calculator import pp as pp_cal

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api, offset = '0', isinline=False, botcall=None, osuid=None, osumode=None):
    text = ''
    osuuser=None
    allflags = ['-offset', '-off']
    user_res = None
    recent_res = None
    beatmap_res = None
    if (msgsplit[1] not in all_modes) and (msgsplit[1] != '$empty$') and (msgsplit[1] not in allflags):
        response = osu_api.profile(msgsplit[1]).json()
        osuid = response['id']
        osuuser = response['username']
        osumode = response['playmode']
    elif osuid == None and not isinline:
        with sqlite3.connect(OSU_USERS_DB) as db:
            if message.reply_to_message:
                tgid = message.reply_to_message.from_user.id
            elif not message.reply_to_message:
                tgid = message.from_user.id
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
        while recent_res == None:
            try:
                recent_res = osu_api.user_scores(osuid, 'recent', mode=osumode, offset=offset, include_fails='1').json()
            except:
                recent_res == None
            await asyncio.sleep(0.1)

        try:
            recent_res = recent_res[0]
        except:
            recent_res == None

        while beatmap_res == None and len(recent_res) != 0:
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

    markup = types.InlineKeyboardMarkup()
    buttonNext = types.InlineKeyboardButton('< Next', callback_data=f'osu_recent_next@{offset}@{osuid}@{osumode}')
    buttonPrev = types.InlineKeyboardButton('Prev >', callback_data=f'osu_recent_prev@{offset}@{osuid}@{osumode}')
    if type(recent_res) == dict and type(beatmap_res) == dict and type(user_res) == dict:
        text += f'''[{recent_res['user']['username']}](https://osu.ppy.sh/users/{recent_res['user']['id']}) (Global: #{user_res['statistics']['global_rank']}, {user_res['country_code']}: #{user_res['statistics']['rank']['country']})\n'''

        artist_title = f'''{recent_res['beatmapset']['artist']} - {recent_res['beatmapset']['title']}'''
        artist_title = artist_title.replace('[', '')
        artist_title = artist_title.replace(']', '')
        text += f'''[{artist_title}]({recent_res['beatmap']['url']}) '''
        text += f'''[[{recent_res['beatmap']['version']}, {recent_res['beatmap']['difficulty_rating']}✩]] by [{recent_res['beatmapset']['creator']}] '''
        text += f'''<{recent_res['beatmap']['status']}>\n'''

        beatmapmods = ''.join(recent_res['mods'][i]['acronym'] for i in range(len(recent_res['mods'])))
        beatmapmin = beatmap_res['total_length']//60
        beatmapsec = str(beatmap_res['total_length']%60)
        if len(beatmapsec) == 1:
            beatmapsec = f"""0{beatmapsec}"""
        beatmaptime = f'''{beatmapmin}:{beatmapsec}'''
        text += f'''{beatmaptime} | AR:{beatmap_res['ar']} OD:{beatmap_res['accuracy']} CS:{beatmap_res['cs']} HP:{beatmap_res['drain']}  {round(beatmap_res['bpm'])}BPM | +{beatmapmods}\n'''

        text += f'''\n'''

        text += f'''Score: {recent_res['classic_total_score']} | Combo: {recent_res['max_combo']}/{beatmap_res['max_combo']} | Accuracy: {round(recent_res['accuracy']*100, 2)}%\n'''
        
        hits = ['great', 'ok', 'meh', 'miss']
        great = ok = meh = miss = '0'
        for hit in hits:
            value = recent_res['statistics'].get(hit, '0')
            match hit:
                case 'great':
                    great = value
                case 'ok':
                    ok = value
                case 'meh':
                    meh = value
                case 'miss':
                    miss = value
        lazer = True
        mods = recent_res['mods']
        accuracy = recent_res['accuracy'] * 100
        combo = recent_res['max_combo']
        pps = await pp_cal.main(recent_res['beatmap']['id'], lazer=lazer, accuracy=accuracy, combo=combo, n300=int(great), n100=int(ok), n50=int(meh), misses=int(miss))
        if isinstance(recent_res['pp'], (int, float)):
            pp = round(recent_res['pp'], 2)
        else:
            pp = str(round(pps['if_rank'], 2)) + '(if rank)'
        pp_fc = round(pps['if_fc'], 2)
        pp_ss = round(pps['if_ss'], 2)
        pp_99 = round(pps['if_99'], 2)
        pp_98 = round(pps['if_98'], 2)
        pp_97 = round(pps['if_97'], 2)
        text += f'''*PP:* {pp} *FC:* {pp_fc} *SS:* {pp_ss}\n'''
        text += f'''*99%:* {pp_99} *98%:* {pp_98} *97%:* {pp_97}\n'''
        text += f'''*300*: {great}  *100*: {ok}  *50*: {meh}  *Miss*:{miss}\n'''

        rank = recent_res['rank'] if recent_res['passed'] else 'F'
        totalhitobjects = beatmap_res['count_circles'] + beatmap_res['count_sliders'] + beatmap_res['count_spinners']
        scorehits = recent_res["maximum_statistics"]["great"]
        percentage = f"""({round(scorehits/totalhitobjects*100, 2)}%)""" if recent_res['passed'] == False else ''
        text += f'''Rank: {rank} {percentage} \n'''

        datetime = other.time(recent_res['ended_at'])
        datetime = datetime['day'] + '.' + datetime['month'] + '.' + datetime['year'] + ' ' + datetime['hour'] + ':' + datetime['min']
        text += f'''{datetime}\n'''

        text += f'''\n'''
        text += f'''Score url: https://osu.ppy.sh/scores/{recent_res['id']}\n'''
        
        markup.add(buttonNext, buttonPrev)
        if isinline:
            try:
                await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', reply_markup=markup, link_preview_options=types.LinkPreviewOptions(False, beatmap_res['beatmapset']['covers']['card@2x'], prefer_large_media=True, show_above_text=True))
            except:
                temp = await bot.reply_to(botcall.message, 'no updates (offset = 0)')
                await asyncio.sleep(10)
                await bot.delete_message(temp.chat.id, temp.id)
        else:
            await bot.reply_to(message, text, parse_mode='MARKDOWN', reply_markup=markup, link_preview_options=types.LinkPreviewOptions(False, beatmap_res['beatmapset']['covers']['card@2x'], prefer_large_media=True, show_above_text=True))
    elif type(recent_res) != dict and osuid != None:
        text = f'ERROR: no recent scores for 24 hours\noffset = {offset}'
        if isinline:
            markup.add(buttonNext)
            await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', reply_markup=markup)
        else:
            await bot.reply_to(message, text)