async def main(message, MembersTop, limit, osu_mode, sortby):
    #tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore
    avg_pp, avg_rank, avg_acc, avg_playcount, avg_topscore = [],[],[],[],[]
    new_limit = limit
    if len(MembersTop) < limit:
        new_limit = len(MembersTop)
    text = ''
    text += f"""Top-{new_limit} of chat members sorted by {sortby} in {message.chat.id} ({osu_mode}):\n"""

    for i in range(new_limit):
        memberdata = MembersTop[i]
        tg_id, tg_username = memberdata[0], memberdata[1]
        osu_id, osu_username = memberdata[2], memberdata[3].replace('_', ' ')
        osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore = round(memberdata[5], 2), memberdata[6], round(memberdata[7], 2), memberdata[8], round(memberdata[9], 2) if memberdata[9] != None else "null"

        avg_pp.append(osu_pp)
        avg_rank.append(osu_rank)
        avg_acc.append(osu_acc)
        avg_playcount.append(osu_playcount)
        avg_topscore.append(osu_topscore)

        text += f'''#{i+1} [{osu_username}](https://t.me/{tg_username}) {osu_pp}pp | #{osu_rank} |'''
        text += f''' {osu_acc}% | {osu_playcount} plays | {osu_topscore}↑pp\n'''

    if len(MembersTop) > limit:
        text += f'''...#{len(MembersTop)}...'''

    while True:
        try:
            avg_topscore.pop(avg_topscore.index('null'))
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
    text += f'''\nAVG: {avg_pp}pp | #{avg_rank} | {avg_acc}% | {avg_playcount} plays | {avg_topscore}↑pp'''

    return text