from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from commands.osu import osuapi
from commands.osu.recent import templates

bot = AsyncTeleBot(config.TG_TOKEN)

async def main(message:types.Message, msgsplit:list, osu_api:osuapi.Osu, UrlSplit:list):
    score_id:int = int(UrlSplit[4])
    score_res:dict = await osu_api.get_score(score_id)
    if score_res != {'error': "Specified Solo\\Score couldn't be found."} :
        userid = score_res['user']['id']
        beatmapid = score_res['beatmap']['id']
        ruleset_id = score_res['ruleset_id']
        if ruleset_id == 0:
            mode = 'osu'
        elif ruleset_id == 1:
            mode = 'mania'
        elif ruleset_id == 2:
            mode = 'taiko'
        elif ruleset_id == 3:
            mode = 'fruits'

        profile_res:dict = await osu_api.profile(userid, mode, use_id=True)
        beatmap_res:dict = await osu_api.beatmap(beatmapid)

        text = await templates.main(mode, score_res, beatmap_res, profile_res, '?')
        await bot.reply_to(message, text, parse_mode='MARKDOWN', link_preview_options=types.LinkPreviewOptions(False, beatmap_res['beatmapset']['covers']['card@2x'], prefer_large_media=True, show_above_text=True))
    else:
        text = 'ERROR: score is not exists'
        await bot.reply_to(message, text, parse_mode='MARKDOWN')