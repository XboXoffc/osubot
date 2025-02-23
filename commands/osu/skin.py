from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
import requests
import sqlite3
import os

OSU_USERS_DB = config.OSU_USERS_DB
OSU_SKIN_PATH = config.OSU_SKIN_PATH
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit):
        # save skin
        if message.document:
            if message.document.file_name.split('.')[-1] == 'osk' and message.document.file_size <= 104857600:
                tg_id = message.from_user.id
                file_info = await bot.get_file(message.document.file_id)
                dowloaded_file = await bot.download_file(file_info.file_path)
                src = f'{OSU_SKIN_PATH}{tg_id}-{message.document.file_name}'
                try:
                    with open(src, 'wb') as new_file:
                        new_file.write(dowloaded_file)
                except:
                    with open(src, 'xb') as new_file:
                        new_file.write(dowloaded_file)
                with sqlite3.connect(OSU_USERS_DB) as db:
                    cursor = db.cursor()
                    query = f""" REPLACE INTO osu_skins(tg_id, file_name) VALUES({tg_id}, '{tg_id}@{message.document.file_name}')"""
                    cursor.execute(query)
                await bot.reply_to(message, 'skin saved')
            else:
                await bot.reply_to(message, 'ERROR: file must be .osk and not over 50MB')

        # deleting skin
        elif msgsplit[1] in ['-del', '-d', 'del', 'd']:
            tg_id = message.from_user.id
            with sqlite3.connect(OSU_USERS_DB) as db:
                cursor = db.cursor()
                query = """ SELECT * FROM osu_skins """
                cursor.execute(query)
                for skin_db in cursor.fetchall():
                    if tg_id == skin_db[0]:
                        src = OSU_SKIN_PATH + skin_db[1]
                        print(src)
                        os.remove(src)
                        skin_exist = True
                        break
                    else:
                        skin_exist = False
                if skin_exist:
                    query = f""" DELETE FROM osu_skins WHERE tg_id={tg_id} """
                    cursor.execute(query)
                    await bot.reply_to(message, 'Your skin already deleted')
                elif not skin_exist:
                    await bot.reply_to(message, '''ERROR: your skin wasn't exists''')

        # bot send skin
        elif msgsplit[1] == "$empty$" and not message.document:
            if message.reply_to_message:
                tg_id = message.reply_to_message.from_user.id
            else:
                tg_id = message.from_user.id
            with sqlite3.connect(OSU_USERS_DB) as db:
                cursor = db.cursor()
                query = """ SELECT tg_id, file_name FROM osu_skins """
                cursor.execute(query)
                for user_skin in cursor.fetchall():
                    if user_skin[0] == tg_id:
                        file_name = user_skin[1]
                        user_exists = True
                        break
                    else:
                        user_exists = False
                
                if user_exists:
                    tempmsg = await bot.reply_to(message, 'Skin is uploading...')
                    if message.reply_to_message:
                        text = f'''@{message.from_user.username}, It's his skin'''
                    elif not message.reply_to_message:
                        text = f'Your skin, @{message.from_user.username}'
                    with open(f'{OSU_SKIN_PATH}{file_name}', 'rb') as file:
                        await bot.send_document(message.chat.id, file, message.id, text)
                        await bot.delete_message(tempmsg.chat.id, tempmsg.id)
                elif not user_exists:
                    if message.reply_to_message:
                        await bot.reply_to(message, "ERROR: he didn't added skin")
                    elif not message.reply_to_message:
                        await bot.reply_to(message, 'ERROR: add your skin via `su sk` with .osk document', parse_mode="MARKDOWN")
        else:
            await bot.reply_to(message, 'ERROR: send `su sk` with file .osk and not over 50MB', parse_mode='MARKDOWN')