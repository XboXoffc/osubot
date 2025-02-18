from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests
import config
from commands import start, info, support, weather, other
from commands.osu import init, osucallback

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

@bot.message_handler(func=lambda message: True, content_types=['text', 'document'])
async def messages(message):
    other.gtm(message)
    messagetext = (message.text or message.caption).lower()
    msgsplit = messagetext.split(' ')
    
    
    if '@' in msgsplit[0]:
        username_part = msgsplit[0].split('@')
        if username_part[1] in ["testxbox202bot", "xboxoffcbot"]:
            msgsplit[0] = username_part[0]

    #Start
    if msgsplit[0] in ['/start', '/help']:
        await start.main(message)
    #Info
    elif msgsplit[0] in ['/info', '/about']:
        await info.main(message)
    #Support
    elif msgsplit[0] in ['/support']:
        await support.main(message)
    #Weather
    elif msgsplit[0] in ['/weather', '/w']:
        await weather.main(message)
    #Osu!
    elif msgsplit[0] in ['/osu' ,'o' ,'su' , 'osu', 'щ', 'ыг']:
        await init.main(message)

@bot.callback_query_handler(func=lambda call:True)
async def Callback(call):
    calldata_prefix = call.data.split('_')
    if calldata_prefix[0] == 'info':
        await info.callback(call)
    elif calldata_prefix[0] == 'osu':
        await osucallback.main(call)


print("Bot | already started\n\n")
asyncio.run(bot.polling(non_stop=True))
