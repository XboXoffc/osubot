async def grouptop(message, MembersTop, limit, osu_mode, sortby):
    #tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore
    avg_pp, avg_rank, avg_acc, avg_playcount, avg_topscore, avg_ii = [],[],[],[],[],[]
    new_limit = limit
    if len(MembersTop) < limit:
        new_limit = len(MembersTop)
    text = ''
    text += f"""Top-{new_limit} of chat members sorted by {sortby} in {message.chat.id} ({osu_mode}):\n"""

    for i in range(new_limit):
        memberdata = MembersTop[i]
        tg_id, tg_username = memberdata[0], memberdata[1]
        osu_id, osu_username = memberdata[2], memberdata[3].replace('_', ' ')
        osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore, osu_ii = round(memberdata[5], 2), memberdata[6], round(memberdata[7], 2), memberdata[8], round(memberdata[9], 2) if memberdata[9] != None else "null", round(memberdata[10], 2) if memberdata[10] != None else "null"

        avg_pp.append(osu_pp)
        avg_rank.append(osu_rank)
        avg_acc.append(osu_acc)
        avg_playcount.append(osu_playcount)
        avg_topscore.append(osu_topscore)
        avg_ii.append(osu_ii)


        text += f'''#{i+1} [{osu_username}](https://t.me/{tg_username}) {osu_pp}pp | #{osu_rank} |'''
        text += f''' {osu_acc}% | {osu_playcount} plays | {osu_topscore}↑pp | {osu_ii} ii\n'''

    if len(MembersTop) > limit:
        text += f'''...#{len(MembersTop)}...'''

    while True:
        try:
            avg_topscore.pop(avg_topscore.index('null'))
        except:
            break
    while True:
        try:
            avg_ii.pop(avg_ii.index('null'))
        except:
            break
    avg_pp = round(sum(avg_pp) / len(avg_pp), 2)
    avg_rank = round(sum(avg_rank) / len(avg_rank))
    avg_acc = round(sum(avg_acc) / len(avg_acc), 2)
    avg_playcount = round(sum(avg_playcount) / len(avg_playcount))
    try:
        avg_topscore = round(sum(avg_topscore) / len(avg_topscore), 2)
    except ZeroDivisionError:
        avg_topscore = 'null'
    try:
        avg_ii = round(sum(avg_ii) / len(avg_ii), 2)
    except ZeroDivisionError:
        avg_ii = 'null'

    text += f'''\nAVG: {avg_pp}pp | #{avg_rank} | {avg_acc}% | {avg_playcount} plays | {avg_topscore}↑pp | {avg_ii} ii'''

    return text


async def update(message, old_db, new_db):
    #tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore, osu_ii
    text = ''
    base_url = 'https://osu.ppy.sh'
    tg_id = new_db[0]
    osu_id = new_db[2]
    osu_username = new_db[3]
    osu_mode = new_db[4]

    text += f'''[{osu_username}'s]({base_url}/users/{osu_id}) update in {message.chat.id} ({osu_mode}):\n'''

    if old_db[5] != None:
        dif_pp = new_db[5] - old_db[5]
    else:
        dif_pp = new_db[5]
    if dif_pp >= 0:
        dif_pp = '+' + str(dif_pp)
    text += f'''pp: {new_db[5]}({dif_pp})\n'''

    if old_db[6] != None:
        dif_rank = new_db[6] - old_db[6]
    else:
        dif_rank = new_db[6]
    if dif_rank >= 0:
        dif_rank = '+' + str(dif_rank)
    text += f'''rank: {new_db[6]}({dif_rank})\n'''

    if old_db[7] != None:
        dif_acc = new_db[7] - old_db[7]
    else:
        dif_acc = new_db[7]
    if dif_acc >= 0:
        dif_acc = '+' + str(round(dif_acc, 2))
    text += f'''acc: {round(new_db[7], 2)}({dif_acc})\n'''

    if old_db[8] != None:
        dif_playcount = new_db[8] - old_db[8]
    else:
        dif_playcount = new_db[8]
    if dif_playcount >= 0:
        dif_playcount = '+' + str(dif_playcount)
    text += f'''playcount: {new_db[8]}({dif_playcount})\n'''

    if old_db[9] != None:
        dif_topscore = new_db[9] - old_db[9]
    else:
        dif_topscore = new_db[9]
    if dif_topscore >= 0:
        dif_topscore = '+' + str(dif_topscore)
    text += f'''topscore: {new_db[9]}({dif_topscore})\n'''

    if old_db[10] != None:
        dif_ii = new_db[10] - old_db[10]
    else:
        dif_ii = new_db[10]
    if dif_ii >= 0:
        dif_ii = '+' + str(dif_ii)
    text += f'''ii: {new_db[10]}({dif_ii})\n'''


    return text