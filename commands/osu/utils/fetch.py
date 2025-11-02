import sqlite3

async def mode(osumode:str, msgsplit:list, all_modes:list, send_index=False):
    osumoderaw = next((m for m in msgsplit if m in set(all_modes)), osumode)
    if osumoderaw in ("-std", '-osu'):
        osumode = 'osu'
    elif osumoderaw in ('-m', '-mania'):
        osumode = 'mania'
    elif osumoderaw in ('-t', '-taiko'):
        osumode = 'taiko'
    elif osumoderaw in ('-c', '-ctb', '-catch'):
        osumode = 'fruits'

    index = None
    if osumoderaw in msgsplit:
        index = msgsplit.index(osumoderaw)

    if send_index:
        return osumode, index
    elif not send_index:
        return osumode

async def sort(sortby, msgsplit, all_sorts):
    sortby = next((m for m in msgsplit if m in set(all_sorts)), sortby)
    if sortby in ('-pp'):
        sortby = 'osu_pp'
    elif sortby in ('-rank'):
        sortby = 'osu_rank'
    elif sortby in ('-acc'):
        sortby = 'osu_acc'
    elif sortby in ('-pc'):
        sortby = 'osu_playcount'
    elif sortby in ('-ts'):
        sortby = 'osu_topscore'
    elif sortby in ('-ii'):
        sortby = 'osu_ii'
    
    return sortby

async def user(tg_id, OSU_USERS_DB):
    user = None
    with sqlite3.connect(OSU_USERS_DB) as db:
        cursor = db.cursor()
        query = f""" SELECT * FROM osu_users WHERE tg_id={tg_id} """
        cursor.execute(query)
        user = cursor.fetchone()
    
    return user