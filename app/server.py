import requests
from flask import Flask, jsonify, request, redirect, session
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

API_Key = os.getenv('API_KEY')

app = Flask(__name__)
app.secret_key = 'jf3A&&]32ADFb8298hh'

@app.route('/geosearch')
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

  session['data'] = data
  pprint(data)
  return redirect(f"http://localhost:9000/city/toronto?lat={ data.get('lat') }&lon={ data.get('lon') }")

@app.route('/city/<city>', methods=['GET'])
def city_weather(city):
  lon = request.args.get('lon')
  lat = request.args.get('lat')
  location = session.get('data')
  # base_url = "https://api.openweathermap.org/data/2.5/weather?&appid="+API_Key+"&q="+city
  base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={ lat }&lon={ lon }&appid={ API_Key }"

  result = requests.get(base_url).json()

  # if "name" not in result or "sys" not in result:
  #   return None
  
  # data = {
  #   "Location": f"{ result.get('name') }, { result.get('sys').get('country') }",
  #   "Weather_Description": f"{ result.get('weather')[0].get('description') }"
  # }

  pprint(location)
  return jsonify(result)

@app.route('/coordinates', methods=['GET'])
def coordinates():
  try:
      lon = float(request.args.get('lon')) if request.args.get('lon') else None
      lat = float(request.args.get('lat')) if request.args.get('lat') else None

      if not lat or not lon:
        raise ValueError("Missing latitude or longitude value.")
      
      base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={ lat }&lon={ lon }&appid={ API_Key }"

      result = requests.get(base_url).json()
      return result
  
  except ValueError as e:
    pprint({ "ERROR: ": e })
    return f"VALUE ERROR: { e }"


@app.route('/current')
def current_weather():
  base_url = 'https://api.openweathermap.org/data/2.5/weather?appid='+API_Key

  weather_today = requests.get(base_url).json()
  return weather_today


app.run(host="0.0.0.0", port=9000, debug=True)