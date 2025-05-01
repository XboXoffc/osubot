from commands import other
from commands.osu.calculator import pp as pp_cal

async def recent(recent, beatmap, user, offset):
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
    beatmapDiff = beatmap['difficulty_rating']
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
    
    CalculatedPP = await pp_cal.main(beatmapID, mods=recentModsRaw, lazer=True, accuracy=recentAccuracyRaw*100, combo=recentMaxCombo, n300=int(n300), n100=int(n100), n50=int(n50), misses=int(miss))
    if isinstance(recentPP, (int, float)):
        pp = round(recentPP, 2)
        pptext = str(pp)
    else:
        pp = round(CalculatedPP['if_rank'], 2) 
        pptext = str(pp) + '(if rank)'
    pp_fc, pp_ss, pp_99, pp_98, pp_97 = round(CalculatedPP['if_fc'], 2), round(CalculatedPP['if_ss'], 2), round(CalculatedPP['if_99'], 2), round(CalculatedPP['if_98'], 2), round(CalculatedPP['if_97'], 2)

    datetime = other.time(recentPassTime)
    datetime = f'''{datetime['day']}.{datetime['month']}.{datetime['year']} {datetime['hour']}:{datetime['min']}'''


    text += f'''[{username}]({url_users}/{userid}) (Global: #{userGlobalRank}, {userCountryCode}: #{userCountryRank})\n'''
    text += f'''[{beatmapsetArtist} - {beatmapsetTitle}]({beatmapURL}) [[{beatmapVER}, {beatmapDiff}✩]] by [{beatmapsetAuthor}] <{beatmapStatus}>\n'''
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