from telebot import types
from commands.osu import osuapi
from commands.osu.url import scores

async def main(message:types.Message, msgsplit:list, osu_api:osuapi.Osu):
    Url:str = msgsplit[0]
    UrlSplit:list = Url.split('/')
    if UrlSplit[2] == 'osu.ppy.sh':
        if UrlSplit[3] == 'scores':
            await scores.main(message, msgsplit, osu_api, UrlSplit)
