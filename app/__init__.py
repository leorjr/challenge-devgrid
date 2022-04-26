from functools import cache
from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from cachetools import cached, TTLCache
from app.functions import get_informations_city, get_data_cached

load_dotenv()


cache = TTLCache(
    maxsize=int(os.environ['DEFAULT_MAX_NUMBER']), ttl=float(os.environ['CACHE_TTL']))


app = Flask(__name__)


@app.route('/temperature/<city>')
@cached(cache)
def get_temperature_city(city):

    info = get_informations_city(city)

    return jsonify(info)


@app.route("/temperature")
def get_cached_temperature():

    data_to_return = get_data_cached()

    return jsonify(data_to_return)
