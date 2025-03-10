from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
from commands.osu import osuapi
import sqlite3

OSU_ID = config.OSU_CLIENT_ID
OSU_SECRET = config.OSU_CLIENT_SECRET
X_API_VERSION = config.X_API_VERSION
OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

osu_api = osuapi.Osu(OSU_ID, OSU_SECRET, X_API_VERSION)

async def main(message, msgsplit, all_modes, offset = '0', isinline=False, delmsgid=None, delchatid=None):
    text = ''
    osuuser=None
    osuid=None
    osumode=None
    allflags = ['-offset', '-off']
    user_res = None
    recent_res = None
    beatmap_res = None
    if (msgsplit[1] not in all_modes) and (msgsplit[1] != '$empty$') and (msgsplit[1] not in allflags):
        response = osu_api.profile(msgsplit[1]).json()
        osuid = response['id']
        osuuser = response['username']
        osumode = response['playmode']
    else:
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
    
    for i in all_modes:
        if i in msgsplit:
            index = msgsplit.index(i)
            osumode = msgsplit[index]
    osumode = next((m for m in msgsplit if m in set(all_modes)), osumode)
    if osumode == "std":
        osumode = 'osu'
    elif osumode == 'm':
        osumode = 'mania'
    elif osumode == 't':
        osumode = 'taiko'
    elif osumode is ('c' or 'ctb' or 'catch'):
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
    buttonNext = types.InlineKeyboardButton('< Next', callback_data=f'osu_recent_next@{offset}')
    buttonPrev = types.InlineKeyboardButton('Prev >', callback_data=f'osu_recent_prev@{offset}')
    if recent_res != None:
        if isinline:
            await bot.delete_message(delchatid, delmsgid)

        text += f'''[{recent_res['user']['username']}](https://osu.ppy.sh/{recent_res['user']['id']}) (Global: #{user_res['statistics']['global_rank']}, {user_res['country_code']}: #{user_res['statistics']['rank']['country']})\n'''
        
        text += f'''[{recent_res['beatmapset']['artist']} - {recent_res['beatmapset']['title']}]({recent_res['beatmap']['url']}) '''
        text += f'''[[{recent_res['beatmap']['version']}, {recent_res['beatmap']['difficulty_rating']}✩]] by {recent_res['beatmapset']['creator']} '''
        text += f'''<{recent_res['beatmap']['status']}>\n'''

        beatmapmods = ''.join(recent_res['mods'][i]['acronym'] for i in range(len(recent_res['mods'])))
        beatmaptime = f'''{beatmap_res['total_length']//60}:{beatmap_res['total_length']%60}'''
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
        text += f'''Rank: {rank}\n'''

        text += f'''\n'''
        text += f'''Score url: https://osu.ppy.sh/scores/{recent_res['id']}\n'''
        
        markup.add(buttonNext, buttonPrev)
        await bot.send_photo(message.chat.id, beatmap_res['beatmapset']['covers']['card@2x'], text, reply_to_message_id=message.id, parse_mode='MARKDOWN', reply_markup=markup)
    elif recent_res == None and osuid != None:
        text = f'ERROR: no recent scores for 24 hours\noffset = {offset}'
        if isinline:
            markup.add(buttonNext)
            await bot.delete_message(delchatid, delmsgid)
            await bot.reply_to(message, text, reply_markup=markup)
        else:
            await bot.reply_to(message, text)