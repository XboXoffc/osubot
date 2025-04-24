import rosu_pp_py as rosu
import config
import asyncio
from commands.osu.calculator import download_map

OSU_MAP_PATH = config.OSU_MAP_PATH

async def main(map_id, mode=None, mods=None, lazer=None, bpm=None, 
                ar=None, cs=None, hp=None, od=None, 
                passed_objects=None, accuracy=None, combo=None,
                large_tick_hits=None, small_tick_hits=None, slider_end_hits=None,
                n_geki=None, n_katu=None, n300=None, n100=None, n50=None, misses=None
):
    if await download_map.main(map_id):
        beatmap =  rosu.Beatmap(path = f"{OSU_MAP_PATH}{map_id}.osu")
        beatmap.convert(rosu.GameMode.Osu, mods)
        perf = rosu.Performance(
            lazer = lazer,
            clock_rate = bpm,
            ar = ar,
            cs = cs, 
            hp = hp,
            od = od,
            passed_objects = passed_objects,
            accuracy = accuracy,
            combo = combo,
            large_tick_hits = large_tick_hits,
            small_tick_hits = small_tick_hits,
            slider_end_hits = slider_end_hits,
            n_geki = n_geki,
            n_katu = n_katu,
            n300 = n300,
            n100 = n100,
            n50 = n50,
            misses = misses
        )
        attrs = perf.calculate(beatmap)

        perf.set_combo(None)
        perf.set_misses(None)
        attrs_fc = perf.calculate(beatmap)

        perf.set_accuracy(100)
        attrs_ss = perf.calculate(beatmap)

        perf.set_accuracy(99)
        attrs_99 = perf.calculate(beatmap)

        perf.set_accuracy(98)
        attrs_98 = perf.calculate(beatmap)

        perf.set_accuracy(97)
        attrs_97 = perf.calculate(beatmap)

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










