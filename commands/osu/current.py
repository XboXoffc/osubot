from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from commands import other
from commands.osu import osuapi
from commands.osu.recent import templates
from commands.osu.utils import fetch
import validators

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message:types.Message = None, msgsplit:list = None, all_modes:list = None, osu_api:osuapi.Osu = None, isinline:bool = False, score_id:int or str = None, beatmap_id:int or str = None, tg_id:int = None, botcall:types.CallbackQuery = None):
    success = False
    reply_is_url:bool = False
    reply_is_score:bool = False
    reply_is_beatmap:bool = False
    reply_is_beatmapset:bool = False
    msg_is_url:bool = False
    msg_is_score:bool = False
    msg_is_beatmap:bool = False
    msg_is_beatmapset:bool = False
    strokes:list = None
    osu_id:int = None

    if not isinline:
        reply_state:bool = message.reply_to_message
        tg_id:int = message.from_user.id

        if reply_state:
            tg_reply_username:str = message.reply_to_message.from_user.username
            tg_reply_id:int = message.reply_to_message.from_user.id
            tg_reply_text:str = message.reply_to_message.text
            if tg_reply_text == None:
                tg_reply_text = message.reply_to_message.caption


            strokes = tg_reply_text.split('\n')
            reply_is_url, reply_is_score, reply_is_beatmap, reply_is_beatmapset = await thereisurl(strokes)
        else:
            tg_reply_username:str = None
            tg_reply_id:int = None
            tg_reply_text:str = None
            msg_is_url, msg_is_score, msg_is_beatmap, msg_is_beatmapset = await thereisurl(msgsplit)

        if reply_is_beatmap or msg_is_beatmap:
            beatmap_id, osu_id = await idfetch(osu_api, msgsplit, strokes, reply_is_beatmap)
        elif reply_is_beatmapset or msg_is_beatmapset:
            beatmap_id, osu_id = await idfetch(osu_api, msgsplit, strokes, reply_is_beatmapset, True)
        elif reply_is_score or msg_is_score:
            score_id, osu_id = await idfetch(osu_api, msgsplit, strokes, reply_is_score)

    text:str = ''
    if isinline:
        if botcall.from_user.username != None:
            text:str = f'''@{botcall.from_user.username},\n'''
        else:
            text:str = f'''{botcall.from_user.id},\n'''
    

    if osu_id == None:
        osu_data:tuple = await fetch.user(tg_id, OSU_USERS_DB)
        if osu_data != None:
            osu_id:int = osu_data[3]
        else:
            text += 'ERROR: set nick in bot with `su nick`'


    if score_id != None and await other.isint(score_id):
        score_res:dict = await osu_api.get_score(score_id)
        beatmap_id:int = score_res['beatmap']['id']
        beatmap_res:dict = await osu_api.beatmap(beatmap_id)
        osu_mode:str = beatmap_res['mode']
    elif beatmap_id != None and await other.isint(beatmap_id):
        beatmap_res:dict = await osu_api.beatmap(beatmap_id)
        osu_mode:str = beatmap_res['mode']
    else:
        text += f'ERROR: reply to message with score or beatmap url on the end'


    if osu_id != None and (beatmap_id != None or score_id != None):
        osubeatmapscore:dict = await osu_api.get_user_beatmap_score(osu_id, beatmap_id, mode=osu_mode)
        if not ('error' in osubeatmapscore):
            profile_res:dict = await osu_api.profile(osu_id, osu_mode, use_id=True)

            text += await templates.main(osu_mode, osubeatmapscore['score'], beatmap_res, profile_res, osubeatmapscore['position'], is_current=True)
            success = True
            if isinline: reply_to_message_id = botcall.message.id
            else: reply_to_message_id = message.id
            await bot.send_message(
                message.chat.id, 
                text, 
                reply_to_message_id=reply_to_message_id,
                parse_mode='MARKDOWN', 
                link_preview_options=types.LinkPreviewOptions(
                    is_disabled=False, 
                    url=beatmap_res['beatmapset']['covers']['card@2x'], 
                    prefer_large_media=True, 
                    show_above_text=True
                )
            )
        else:
            text += 'ERROR: your score on this beatmap not exists'
            
    if not success:
        if isinline: reply_to_message_id = botcall.message.id
        else: reply_to_message_id = message.id
        await bot.send_message(
            message.chat.id, 
            text, 
            reply_to_message_id=reply_to_message_id,
            parse_mode='MARKDOWN'
        )



async def idfetch(osu_api:osuapi.Osu, msgsplit:list = None, strokes:list = None, reply_is:bool = False, reply_is_beatmapset:bool = False):
    osu_id = None
    fetchedid = None
    osu_mode = None
    base = ''

    if reply_is_beatmapset:
        if strokes != None:
            if '#' in strokes[-1]:
                base = strokes[-1].split('#')[1]
        elif msgsplit != None:
            if '#' in msgsplit[-1]:
                base = msgsplit[-1].split('#')[1]
    else:
        if strokes != None:
            base = strokes[-1]
        elif msgsplit != None:
            base = msgsplit[-1]

    if base.split('/') != '':
        osu_mode = base.split('/')[0]


    if len(msgsplit) == 0 and reply_is:
        fetchedid:int = base.split('/')[-1]

    elif len(msgsplit) == 1 and reply_is:
        fetchedid:int = base.split('/')[-1]
        osu_name:str = msgsplit[0]
        profile_res = await osu_api.profile(osu_name)
        osu_id = int(profile_res['id'])

    elif len(msgsplit) == 1 and not reply_is:
        try:
            fetchedid:int = int(base.split('/')[-1])
        except:
            pass

    elif len(msgsplit) == 2 and not reply_is:
        islink = []
        for i in range(2):
            islink.append(validators.url(msgsplit[i]))
        if islink[0] != islink[1]:
            try:
                for i in range(2):
                    if islink[i]:
                        fetchedid:int = int(msgsplit[i].split('/')[-1])
                        msgsplit.pop(i)
            finally:
                osu_name:str = msgsplit[-1]
                profile_res = await osu_api.profile(osu_name)
                osu_id = int(profile_res['id'])
    

    if not await other.isint(fetchedid):
        fetchedid = None
    return fetchedid, osu_id



async def thereisurl(list:list):
    there_is_url, is_score_url, is_beatmap_url, is_beatmapset_url = False, False, False, False
    if 'https://osu.ppy.sh/scores/' in list[-1]:
        is_score_url = True
    elif 'https://osu.ppy.sh/b/' in list[-1]:
        is_beatmap_url = True
    elif 'https://osu.ppy.sh/beatmaps/' in list[-1]:
        is_beatmap_url = True
    elif 'https://osu.ppy.sh/s/' in list[-1]:
        is_beatmapset_url = True
    elif 'https://osu.ppy.sh/beatmapsets/' in list[-1]:
        is_beatmapset_url = True
    there_is_url = is_score_url or is_beatmap_url or is_beatmap_url

    return [there_is_url, is_score_url, is_beatmap_url, is_beatmapset_url]


