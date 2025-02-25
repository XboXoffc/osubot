from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests
import config
from commands import other
import sqlite3

API_KEY = config.WHEATHER_API
DB_PATH = config.WHEATHER_DB_PATH
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

def isempty(list: list or tuple, index: int):
    try:
        trash = list[index]
        return False
    except:
        return True

async def main(message):
    message_split = message.text.split(" ")
    try:
        if not isempty(message_split, 1) and message_split[1][0] == '+':
            city = message_split[1]
            city.removeprefix('+')
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.cursor()
                query = ''' CREATE TABLE IF NOT EXISTS users_city(
                    tg_id INTEGER UNIQUE,
                    tg_user TEXT,
                    city TEXT
                    ) '''
                query1 = f'''  REPLACE INTO users_city(tg_id, tg_user, city) VALUES({message.from_user.id}, "{message.from_user.username}", "{city}") '''
                cursor.execute(query)
                cursor.execute(query1)
        elif isempty(message_split, 1):
            with sqlite3.connect(DB_PATH) as db:
                cursor = db.cursor()
                query = '''  SELECT tg_id, city FROM users_city  '''
                cursor.execute(query)
                users_city = cursor.fetchall()
                for data in users_city:
                    if message.from_user.id == data[0]:
                        city = data[1]
                        break
        else:
            city = message_split[1]
        flags = message_split
        days = 2
        api_key=API_KEY
        base_url = "http://api.weatherapi.com/v1/forecast.json"
        params = {
        "key": api_key,
        "q": city,
        "days": days
        }
        response = requests.get(base_url, params)
        if response.status_code == 200:
            data = response.json()
            location = data["location"]
            current = data["current"]
            forecast = data["forecast"]["forecastday"]
        #flags for weather
            if "-add" in flags or "-a" in flags:
                text = f"""*{location["localtime"]}*
*{location["country"]}, {location["region"]}, {location["name"]}*
*Current:*
    {current["condition"]["text"]}
    temp: {current["temp_c"]}°C
    rain chance: {forecast[0]["day"]["daily_chance_of_rain"]}%
    snow chance: {forecast[0]["day"]["daily_chance_of_snow"]}%
*Tomorrow({forecast[1]["date"]}):*
    {forecast[1]["day"]["condition"]["text"]}
    max temp: {forecast[1]["day"]["maxtemp_c"]}°C
    min temp: {forecast[1]["day"]["mintemp_c"]}°C
    avg temp: {forecast[1]["day"]["avgtemp_c"]}°C
    rain chance: {forecast[1]["day"]["daily_chance_of_rain"]}%
    snow chance: {forecast[1]["day"]["daily_chance_of_snow"]}%"""
                await bot.send_message(message.chat.id, text, "MARKDOWN")

            else:
                text = f"""*{location["localtime"]}*
*{location["country"]}, {location["region"]}, {location["name"]}*
    {current["condition"]["text"]}
    temp: {current["temp_c"]}°C
    rain chance: {forecast[0]["day"]["daily_chance_of_rain"]}%
    snow chance: {forecast[0]["day"]["daily_chance_of_snow"]}%"""
                await bot.send_message(message.chat.id, text, "MARKDOWN")
                
            if "-p" in flags:
                text = "it is easter egg -- pashalko"
                await bot.send_message(message.chat.id, text, "MARKDOWN")
        else:
            response = response.json()
            await bot.send_message(message.chat.id, f"api is not work\n{response}", timeout=20)
    except Exception as e:
        await bot.send_message(message.chat.id, "Вы не указали город, добавьте свой город указав '+' в начале города")
        print(e)


print("Cogs | weather.py is ready")