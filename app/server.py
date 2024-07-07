import requests
from flask import Flask, jsonify, request
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

API_Key = os.getenv('API_KEY')

app = Flask(__name__)
print('app1', app)

@app.route('/geosearch', methods=['GET'])
def home_page():
  city_name = request.args.get('city')
  base_url = "http://api.openweathermap.org/geo/1.0/direct?q="+city_name+"&appid="+API_Key
  result = requests.get(base_url).json()
  location = result[0]
  data = {
    "city": location.get('country'),
    "state": location.get('state'),
    "lat": location.get('lat'),
    "lon": location.get('lon')
  }
  pprint(data)
  return data, 200

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