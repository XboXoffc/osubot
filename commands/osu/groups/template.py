async def main(message, MembersTop, limit, osu_mode, sortby):
    #tg_id, tg_username, osu_id, osu_username, osu_mode, osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore
    if len(MembersTop) < limit:
        limit = len(MembersTop)
    text = ''
    text += f"""Top-{limit} of chat members sorted by {sortby} in {message.chat.id} ({osu_mode}):\n"""
    for i in range(limit):
        memberdata = MembersTop[i]
        tg_id, tg_username = memberdata[0], memberdata[1]
        osu_id, osu_username = memberdata[2], memberdata[3].replace('_', ' ')
        osu_pp, osu_rank, osu_acc, osu_playcount, osu_topscore = round(memberdata[5], 2), memberdata[6], round(memberdata[7], 2), memberdata[8], round(memberdata[9], 2) if memberdata[9] != None else "null"

        text += f'''#{i+1} [{osu_username}](https://t.me/{tg_username}) {osu_pp}pp | Rank #{osu_rank}\n'''
        text += f'''{osu_acc}% | {osu_playcount} plays | {osu_topscore}↑pp\n'''

    return text