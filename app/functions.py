import json
import os
from flask import request
import requests


def read_file():
    with open("./data.json", "r") as file:
        data = json.load(file)

    return data


def write_file(data_to_append):
    with open("./data.json", "w") as file:
        json.dump(data_to_append, file)


def convert_to_celsius(info):
    return round((273 - info) * -1, 2)


def get_informations_city(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ['API_KEY']}"

    response = requests.get(url).json()

    info = {
        "name": city,
        "country": response["sys"]["country"],
        "main": {
            "feels_like": convert_to_celsius(response["main"]["feels_like"]),
            "temp_avg": convert_to_celsius(response["main"]["temp"]),
            "temp_max": convert_to_celsius(response["main"]["temp_max"]),
            "temp_min": convert_to_celsius(response["main"]["temp_min"]),
        },
    }

    data = read_file()

    data.append(info)

    write_file(data)

    return info


def get_data_cached():
    param_max = int(os.environ["DEFAULT_MAX_NUMBER"])

    if request.args:
        param_max = int(request.args.get("max"))

    data = read_file()

    data_to_return = data[0:param_max]

    return data_to_return
