from time import sleep
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from cachetools import TLRUCache, cached, TTLCache
import requests
import json

load_dotenv()


def read_file():
    with open("./data.json", "r") as file:
        data = json.load(file)

    return data


def write_file(data_to_append):
    with open("./data.json", "w") as file:
        json.dump(data_to_append, file)


cache = TTLCache(
    maxsize=int(os.environ['DEFAULT_MAX_NUMBER']), ttl=float(os.environ['CACHE_TTL']))


app = Flask(__name__)


@app.route('/temperature/<city>')
@cached(cache)
def get_temperature_city(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ['API_KEY']}"

    response = requests.get(url).json()

    info = {
        "name": response["name"],
        "country": response["sys"]["country"],
        "main": {
            "feels_like": response["main"]["feels_like"],
            "temp_avg": response["main"]["temp"],
            "temp_max": response["main"]["temp_max"],
            "temp_min": response["main"]["temp_min"],
        },
    }

    data = read_file()

    data.append(info)
    write_file(data)

    return jsonify(info)


@app.route("/temperature")
def get_cached_temperature():

    param_max = int(os.environ["DEFAULT_MAX_NUMBER"])

    if request.args:
        param_max = int(request.args.get("max"))

    data = read_file()

    data_to_return = data[0:param_max]
    return jsonify(data_to_return)
