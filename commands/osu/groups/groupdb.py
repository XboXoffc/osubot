import config
import sqlite3

OSU_GROUPS_DB = config.OSU_GROUPS_DB

async def main(mode, tg_chat_id=None, tg_id=None, tg_username=None, osu_id=None, osu_username=None, osu_mode=None, osu_pp=None, osu_rank=None, osu_acc=None, osu_playcount=None, osu_topscore=None):
    tg_chat_id = str(tg_chat_id)
    tg_chat_id = tg_chat_id.replace('-', '')
    table_name = "ID" + tg_chat_id
    with sqlite3.connect(OSU_GROUPS_DB) as db:
        cursor = db.cursor()
        query = f""" CREATE TABLE IF NOT EXISTS {table_name}(
        tg_id INTEGER NOT NULL,
        tg_username TEXT,
        osu_id INTEGER,
        osu_username TEXT,
        osu_mode TEXT NOT NULL,
        osu_pp REAL,
        osu_rank INTEGER,
        osu_acc REAL,
        osu_playcount INTEGER,
        osu_topscore REAL
        ) """
        
        cursor.execute(query)

    if mode == "profile":
        with sqlite3.connect(OSU_GROUPS_DB) as db:
            cursor = db.cursor()

            query = f""" DELETE FROM {table_name} WHERE tg_id={tg_id} AND osu_mode='{osu_mode}' """

            query1 = f""" REPLACE INTO {table_name}(tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount)
                        VALUES({tg_id}, '{tg_username}', {osu_id}, '{osu_username}', '{osu_mode}', {osu_pp}, {osu_rank}, {osu_acc}, {osu_playcount}) """

            cursor.execute(query)
            cursor.execute(query1)









