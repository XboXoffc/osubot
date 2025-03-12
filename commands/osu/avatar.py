from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import asyncio
import requests

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, osu_api):
        user = msgsplit[1]
        if user != '$empty$':
            try:
                response = osu_api.profile(user)
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(f'{user} profile', f"https://osu.ppy.sh/users/{response.json()['id']}")
                button2 = types.InlineKeyboardButton(f'{user} avatar', response.json()['avatar_url'])
                button3 = types.InlineKeyboardButton(f'{user} cover', response.json()['cover_url'])
                markup.add(button1, row_width=1)
                markup.add(button2, button3, row_width=2)
                await bot.send_photo(message.chat.id, response.json()['avatar_url'], reply_to_message_id=message.id, reply_markup=markup)
            except:
                await bot.reply_to(message, 'ERROR: username is not exists')
        else:
            await bot.reply_to(message, 'ERROR: write username')