from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
import sqlite3
from commands.osu.groups import templates, groupdb
from commands.osu import ii

OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message, msgsplit, all_modes, osu_api):
    SilenceMode = False
    osu_id = None
    osu_mode = None
    profile_res = None
    top_res = None
    tg_chat_id = message.chat.id

    if message.chat.type in ["group", "supergroup"]:
        if message.reply_to_message:
            tg_id = message.reply_to_message.from_user.id
        elif not message.reply_to_message:
            tg_id = message.from_user.id

        if message.reply_to_message:
            tg_username = message.reply_to_message.from_user.username
        elif not message.reply_to_message:
            tg_username = message.from_user.username
        
        for i in ['-silence', '-s', '-ы']:
            if i in msgsplit:
                SilenceMode = True

        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = f''' SELECT * FROM osu_users WHERE tg_id={tg_id} '''
            cursor.execute(query)
            userdata = cursor.fetchone()

            osu_id = userdata[3]
            osu_mode = userdata[5]

        osu_mode = next((m for m in msgsplit if m in set(all_modes)), osu_mode)
        if osu_mode in ("-std", '-osu'):
            osu_mode = 'osu'
        elif osu_mode in ('-m', '-mania'):
            osu_mode = 'mania'
        elif osu_mode in ('-t', '-taiko'):
            osu_mode = 'taiko'
        elif osu_mode in ('-c' or '-ctb' or '-catch'):
            osu_mode = 'fruits'
        
        if osu_id != None and osu_mode != None:
            profile_res = await osu_api.profile(osu_id, mode=osu_mode, use_id=True)
            top_res = await osu_api.user_scores(osu_id, 'best', mode=osu_mode)
            top_res = top_res[0]
        else:
            await bot.reply_to(message, 'ERROR: write username OR set nick `su nick <username>`', parse_mode="MARKDOWN")

        if profile_res != None and top_res != None:
            osu_username = profile_res['username']
            osu_pp = profile_res['statistics']['pp']
            osu_rank = profile_res['statistics']['global_rank']
            osu_acc = profile_res['statistics']['hit_accuracy']
            osu_playcount = profile_res['statistics']['play_count']
            osu_topscore = top_res['pp']
            playtime = profile_res['statistics']['play_time']//3600
            osu_ii = await ii.calculate(osu_mode, osu_pp, playtime)

            new_db = [tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore, osu_ii]
            old_db = await groupdb.main('update', tg_chat_id, tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore, osu_ii)
        else:
            await bot.reply_to(message, 'ERROR: user is not exist, change nick `su nick <username>`', parse_mode="MARKDOWN")
            old_db = False
        
        if old_db and not SilenceMode:
            text = await templates.update(message, old_db, new_db)
            await bot.reply_to(message, text, parse_mode="MARKDOWN")
        elif old_db and SilenceMode:
            await bot.reply_to(message, 'Your data was updated')
        elif old_db == None:
            await bot.reply_to(message, 'ERROR: I do not have your data, write `su p` to add it, then you can update it', parse_mode="MARKDOWN")
        else:
            await bot.reply_to(message, 'ERROR: idk how you get this, write to dev')
    else:
        await bot.reply_to(message, 'ERROR: you are write not in group')












