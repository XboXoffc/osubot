async def compare(profile_list:list, top_list:list, ii_list:list, osumode:str):
    text = ''
    osuid = [None, None]; osunick = [None, None]; osuurl = [None, None]; pp = [None, None]; rank = [None, None]; acc = [None, None]; playcount = [None, None]; playtime = [None, None]; topscore = [None, None]; ii = [None, None]
    for i in range(2):
        osuid[i] = 'ID' + str(profile_list[i]['id'])
        osunick[i] = profile_list[i]['username']
        osuurl[i] = f'https://osu.ppy.sh/users/{profile_list[i]['id']}'
        pp[i] = round(profile_list[i]['statistics']['pp'], 2)
        rank[i] = '#' + str(profile_list[i]['statistics']['global_rank'])
        acc[i] = str(round(profile_list[i]['statistics']['hit_accuracy'], 2)) + '%'
        playcount[i] = profile_list[i]['statistics']['play_count']
        playtime[i] = str(profile_list[i]['statistics']['play_time']//3600) + 'h'
        topscore[i] = round(top_list[i][0]['pp'], 2)
        ii[i] = ii_list[i]

    async def space(mode):
        space = ' ' * (len(str(osunick[0])) + 7 - len(str(mode)))
        return space

    text += '```\n'
    text += f'''Сompare of  {osunick[0]}  and  {osunick[1]} ({osumode})\n'''
    text += f'''ID:         {osuid[0]}{await space(osuid[0])}{osuid[1]}\n'''
    text += f'''PP:         {pp[0]}{await space(pp[0])}{pp[1]}\n'''
    text += f'''Rank:       {rank[0]}{await space(rank[0])}{rank[1]}\n'''
    text += f'''Accuracy:   {acc[0]}{await space(acc[0])}{acc[1]}\n'''
    text += f'''PlayCount:  {playcount[0]}{await space(playcount[0])}{playcount[1]}\n'''
    text += f'''PlayTime:   {playtime[0]}{await space(playtime[0])}{playtime[1]}\n'''
    text += f'''Top Score:  {topscore[0]}{await space(topscore[0])}{topscore[1]}\n'''
    text += f'''ii:         {ii[0]}{await space(ii[0])}{ii[1]}\n'''
    text += '```\n'

    return text






