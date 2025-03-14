from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
import sqlite3
from commands import other

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api, offset = '0', isinline=False, botcall=None, osuid=None, osumode=None):
    text = ''
    osuuser=None
    allflags = ['-offset', '-off']
    user_res = {}
    recent_res = {}
    beatmap_res = {}
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
        try:
            recent_res = osu_api.user_scores(osuid, 'recent', mode=osumode, offset=offset, include_fails='1').json()[0]
            beatmap_res = osu_api.beatmap(recent_res['beatmap']['id']).json()
            user_res = osu_api.profile(osuid, mode=osumode, use_id=True).json()
        except:
            pass
    else:
        text = 'ERROR: set nick in bot with `su nick`'
        await bot.reply_to(message, text, parse_mode='MARKDOWN')

    markup = types.InlineKeyboardMarkup()
    buttonNext = types.InlineKeyboardButton('< Next', callback_data=f'osu_recent_next@{offset}@{osuid}@{osumode}')
    buttonPrev = types.InlineKeyboardButton('Prev >', callback_data=f'osu_recent_prev@{offset}@{osuid}@{osumode}')
    if len(recent_res) != 0:
        #if isinline:
        #    await bot.delete_message(delchatid, delmsgid)

        text += f'''[{recent_res['user']['username']}](https://osu.ppy.sh/{recent_res['user']['id']}) (Global: #{user_res['statistics']['global_rank']}, {user_res['country_code']}: #{user_res['statistics']['rank']['country']})\n'''

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
        
        if isinstance(recent_res['pp'], (int, float)):
            pp = round(recent_res['pp'], 2)
        else:
            pp = 'no pp'
        text += f'''PP: {pp}\n'''

        hits = ['great', 'ok', 'meh', 'miss']
        great = ok = meh = miss = '0'
        for hit in hits:
            value = recent_res['statistics'].get(hit, '0')
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

        rank = recent_res['rank'] if recent_res['passed'] else 'F'
        percentage = f"""({round(recent_res["maximum_statistics"]["great"]/beatmap_res['max_combo']*100, 2)}%)""" if recent_res['passed'] == False else ''
        text += f'''Rank: {rank} {percentage} \n'''

        datetime = other.time(recent_res['ended_at'])
        datetime = datetime['day'] + '.' + datetime['month'] + '.' + datetime['year'] + ' ' + datetime['hour'] + ':' + datetime['min']
        text += f'''{datetime}\n'''

        text += f'''\n'''
        text += f'''Score url: https://osu.ppy.sh/scores/{recent_res['id']}\n'''
        
        markup.add(buttonNext, buttonPrev)
        if isinline:
            await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', reply_markup=markup, link_preview_options=types.LinkPreviewOptions(False, beatmap_res['beatmapset']['covers']['card@2x'], prefer_large_media=True, show_above_text=True))
        else:
            await bot.reply_to(message, text, parse_mode='MARKDOWN', reply_markup=markup, link_preview_options=types.LinkPreviewOptions(False, beatmap_res['beatmapset']['covers']['card@2x'], prefer_large_media=True, show_above_text=True))
    elif len(recent_res) == 0 and osuid != None:
        text = f'ERROR: no recent scores for 24 hours\noffset = {offset}'
        if isinline:
            markup.add(buttonNext)
            await bot.edit_message_text(text, botcall.message.chat.id, botcall.message.id, parse_mode='MARKDOWN', reply_markup=markup)
        else:
            await bot.reply_to(message, text)