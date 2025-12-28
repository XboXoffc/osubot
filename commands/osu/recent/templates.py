from commands import other
from commands.osu.calculator import pp as pp_cal

async def main(types, recent, beatmap, user, offset):
    if types == 'osu':
        return await standart(recent, beatmap, user, offset)
    elif types == 'mania':
        return await mania(recent, beatmap, user, offset)
    elif types == 'taiko':
        return await taiko(recent, beatmap, user, offset)
    elif types == 'fruits':
        return await fruits(recent, beatmap, user, offset)

async def standart(recent, beatmap, user, offset):
    text = ''
    url_base = 'https://osu.ppy.sh'
    url_users = url_base + '/users'
    url_scores = url_base + '/scores'
    username = user['username']
    userid = user['id']
    userGlobalRank = user['statistics']['global_rank']
    userCountryRank = user['statistics']['rank']['country']
    userCountryCode = user['country_code']
    beatmapsetArtist = beatmap['beatmapset']['artist']
    beatmapsetTitle = beatmap['beatmapset']['title']
    beatmapsetAuthor = beatmap['beatmapset']['creator']
    beatmapID = beatmap['id']
    beatmapURL = beatmap['url']
    beatmapVER = beatmap['version']
    beatmapDiff = round(beatmap['difficulty_rating'], 2)
    beatmapStatus = beatmap['status']
    beatmapLength = beatmap['total_length']
    beatmapAR = beatmap['ar']
    beatmapOD = beatmap['accuracy']
    beatmapCS = beatmap['cs']
    beatmapHP = beatmap['drain']
    beatmapBPM = beatmap['bpm']
    beatmapMaxCombo = beatmap['max_combo']
    beatmapCircles = beatmap['count_circles']
    beatmapSliders = beatmap['count_sliders']
    beatmapSpinners = beatmap['count_spinners']
    beatmapTotalHitObjects = beatmapCircles + beatmapSliders + beatmapSpinners
    recentID = recent['id']
    recentModsRaw = recent['mods']
    recentScore = recent['classic_total_score']
    recentMaxCombo = recent['max_combo']
    recentAccuracyRaw = recent['accuracy']
    recentAccuracy = round(recentAccuracyRaw*100, 2)
    recentStatistics = recent['statistics']
    recentPP = recent['pp']
    recentRankRaw = recent['rank']
    recentPassed = recent['passed']
    recentPassTime = recent['ended_at']
    recentTotalHits = recent["maximum_statistics"]["great"]

    recentRank = 'F'
    if recentPassed:
        recentRank = recentRankRaw  
    
    isFC = False
    if recentMaxCombo == beatmapMaxCombo:
        isFC = True

    beatmapsetArtist = beatmapsetArtist.replace('[', '')
    beatmapsetArtist = beatmapsetArtist.replace(']', '')
    beatmapsetTitle = beatmapsetTitle.replace('[', '')
    beatmapsetTitle = beatmapsetTitle.replace(']', '')
    beatmapVER = beatmapVER.replace('[', '')
    beatmapVER = beatmapVER.replace(']', '')

    beatmapMods = []
    for i in range(len(recentModsRaw)):
        beatmapMods.append(recentModsRaw[i]['acronym'])
    if beatmapMods != []:
        beatmapModsText = f'| +{''.join(beatmapMods)}'
    else:
        beatmapModsText = ''

    beatmapMin = beatmapLength//60
    beatmapSec = beatmapLength%60
    if len(str(beatmapSec)) == 1:
        beatmapTime = f'{beatmapMin}:0{beatmapSec}'
    else:
        beatmapTime = f'{beatmapMin}:{beatmapSec}'

    hits = ['great', 'ok', 'meh', 'miss']
    n300 = n100 = n50 = miss = '0'
    for hit in hits:
        value = recentStatistics.get(hit, '0')
        match hit:
            case 'great':
                n300 = value
            case 'ok':
                n100 = value
            case 'meh':
                n50 = value
            case 'miss':
                miss = value

    recentPassedPercentText = ''
    if not recentPassed:
        recentPassedPercent = round(recentTotalHits/beatmapTotalHitObjects*100, 2)
        recentPassedPercentText = f'({recentPassedPercent}%)'
    
    CalculatedScore = await pp_cal.main(beatmapID, 'osu', mods=recentModsRaw, lazer=True, accuracy=recentAccuracyRaw*100, combo=recentMaxCombo, n300=int(n300), n100=int(n100), n50=int(n50), misses=int(miss))
    if isinstance(recentPP, (int, float)):
        pp = round(recentPP, 2)
        pptext = str(pp)
    else:
        pp = round(CalculatedScore['if_rank'], 2) 
        pptext = str(pp) + '(if rank)'
    pp_fc, pp_ss, pp_99, pp_98, pp_97 = round(CalculatedScore['if_fc'], 2), round(CalculatedScore['if_ss'], 2), round(CalculatedScore['if_99'], 2), round(CalculatedScore['if_98'], 2), round(CalculatedScore['if_97'], 2)

    beatmapDiffNew = round(CalculatedScore["star_rate"], 2)

    datetime = other.time(recentPassTime)
    datetime = f'''{datetime['day']}.{datetime['month']}.{datetime['year']} {datetime['hour']}:{datetime['min']}'''


    text += f'''[{username}]({url_users}/{userid}) (Global: #{userGlobalRank}, {userCountryCode}: #{userCountryRank}) [[osu]]\n'''
    if beatmapMods == [] or beatmapMods == ['CL']:
        text += f'''[{beatmapsetArtist} - {beatmapsetTitle}]({beatmapURL}) [[{beatmapVER}, {beatmapDiff}✩]] by [{beatmapsetAuthor}] <{beatmapStatus}>\n'''
    else:
        text += f'''[{beatmapsetArtist} - {beatmapsetTitle}]({beatmapURL}) [[{beatmapVER}, {beatmapDiff}✩->{beatmapDiffNew}✩]] by [{beatmapsetAuthor}] <{beatmapStatus}>\n'''
    text += f'''{beatmapTime} | AR:{beatmapAR} OD:{beatmapOD} CS:{beatmapCS} HP:{beatmapHP} {beatmapBPM}BPM {beatmapModsText}\n'''
    text += f'''\n'''
    text += f'''Score: {recentScore} | Combo: {recentMaxCombo}/{beatmapMaxCombo} | Accuracy: {recentAccuracy}%\n'''
    if isFC:
        text += f'''*PP:* {pptext} *SS:* {pp_ss}\n'''
    elif not isFC:
        text += f'''*PP:* {pptext} *FC:* {pp_fc} *SS:* {pp_ss}\n'''
    text += f'''*99%:* {pp_99} *98%:* {pp_98} *97%:* {pp_97}\n'''
    text += f'''*300*: {n300}  *100*: {n100}  *50*: {n50}  *Miss*:{miss}\n'''
    text += f'''Rank: {recentRank} {recentPassedPercentText}\n'''
    text += f'''{datetime}\n'''
    text += f'''\n'''
    text += f'''offset: {offset} \nScore url: {url_scores}/{recentID}'''

    return text





async def mania(recent, beatmap, user, offset):
    text = ''
    url_base = 'https://osu.ppy.sh'
    url_users = url_base + '/users'
    url_scores = url_base + '/scores'
    username = user['username']
    userid = user['id']
    userGlobalRank = user['statistics']['global_rank']
    userCountryRank = user['statistics']['rank']['country']
    userCountryCode = user['country_code']
    beatmapsetArtist = beatmap['beatmapset']['artist']
    beatmapsetTitle = beatmap['beatmapset']['title']
    beatmapsetAuthor = beatmap['beatmapset']['creator']
    beatmapID = beatmap['id']
    beatmapURL = beatmap['url']
    beatmapVER = beatmap['version']
    beatmapDiff = round(beatmap['difficulty_rating'], 2)
    beatmapStatus = beatmap['status']
    beatmapLength = beatmap['total_length']
    beatmapAR = beatmap['ar']
    beatmapOD = beatmap['accuracy']
    beatmapCS = beatmap['cs']
    beatmapHP = beatmap['drain']
    beatmapBPM = beatmap['bpm']
    beatmapMaxCombo = beatmap['max_combo']
    beatmapCircles = beatmap['count_circles']
    beatmapSliders = beatmap['count_sliders']
    beatmapSpinners = beatmap['count_spinners']
    beatmapTotalHitObjects = beatmapCircles + beatmapSliders + beatmapSpinners
    recentID = recent['id']
    recentModsRaw = recent['mods']
    recentScore = recent['classic_total_score']
    recentMaxCombo = recent['max_combo']
    recentAccuracyRaw = recent['accuracy']
    recentAccuracy = round(recentAccuracyRaw*100, 2)
    recentStatistics = recent['statistics']
    recentPP = recent['pp']
    recentRankRaw = recent['rank']
    recentPassed = recent['passed']
    recentPassTime = recent['ended_at']
    recentTotalHits = recent["maximum_statistics"]["perfect"]

    recentRank = 'F'
    if recentPassed:
        recentRank = recentRankRaw  
    
    isFC = False
    if recentMaxCombo == beatmapMaxCombo:
        isFC = True

    beatmapsetArtist = beatmapsetArtist.replace('[', '')
    beatmapsetArtist = beatmapsetArtist.replace(']', '')
    beatmapsetTitle = beatmapsetTitle.replace('[', '')
    beatmapsetTitle = beatmapsetTitle.replace(']', '')
    beatmapVER = beatmapVER.replace('[', '')
    beatmapVER = beatmapVER.replace(']', '')

    beatmapMods = ''.join(recentModsRaw[i]['acronym'] for i in range(len(recentModsRaw)))
    if beatmapMods != '':
        beatmapModsText = f'| +{beatmapMods}'
    else:
        beatmapModsText = ''

    beatmapMin = beatmapLength//60
    beatmapSec = beatmapLength%60
    if len(str(beatmapSec)) == 1:
        beatmapTime = f'{beatmapMin}:0{beatmapSec}'
    else:
        beatmapTime = f'{beatmapMin}:{beatmapSec}'

    hits = ['perfect', 'great', 'good', 'ok', 'meh', 'miss']
    nMax = n300 = n200 = n100 = n50 = miss = '0'
    for hit in hits:
        value = recentStatistics.get(hit, '0')
        match hit:
            case 'perfect':
                nMax = value
            case 'great':
                n300 = value
            case 'good':
                n200 = value
            case 'ok':
                n100 = value
            case 'meh':
                n50 = value
            case 'miss':
                miss = value

    recentPassedPercentText = ''
    if not recentPassed:
        recentPassedPercent = round(recentTotalHits/beatmapTotalHitObjects*100, 2)
        recentPassedPercentText = f'({recentPassedPercent}%)'
    
    CalculatedScore = await pp_cal.main(beatmapID, 'mania', mods=recentModsRaw, lazer=True, accuracy=recentAccuracyRaw*100, combo=recentMaxCombo, n_geki=int(nMax), n300=int(n300), n_katu=int(n200), n100=int(n100), n50=int(n50), misses=int(miss))
    if isinstance(recentPP, (int, float)):
        pp = round(recentPP, 2)
        pptext = str(pp)
    else:
        pp = round(CalculatedScore['if_rank'], 2) 
        pptext = str(pp) + '(if rank)'
    pp_fc, pp_ss, pp_99, pp_98, pp_97 = round(CalculatedScore['if_fc'], 2), round(CalculatedScore['if_ss'], 2), round(CalculatedScore['if_99'], 2), round(CalculatedScore['if_98'], 2), round(CalculatedScore['if_97'], 2)

    datetime = other.time(recentPassTime)
    datetime = f'''{datetime['day']}.{datetime['month']}.{datetime['year']} {datetime['hour']}:{datetime['min']}'''


    text += f'''[{username}]({url_users}/{userid}) (Global: #{userGlobalRank}, {userCountryCode}: #{userCountryRank}) [[mania]]\n'''
    text += f'''[{beatmapsetArtist} - {beatmapsetTitle}]({beatmapURL}) [[{beatmapVER}, {beatmapDiff}✩]] by [{beatmapsetAuthor}] <{beatmapStatus}>\n'''
    text += f'''{beatmapTime} | Keys:{beatmapCS} AR:{beatmapAR} OD:{beatmapOD} HP:{beatmapHP} {beatmapBPM}BPM {beatmapModsText}\n'''
    text += f'''\n'''
    text += f'''Score: {recentScore} | Combo: {recentMaxCombo}/{beatmapMaxCombo} | Accuracy: {recentAccuracy}%\n'''
    if isFC:
        text += f'''*PP:* {pptext} *SS:* {pp_ss}\n'''
    elif not isFC:
        text += f'''*PP:* {pptext} *FC:* {pp_fc} *SS:* {pp_ss}\n'''
    text += f'''*99%:* {pp_99} *98%:* {pp_98} *97%:* {pp_97}\n'''
    text += f'''*Max*: {nMax}  *300*: {n300}  *200*: {n200}  *100*: {n100}  *50*: {n50}  *Miss*:{miss}\n'''
    text += f'''Rank: {recentRank} {recentPassedPercentText}\n'''
    text += f'''{datetime}\n'''
    text += f'''\n'''
    text += f'''offset: {offset} \nScore url: {url_scores}/{recentID}'''

    return text





async def taiko(recent, beatmap, user, offset):
    text = ''
    url_base = 'https://osu.ppy.sh'
    url_users = url_base + '/users'
    url_scores = url_base + '/scores'
    username = user['username']
    userid = user['id']
    userGlobalRank = user['statistics']['global_rank']
    userCountryRank = user['statistics']['rank']['country']
    userCountryCode = user['country_code']
    beatmapsetArtist = beatmap['beatmapset']['artist']
    beatmapsetTitle = beatmap['beatmapset']['title']
    beatmapsetAuthor = beatmap['beatmapset']['creator']
    beatmapID = beatmap['id']
    beatmapURL = beatmap['url']
    beatmapVER = beatmap['version']
    beatmapDiff = round(beatmap['difficulty_rating'], 2)
    beatmapStatus = beatmap['status']
    beatmapLength = beatmap['total_length']
    beatmapOD = recent['beatmap']['accuracy']
    beatmapHP = recent['beatmap']['drain']
    beatmapBPM = beatmap['bpm']
    beatmapMaxCombo = recent["maximum_statistics"]["great"]
    beatmapCircles = beatmap['count_circles']
    beatmapSliders = beatmap['count_sliders']
    beatmapSpinners = beatmap['count_spinners']
    beatmapTotalHitObjects = beatmapCircles + beatmapSliders + beatmapSpinners
    recentID = recent['id']
    recentModsRaw = recent['mods']
    recentScore = recent['classic_total_score']
    recentMaxCombo = recent['max_combo']
    recentAccuracyRaw = recent['accuracy']
    recentAccuracy = round(recentAccuracyRaw*100, 2)
    recentStatistics = recent['statistics']
    recentPP = recent['pp']
    recentRankRaw = recent['rank']
    recentPassed = recent['passed']
    recentPassTime = recent['ended_at']
    recentTotalHits = recent["maximum_statistics"]["great"]

    recentRank = 'F'
    if recentPassed:
        recentRank = recentRankRaw  
    
    isFC = False
    if recentMaxCombo == beatmapMaxCombo:
        isFC = True

    beatmapsetArtist = beatmapsetArtist.replace('[', '')
    beatmapsetArtist = beatmapsetArtist.replace(']', '')
    beatmapsetTitle = beatmapsetTitle.replace('[', '')
    beatmapsetTitle = beatmapsetTitle.replace(']', '')
    beatmapVER = beatmapVER.replace('[', '')
    beatmapVER = beatmapVER.replace(']', '')

    beatmapMods = ''.join(recentModsRaw[i]['acronym'] for i in range(len(recentModsRaw)))
    if beatmapMods != '':
        beatmapModsText = f'| +{beatmapMods}'
    else:
        beatmapModsText = ''

    beatmapMin = beatmapLength//60
    beatmapSec = beatmapLength%60
    if len(str(beatmapSec)) == 1:
        beatmapTime = f'{beatmapMin}:0{beatmapSec}'
    else:
        beatmapTime = f'{beatmapMin}:{beatmapSec}'

    hits = ['great', 'ok', 'miss']
    n300 = n100 = miss = '0'
    for hit in hits:
        value = recentStatistics.get(hit, '0')
        match hit:
            case 'great':
                n300 = value
            case 'ok':
                n100 = value
            case 'miss':
                miss = value

    recentPassedPercentText = ''
    if not recentPassed:
        recentPassedPercent = round(recentTotalHits/beatmapTotalHitObjects*100, 2)
        recentPassedPercentText = f'({recentPassedPercent}%)'
    
    CalculatedScore = await pp_cal.main(beatmapID, 'taiko', mods=recentModsRaw, lazer=True, accuracy=recentAccuracyRaw*100, combo=recentMaxCombo, n300=int(n300), n100=int(n100), misses=int(miss))
    if isinstance(recentPP, (int, float)):
        pp = round(recentPP, 2)
        pptext = str(pp)
    else:
        pp = round(CalculatedScore['if_rank'], 2) 
        pptext = str(pp) + '(if rank)'
    pp_fc, pp_ss, pp_99, pp_98, pp_97 = round(CalculatedScore['if_fc'], 2), round(CalculatedScore['if_ss'], 2), round(CalculatedScore['if_99'], 2), round(CalculatedScore['if_98'], 2), round(CalculatedScore['if_97'], 2)

    datetime = other.time(recentPassTime)
    datetime = f'''{datetime['day']}.{datetime['month']}.{datetime['year']} {datetime['hour']}:{datetime['min']}'''


    text += f'''[{username}]({url_users}/{userid}) (Global: #{userGlobalRank}, {userCountryCode}: #{userCountryRank}) [[taiko]]\n'''
    text += f'''[{beatmapsetArtist} - {beatmapsetTitle}]({beatmapURL}) [[{beatmapVER}, {beatmapDiff}✩]] by [{beatmapsetAuthor}] <{beatmapStatus}>\n'''
    text += f'''{beatmapTime} | OD:{beatmapOD} HP:{beatmapHP} {beatmapBPM}BPM {beatmapModsText}\n'''
    text += f'''\n'''
    text += f'''Score: {recentScore} | Combo: {recentMaxCombo}/{beatmapMaxCombo} | Accuracy: {recentAccuracy}%\n'''
    if isFC:
        text += f'''*PP:* {pptext} *SS:* {pp_ss}\n'''
    elif not isFC:
        text += f'''*PP:* {pptext} *FC:* {pp_fc} *SS:* {pp_ss}\n'''
    text += f'''*99%:* {pp_99} *98%:* {pp_98} *97%:* {pp_97}\n'''
    text += f'''*300*: {n300}  *100*: {n100}  *Miss*:{miss}\n'''
    text += f'''Rank: {recentRank} {recentPassedPercentText}\n'''
    text += f'''{datetime}\n'''
    text += f'''\n'''
    text += f'''offset: {offset} \nScore url: {url_scores}/{recentID}'''

    return text





async def fruits(recent, beatmap, user, offset):
    text = ''
    url_base = 'https://osu.ppy.sh'
    url_users = url_base + '/users'
    url_scores = url_base + '/scores'
    username = user['username']
    userid = user['id']
    userGlobalRank = user['statistics']['global_rank']
    userCountryRank = user['statistics']['rank']['country']
    userCountryCode = user['country_code']
    beatmapsetArtist = beatmap['beatmapset']['artist']
    beatmapsetTitle = beatmap['beatmapset']['title']
    beatmapsetAuthor = beatmap['beatmapset']['creator']
    beatmapID = beatmap['id']
    beatmapURL = beatmap['url']
    beatmapVER = beatmap['version']
    beatmapDiff = round(beatmap['difficulty_rating'], 2)
    beatmapStatus = beatmap['status']
    beatmapLength = beatmap['total_length']
    beatmapAR = beatmap['ar']
    beatmapOD = beatmap['accuracy']
    beatmapCS = beatmap['cs']
    beatmapHP = beatmap['drain']
    beatmapBPM = beatmap['bpm']
    recentID = recent['id']
    recentModsRaw = recent['mods']
    recentScore = recent['classic_total_score']
    recentMaxCombo = recent['max_combo']
    recentAccuracyRaw = recent['accuracy']
    recentAccuracy = round(recentAccuracyRaw*100, 2)
    recentStatistics = recent['statistics']
    recentPP = recent['pp']
    recentRankRaw = recent['rank']
    recentPassed = recent['passed']
    recentPassTime = recent['ended_at']
    recentTotalHits = recent["maximum_statistics"]["great"]

    recentRank = 'F'
    if recentPassed:
        recentRank = recentRankRaw  

    beatmapsetArtist = beatmapsetArtist.replace('[', '')
    beatmapsetArtist = beatmapsetArtist.replace(']', '')
    beatmapsetTitle = beatmapsetTitle.replace('[', '')
    beatmapsetTitle = beatmapsetTitle.replace(']', '')
    beatmapVER = beatmapVER.replace('[', '')
    beatmapVER = beatmapVER.replace(']', '')

    beatmapMods = ''.join(recentModsRaw[i]['acronym'] for i in range(len(recentModsRaw)))
    if beatmapMods != '':
        beatmapModsText = f'| +{beatmapMods}'
    else:
        beatmapModsText = ''

    beatmapMin = beatmapLength//60
    beatmapSec = beatmapLength%60
    if len(str(beatmapSec)) == 1:
        beatmapTime = f'{beatmapMin}:0{beatmapSec}'
    else:
        beatmapTime = f'{beatmapMin}:{beatmapSec}'

    hits = ['great', "large_tick_hit", "small_tick_hit", "small_tick_miss", 'miss']
    n300 = large_tick_hit = small_tick_hit = small_tick_miss = miss = '0'
    for hit in hits:
        value = recentStatistics.get(hit, '0')
        match hit:
            case 'great':
                n300 = value
            case 'large_tick_hit':
                large_tick_hit = value
            case 'small_tick_hit':
                small_tick_hit = value
            case 'small_tick_miss':
                small_tick_miss = value
            case 'miss':
                miss = value

    CalculatedScore = await pp_cal.main(beatmapID, 'fruits', mods=recentModsRaw, lazer=True, accuracy=recentAccuracyRaw*100, combo=recentMaxCombo, n300=int(n300), misses=int(miss), n100=int(large_tick_hit), n50=int(small_tick_hit), n_katu=int(small_tick_miss))
    if isinstance(recentPP, (int, float)):
        pp = round(recentPP, 2)
        pptext = str(pp)
    else:
        pp = round(CalculatedScore['if_rank'], 2) 
        pptext = str(pp) + '(if rank)'
    pp_fc, pp_ss, pp_99, pp_98, pp_97 = round(CalculatedScore['if_fc'], 2), round(CalculatedScore['if_ss'], 2), round(CalculatedScore['if_99'], 2), round(CalculatedScore['if_98'], 2), round(CalculatedScore['if_97'], 2)
    beatmapMaxCombo = beatmapTotalHitObjects = CalculatedScore['max_combo']

    recentPassedPercentText = ''
    if not recentPassed:
        recentPassedPercent = round(recentTotalHits/beatmapTotalHitObjects*100, 2)
        recentPassedPercentText = f'({recentPassedPercent}%)'

    datetime = other.time(recentPassTime)
    datetime = f'''{datetime['day']}.{datetime['month']}.{datetime['year']} {datetime['hour']}:{datetime['min']}'''


    text += f'''[{username}]({url_users}/{userid}) (Global: #{userGlobalRank}, {userCountryCode}: #{userCountryRank}) [[fruits]]\n'''
    text += f'''[{beatmapsetArtist} - {beatmapsetTitle}]({beatmapURL}) [[{beatmapVER}, {beatmapDiff}✩]] by [{beatmapsetAuthor}] <{beatmapStatus}>\n'''
    text += f'''{beatmapTime} | AR:{beatmapAR} OD:{beatmapOD} CS:{beatmapCS} HP:{beatmapHP} {beatmapBPM}BPM {beatmapModsText}\n'''
    text += f'''\n'''
    text += f'''Score: {recentScore} | Combo: {recentMaxCombo}/{beatmapMaxCombo} | Accuracy: {recentAccuracy}%\n'''
    text += f'''*PP:* {pptext} *SS:* {pp_ss}\n'''
    text += f'''*99%:* {pp_99} *98%:* {pp_98} *97%:* {pp_97}\n'''
    text += f'''*Great*: {n300}  *Miss*:{miss}\n'''
    text += f'''Rank: {recentRank} {recentPassedPercentText}\n'''
    text += f'''{datetime}\n'''
    text += f'''\n'''
    text += f'''offset: {offset} \nScore url: {url_scores}/{recentID}'''

    return text