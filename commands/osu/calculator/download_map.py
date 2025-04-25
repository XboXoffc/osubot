import requests
import config
import asyncio
import os.path

OSU_MAP_PATH = config.OSU_MAP_PATH 

async def main(map_id):
    base_url = 'https://osu.ppy.sh/osu'
    try:
        mapdata = requests.get(f'{base_url}/{map_id}')
    except:
        mapdata = None

    if mapdata != None:
        mapdata = mapdata.text
        try:
            with open(f'{OSU_MAP_PATH}{map_id}.osu', 'x') as file:
                file.write(mapdata)
        except:
            with open(f'{OSU_MAP_PATH}{map_id}.osu', 'w') as file:
                file.write(mapdata)
    elif mapdata == None:
        await main(map_id)

    return True








