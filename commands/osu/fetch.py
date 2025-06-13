def mode(osumode, msgsplit, all_modes):
    osumode = next((m for m in msgsplit if m in set(all_modes)), osumode)
    if osumode in ("-std", '-osu'):
        osumode = 'osu'
    elif osumode in ('-m', '-mania'):
        osumode = 'mania'
    elif osumode in ('-t', '-taiko'):
        osumode = 'taiko'
    elif osumode in ('-c' or '-ctb' or '-catch'):
        osumode = 'fruits'

    return osumode

def sort(sortby, msgsplit, all_sorts):
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