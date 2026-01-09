from telebot.async_telebot import AsyncTeleBot
from telebot import types
import sqlite3
import config
from commands.osu import osuapi
from commands import other

OSU_GROUPS_DB = config.OSU_GROUPS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(osu_api:osuapi.Osu, beatmap_id:int, botcall:types.CallbackQuery, osumode:str):
    chat_id:int = botcall.message.chat.id
    table_name:str = 'ID' + str(chat_id)[1:]
    
    if botcall.from_user.username != None:
        text:str = f'''@{botcall.from_user.username},\n'''
    else:
        text:str = f'''{botcall.from_user.id},\n'''

    beatmap = await osu_api.beatmap(beatmap_id)
    beatmapStatus = beatmap['status']

    if beatmapStatus in ['ranked', 'loved', 'approved']:
        with sqlite3.connect(OSU_GROUPS_DB) as db:
            cur = db.cursor()
            query = f''' SELECT tg_id, tg_username, osu_id, osu_username FROM {table_name} WHERE osu_mode='{osumode}' '''
            cur.execute(query)
            dbdata = cur.fetchall()

        data:list = []
        for user in dbdata:
            tg_id = user[0]
            tg_username = user[1]
            osu_id = user[2]
            osu_username = user[3]

            score_res:dict = await osu_api.get_user_beatmap_score(osu_id, beatmap_id, mode = osumode)
            if not ('error' in score_res):
                score_res.setdefault('tg_id', tg_id)
                score_res.setdefault('tg_username', tg_username)
                data.append(score_res)

        scores_index:list[int] = []
        for i in range(len(data)):
            scores_index.append(data[i]['score']['total_score'])

        top_scores:list[dict] = []
        for i in range(len(data)):
            top_scores.append(data[scores_index.index(max(scores_index))])
            scores_index[scores_index.index(max(scores_index))] = -1

        text += f'''Top of chat member's scores in {osumode} map:\n'''

        beatmapsetArtist = beatmap['beatmapset']['artist']
        beatmapsetTitle = beatmap['beatmapset']['title']
        beatmapsetAuthor = beatmap['beatmapset']['creator']
        beatmapURL = beatmap['url']
        beatmapVER = beatmap['version']
        beatmapDiff = round(beatmap['difficulty_rating'], 2)
        beatmapLength = beatmap['total_length']
        beatmapAR = beatmap['ar']
        beatmapOD = beatmap['accuracy']
        beatmapCS = beatmap['cs']
        beatmapHP = beatmap['drain']
        beatmapBPM = beatmap['bpm']
        max_combo = beatmap['max_combo']

        beatmapsetArtist = beatmapsetArtist.replace('[', '')
        beatmapsetArtist = beatmapsetArtist.replace(']', '')
        beatmapsetTitle = beatmapsetTitle.replace('[', '')
        beatmapsetTitle = beatmapsetTitle.replace(']', '')
        beatmapVER = beatmapVER.replace('[', '')
        beatmapVER = beatmapVER.replace(']', '')

        beatmapMin = beatmapLength//60
        beatmapSec = beatmapLength%60
        if len(str(beatmapSec)) == 1:
            beatmapTime = f'{beatmapMin}:0{beatmapSec}'
        else:
            beatmapTime = f'{beatmapMin}:{beatmapSec}'
        
        text += f'''[{beatmapsetArtist} - {beatmapsetTitle}]({beatmapURL}) [[{beatmapVER}, {beatmapDiff}✩]] by [{beatmapsetAuthor}] <{beatmapStatus}>\n'''
        text += f'''{beatmapTime} | AR:{beatmapAR} OD:{beatmapOD} CS:{beatmapCS} HP:{beatmapHP} {beatmapBPM}BPM \n\n'''

        if len(top_scores) != 0:
            for i in range(len(top_scores)):
                place = i+1
                username = top_scores[i]['score']['user']['username']
                score = top_scores[i]['score']['total_score']
                combo = top_scores[i]['score']['max_combo']
                acc = round(top_scores[i]['score']['accuracy']*100, 2)
                try: pp = round(top_scores[i]['score']['pp'], 2) 
                except: pp = 0
                position = top_scores[i]['position']
                date = await other.time(top_scores[i]['score']['ended_at'])
                date = f'''{date['day']}.{date['month']}.{date['year']}'''

                mods = []
                recentModsRaw = top_scores[i]['score']['mods']
                for j in range(len(recentModsRaw)):
                    mods.append(recentModsRaw[j]['acronym'])
                if mods != []:
                    mods_text = f'+{''.join(mods)}'
                else:
                    mods_text = ''
                
                if top_scores[i]['tg_username'] != 'None':
                    tg_url = f'''https://t.me/{top_scores[i]['tg_username']}'''
                else:
                    tg_url = f'''tg://openmessage?user_id={top_scores[i]['tg_id']}'''

                text += f'''   #{place} [{username}]({tg_url}) | {score} | {combo}/{max_combo}x | {acc}% | {pp}pp {mods_text} | #{position} | {date}\n'''
        else:
            text += 'No scores'
    else:
        text += 'ERROR: beatmap status is not ranked, loved or approved'

    await bot.send_message(botcall.message.chat.id, text, parse_mode="MARKDOWN", link_preview_options=types.LinkPreviewOptions(is_disabled=True))










