from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from cachetools import cached, TTLCache
import requests

load_dotenv()

cache = TTLCache(
    maxsize=os.environ['DEFAULT_MAX_NUMBER'], ttl=os.environ['CACHE_TTL'])

app = Flask(__name__)


@app.route('/temperature/<city>')
@cached(cache)
def home(city):

    link_request = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ['API_KEY']}"
    response = requests.get(link_request).json()

    return jsonify(response)
