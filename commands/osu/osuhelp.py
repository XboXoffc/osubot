from telebot.async_telebot import AsyncTeleBot
import asyncio
import config

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit):
    text = """
*message format:* <prefix> <command> <option> <suffix>
*prefixes:* /osu, osu, o, su
*commands:* help, nick(set), profile(p), avatar

< > - required
( ) - optional

`su nick <username> (mode)` - set username
options: any username*(required)* and any mode

`su profile (username)` - check profile
options: you can write any other username
suffixes: osu(std), mania(m), taiko(t), fruits(c, ctb, catch)

`su avatar <username>` - returns avatar
options: any username*(required)*
        """
    await bot.reply_to(message, text, parse_mode='MARKDOWN')
