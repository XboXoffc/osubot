from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from commands.osu.groups import groupdb

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message:types.Message, msgsplit:list):
    tg_id:int = message.from_user.id
    tg_chat_id:int = message.chat.id
    try: mode:str = msgsplit[1]
    except: mode = None
    args:list[str] = msgsplit[2:]

    chat_admin_ids:list[int] = []
    chat_admins:list[types.ChatMemberAdministrator] = await bot.get_chat_administrators(tg_chat_id)
    for i in range(len(chat_admins)):
        chat_admin_ids.append(chat_admins[i].user.id)

    if tg_id in chat_admin_ids:
        if mode in ['delete', 'del', 'вуд']:
            if len(args) > 0:
                tg_id:int = args[0]
                text = await groupdb.main(mode, tg_chat_id, tg_id)
                await bot.reply_to(message, text)
            else:
                await bot.reply_to(message, 'ERROR: no args')
        elif mode is None:
            await bot.reply_to(message, 'ERROR: there is no mode') 
        else:
            await bot.reply_to(message, 'ERROR: this mode is not exists') 
    else:
        await bot.reply_to(message, 'ERROR: You are not admin')



