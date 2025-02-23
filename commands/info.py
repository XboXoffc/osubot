from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from commands import other
from telebot import types

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, back_button=False):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("About bot", callback_data="info_about_bot")
    button2 = types.InlineKeyboardButton("Contacts", callback_data="info_contacts")
    button3 = types.InlineKeyboardButton("Support", callback_data="info_support")
    button4 = types.InlineKeyboardButton("Credits", callback_data="info_credits")
    markup.add(button1, button2, button3, button4, row_width=2)
    text = """
Choose any you need
"""
    if not back_button:
        await bot.reply_to(message, text, reply_markup=markup)
    else:
        await bot.edit_message_text(text, message.chat.id, message.id, reply_markup=markup)

async def callback(call):
    if call.data == 'info_back':
        await main(call.message, back_button=True)
    elif call.data == "info_about_bot":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Bot code(github)", "https://github.com/XboXoffc/osubot")
        backbutton = types.InlineKeyboardButton('Back', callback_data='info_back')
        markup.add(button1)
        markup.add(backbutton)
        text = """
Just pet project
There you can check weather and etc
"""
        await bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)
    elif call.data == "info_contacts":
        markup = types.InlineKeyboardMarkup()
        backbutton = types.InlineKeyboardButton('Back', callback_data='info_back')
        markup.add(backbutton)
        text = """
dev: @xbox202
dev channel: @xboxosu
Write me if bot don't work correctly        
"""
        await bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)
    elif call.data == 'info_credits':
        markup = types.InlineKeyboardMarkup()
        backbutton = types.InlineKeyboardButton('Back', callback_data='info_back')
        markup.add(backbutton)
        text ="""
Thanks for imexoQQ(ilmir) for host my bot
"""
        await bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)
    elif call.data == 'info_support':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("DonationAlerts", "https://www.donationalerts.com/r/xbox202")
        backbutton = types.InlineKeyboardButton('Back', callback_data='info_back')
        markup.add(button1)
        markup.add(backbutton)
        text = """
You can help me financially(with donate) or message me(@xbox202) any your idea
"""
        await bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)

print("Cogs | info.py is ready")