from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import sqlite3
from commands import other
from commands.osu import osuapi
from commands.osu.recent import templates
from commands.osu.utils import fetch
import validators

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message:types.Message, msgsplit:list, all_modes:list, osu_api:osuapi.Osu):
    reply_is_recent:bool = False
    strokes:list = None
    score_id:int or str = None
    reply_state:bool = message.reply_to_message
    osu_id:int = None


    tg_id:int = message.from_user.id
    if reply_state:
        tg_reply_username:str = message.reply_to_message.from_user.username
        tg_reply_id:int = message.reply_to_message.from_user.id
        tg_reply_text:str = message.reply_to_message.text
        if tg_reply_text == None:
            tg_reply_text = message.reply_to_message.caption


        strokes = tg_reply_text.split('\n')
        if 'https://osu.ppy.sh/scores' in strokes[-1]:
            reply_is_recent = True
    else:
        tg_reply_username:str = None
        tg_reply_id:int = None
        tg_reply_text:str = None


    if len(msgsplit) == 0 and reply_is_recent:
        score_id:int = strokes[-1].split('/')[-1]
    elif len(msgsplit) == 1 and reply_is_recent:
        score_id:int = strokes[-1].split('/')[-1]
        osu_name:str = msgsplit[0]
        profile_res = await osu_api.profile(osu_name)
        osu_id = int(profile_res['id'])
    elif len(msgsplit) == 1 and not reply_is_recent:
        try:
            if validators.url(msgsplit[0]):
                score_id:int = int(msgsplit[0].split('/')[-1])
            else:
                score_id:int = int(msgsplit[0])
        except:
            pass
    elif len(msgsplit) == 2 and not reply_is_recent:
        islink = []
        for i in range(2):
            islink.append(validators.url(msgsplit[i]))
        if islink[0] != islink[1]:
            try:
                for i in range(2):
                    if islink[i]:
                        score_id:int = int(msgsplit[i].split('/')[-1])
                        msgsplit.pop(i)
            finally:
                osu_name:str = msgsplit[-1]
                profile_res = await osu_api.profile(osu_name)
                osu_id = int(profile_res['id'])
    

    if score_id != None and await other.isint(score_id):
        osu_data:tuple = await fetch.user(tg_id, OSU_USERS_DB)
        if osu_data != None or osu_id:
            if osu_id == None:
                osu_id:int = osu_data[3]

            score_res:dict = await osu_api.get_score(score_id)
            beatmapid:int = score_res['beatmap']['id']
            osu_mode:str = score_res['beatmap']['mode']

            osubeatmapscore:dict = await osu_api.get_user_beatmap_score(osu_id, beatmapid, mode=osu_mode)
            if not ('error' in osubeatmapscore):
                beatmap_res:dict = await osu_api.beatmap(beatmapid)
                profile_res:dict = await osu_api.profile(osu_id, osu_mode, use_id=True)

                text = await templates.main(osu_mode, osubeatmapscore['score'], beatmap_res, profile_res, osubeatmapscore['position'], is_current=True)
                await bot.reply_to(
                    message, 
                    text, 
                    parse_mode='MARKDOWN', 
                    link_preview_options=types.LinkPreviewOptions(
                        is_disabled=False, 
                        url=beatmap_res['beatmapset']['covers']['card@2x'], 
                        prefer_large_media=True, 
                        show_above_text=True
                    )
                )
            else:
                text = 'ERROR: your score on this beatmap not exists'
                await bot.reply_to(message, text, parse_mode='MARKDOWN')
        else:
            text = 'ERROR: set nick in bot with `su nick`'
            await bot.reply_to(message, text, parse_mode='MARKDOWN')
    else:
        text = f'ERROR: score id value is "{score_id}", reply to message with score link on the end'
        await bot.reply_to(message, text, parse_mode='MARKDOWN')
        







