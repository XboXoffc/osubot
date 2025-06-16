from telebot.async_telebot import AsyncTeleBot
import asyncio
import config

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit):
    text = """
*prefixes:* /osu, osu, o, su
*commands:* help, nick(set), profile(p), compare(com), avatar, recent(r), ii, skin(sk), top(t), chat(c)
*modes:* -std, -osu, -m, -mania, -t, -taiko, -c, -ctb, -catch, -fruits
< > - required
( ) - optional

`su nick <username> (mode)` - set username
`su profile (username) (mode)` - check profile
`su compare (user1) (user2) (mode)` - compare profiles
`su avatar <username> (mode)` - returns avatar
`su recent (username) (-offset *num*)` - returns your recent play
`su top (username)` - your top scores list
`su chat (-pp, -acc, -rank, -pc, -ts)` - top of chat members
`su sk` - add your skin in database(send document with this command)
`su ii` - checks your improvement indicator
        """
    await bot.reply_to(message, text, parse_mode='MARKDOWN')