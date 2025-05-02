import requests
import config
import asyncio
import os.path
import os

OSU_MAP_PATH = config.OSU_MAP_PATH 

async def main(map_id):
    base_url = 'https://osu.ppy.sh/osu'
    path_to_map = f'{OSU_MAP_PATH}{map_id}.osu'
    try:
        mapdata = requests.get(f'{base_url}/{map_id}')
    except:
        mapdata = None

    if mapdata != None:
        mapdata = mapdata.text
        if os.path.exists(path_to_map):
            os.remove(path_to_map)
        with open(path_to_map, 'x') as file:
            file.write(mapdata)
    elif mapdata == None:
        await main(map_id)

    return True








