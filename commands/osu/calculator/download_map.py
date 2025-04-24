import requests
import config
import asyncio
import os.path

OSU_MAP_PATH = config.OSU_MAP_PATH 

async def main(map_id):
    try:
        base_url = 'https://osu.ppy.sh/osu'
        mapdata = requests.get(f'{base_url}/{map_id}').text
        if os.path.exists(f'{OSU_MAP_PATH}{map_id}.osu'):
            with open(f'{OSU_MAP_PATH}{map_id}.osu', 'w') as file:
                file.write(mapdata)
        else:
            with open(f'{OSU_MAP_PATH}{map_id}.osu', 'x') as file:
                file.write(mapdata)

        return True
    except:
        return False








