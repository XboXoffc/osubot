from telebot.async_telebot import AsyncTeleBot
import asyncio
import config

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit):
    text = """
*prefixes:* /osu, osu, o, su
*commands:* help, nick(set), profile(p), avatar, recent(r), ii, skin(sk)
< > - required
( ) - optional

`su nick <username> (mode)` - set username
`su profile (username) (mode)` - check profile
`su avatar <username>` - returns avatar
`su r (username) (-offset *num*)` - returns your recent play
`su sk` - add your skin in database
`su ii` - checks your improvement indicator
        """
    await bot.reply_to(message, text, parse_mode='MARKDOWN')