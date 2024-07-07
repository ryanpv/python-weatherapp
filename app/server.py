import requests
from flask import Flask, jsonify
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

API_Key = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def home_page():
  return "Hello World"

@app.route('/city/<city>', methods=['GET'])
def city_weather(city):
  base_url = "https://api.openweathermap.org/data/2.5/weather?&appid="+API_Key+"&q="+city

  result = requests.get(base_url).json()

  # if "name" not in result or "sys" not in result:
  #   return None
  
  data = {
    "Location": f"{ result.get('name') }, { result.get('sys').get('country') }",
    "Weather_Description": f"{ result.get('weather')[0].get('description') }"
  }
  pprint(result)
  return jsonify(data)

@app.route('/current')
def current_weather():
  base_url = 'https://api.openweathermap.org/data/2.5/weather?appid='+API_Key

  weather_today = requests.get(base_url).json()
  return weather_today


app.run(host="0.0.0.0", port=9000, debug=True)