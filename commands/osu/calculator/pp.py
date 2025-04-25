import rosu_pp_py as rosu
import config
import asyncio
from commands.osu.calculator import download_map

OSU_MAP_PATH = config.OSU_MAP_PATH

async def main(map_id, mode=None, mods=None, lazer=None, clockrate=None, 
                ar=None, cs=None, hp=None, od=None, 
                passed_objects=None, accuracy=None, combo=None,
                large_tick_hits=None, small_tick_hits=None, slider_end_hits=None,
                n_geki=None, n_katu=None, n300=None, n100=None, n50=None, misses=None
):
    if await download_map.main(map_id):
        beatmap =  rosu.Beatmap(path = f"{OSU_MAP_PATH}{map_id}.osu")
        beatmap.convert(rosu.GameMode.Osu)
        attrs = rosu.Performance(
            mods = mods,
            lazer = lazer,
            clock_rate = clockrate,
            accuracy = accuracy,
            combo = combo,
            n300 = n300,
            n100 = n100,
            n50 = n50,
            misses = misses
        ).calculate(beatmap)

        attrs_fc = rosu.Performance(
            mods = mods,
            lazer = lazer,
            clock_rate = clockrate,
            accuracy = accuracy,
            combo = combo + misses,
            n300 = n300 + misses,
            n100 = n100,
            n50 = n50
        ).calculate(beatmap)

        attrs_ss = rosu.Performance(
            mods = mods,
            lazer = lazer,
            clock_rate = clockrate,
            accuracy = 100
        ).calculate(beatmap)

        attrs_99 = rosu.Performance(
            mods = mods,
            lazer = lazer,
            clock_rate = clockrate,
            accuracy = 99
        ).calculate(beatmap)

        attrs_98 = rosu.Performance(
            mods = mods,
            lazer = lazer,
            clock_rate = clockrate,
            accuracy = 98
        ).calculate(beatmap)

        attrs_97 = rosu.Performance(
            mods = mods,
            lazer = lazer,
            clock_rate = clockrate,
            accuracy = 97
        ).calculate(beatmap)

        answer = {
            "if_rank": attrs.pp,
            "if_fc": attrs_fc.pp,
            "if_ss": attrs_ss.pp,
            "if_99": attrs_99.pp,
            "if_98": attrs_98.pp,
            "if_97": attrs_97.pp
        }

        return answer
    
    else:
        return False










