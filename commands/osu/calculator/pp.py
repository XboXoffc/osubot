import osu_tools as ot
import config
import asyncio
from commands.osu.calculator import download_map
from commands.osu.utils.fetch import ruleset_convert

OSU_MAP_PATH = config.OSU_MAP_PATH

async def main(map_id, mode=None, mods=None, lazer=None, clockrate=None, 
                ar=None, cs=None, hp=None, od=None, 
                passed_objects=None, accuracy=None, combo=None,
                large_tick_hits=0, small_tick_hits=0, small_tick_miss=0, slider_end_hits=0,
                n_geki=0, n_katu=0, n300=0, n100=0, n50=0, misses=0, statistics=None
):
    if await download_map.main(map_id):
        beatmap = ot.OsuCalculator()
        mode_int = await ruleset_convert(mode)
        
        if mode == 'osu':
            attrs = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                combo = combo,
                statistics = statistics
            )

            statistics['miss'] = 0
            attrs_fc = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                statistics = statistics
            )
        elif mode == 'mania':
            attrs = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                combo = combo,
                statistics = statistics
            )

            statistics['miss'] = 0
            attrs_fc = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                statistics = statistics
            )
        elif mode == 'taiko':
            attrs = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                combo = combo,
                statistics = statistics
            )

            statistics['miss'] = 0
            attrs_fc = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                statistics = statistics
            )
        elif mode == 'fruits':
            attrs = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                combo = combo,
                statistics = statistics
            )

            statistics['miss'] = 0
            attrs_fc = beatmap.calculate(
                file_path = f"{OSU_MAP_PATH}{map_id}.osu",
                mode = mode_int,
                mods = mods,
                acc = accuracy,
                statistics = statistics
            )
        
        attrs_ss = beatmap.calculate(
            file_path = f"{OSU_MAP_PATH}{map_id}.osu",
            mode = mode_int,
            mods = mods,
            acc = 100.0
        )

        attrs_99 = beatmap.calculate(
            file_path = f"{OSU_MAP_PATH}{map_id}.osu",
            mode = mode_int,
            mods = mods,
            acc = 99.0
        )

        attrs_98 = beatmap.calculate(
            file_path = f"{OSU_MAP_PATH}{map_id}.osu",
            mode = mode_int,
            mods = mods,
            acc = 98.0
        )

        attrs_97 = beatmap.calculate(
            file_path = f"{OSU_MAP_PATH}{map_id}.osu",
            mode = mode_int,
            mods = mods,
            acc = 97.0
        )

        answer = {
            "if_rank": attrs.pp,
            "if_fc": attrs_fc.pp,
            "if_ss": attrs_ss.pp,
            "if_99": attrs_99.pp,
            "if_98": attrs_98.pp,
            "if_97": attrs_97.pp,
            "max_combo": attrs_ss.max_combo,
            "star_rate": attrs_ss.stars
        }

        return answer
    
    else:
        return False










