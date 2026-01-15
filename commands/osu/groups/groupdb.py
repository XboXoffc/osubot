import config
import sqlite3

OSU_GROUPS_DB = config.OSU_GROUPS_DB

async def main(mode, tg_chat_id:int or str=None, tg_id=None, tg_username=None, osu_id=None, osu_username=None, osu_mode=None, osu_pp=None, osu_rank=None, osu_acc=None, osu_playcount=None, osu_topscore=None, osu_ii=None):
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
        osu_topscore REAL,
        osu_ii REAL
        ) """
        
        cursor.execute(query)

    if mode == "profile":
        with sqlite3.connect(OSU_GROUPS_DB) as db:
            cursor = db.cursor()

            query = f""" SELECT * FROM {table_name} WHERE tg_id={tg_id} AND osu_mode='{osu_mode}' """
            cursor.execute(query)
            old_db = cursor.fetchone()
            if old_db != None:
                query = f''' UPDATE {table_name}
                SET tg_username='{tg_username}', 
                    osu_id={osu_id},
                    osu_username='{osu_username}',
                    osu_pp={osu_pp},
                    osu_rank={osu_rank},
                    osu_acc={osu_acc},
                    osu_playcount={osu_playcount}
                WHERE tg_id={tg_id} AND osu_mode='{osu_mode}'
                '''
                cursor.execute(query)
            elif old_db == None:
                query = f""" REPLACE INTO {table_name}(tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount)
                        VALUES({tg_id}, '{tg_username}', {osu_id}, '{osu_username}', '{osu_mode}', {osu_pp}, {osu_rank}, {osu_acc}, {osu_playcount}) """
                cursor.execute(query)

    elif mode == "update":
        with sqlite3.connect(OSU_GROUPS_DB) as db:
            cursor = db.cursor()
            query = f''' SELECT * FROM {table_name} WHERE tg_id={tg_id} AND osu_mode='{osu_mode}' '''
            cursor.execute(query)
            old_db = cursor.fetchone()

            query = f''' UPDATE {table_name}
            SET tg_username='{tg_username}', 
                osu_id={osu_id},
                osu_username='{osu_username}',
                osu_pp={osu_pp},
                osu_rank={osu_rank},
                osu_acc={osu_acc},
                osu_playcount={osu_playcount},
                osu_topscore={osu_topscore},
                osu_ii={osu_ii}
            WHERE tg_id={tg_id} AND osu_mode='{osu_mode}'
            '''
            cursor.execute(query)
        
        if old_db == None:
            old_db = []
            for i in range(11):
                old_db.append(0)

        return old_db

    elif mode in ['delete', 'del']:
        with sqlite3.connect(OSU_GROUPS_DB) as db:
            cursor = db.cursor()
            query = f''' SELECT tg_username, osu_username FROM {table_name} WHERE tg_id={tg_id} '''
            cursor.execute(query)
            data = cursor.fetchone()
            if data != None:
                tg_username = data[0]
                osu_username = data[1]
                query = f''' DELETE FROM {table_name} WHERE tg_id={tg_id} '''
                cursor.execute(query)
                return f'Success: user {osu_username}({tg_username}, {tg_id}) deleted from group db'
            else:
                return 'ERROR: there is no user'











