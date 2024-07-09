import requests
from flask import Flask, jsonify, request, redirect, session
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

API_Key = os.getenv('API_KEY')
SECRET_Key = os.getenv('SECRET_ENV')

app = Flask(__name__)
app.secret_key = SECRET_Key

############## ROUTES ###############
# ROUTE TO GET LAT / LON COORDINATES
@app.route('/coordinates', methods=['GET'])
def coordinates():
  try:
    city_name = request.args.get('city')
    if not city_name:
      raise ValueError("Missing/Invalid city query parameter.")

    base_url = "http://api.openweathermap.org/geo/1.0/direct?q="+city_name+"&appid="+API_Key
    result = requests.get(base_url).json()
    location_data = result[0]
    data = {
      "state": location_data.get('state'),
      "country": location_data.get('country'),
      "lat": location_data.get('lat'),
      "lon": location_data.get('lon')
    }

    return jsonify(data)
  except ValueError as e:
    pprint({ "VALUE ERROR: ", e })
    
# TEMPS USING LAT / LON COORDINATES
@app.route('/coordinates/list', methods=['GET'])
def coordinatesSearch():
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
  


    

# RETURN ALL WEATHER DATA USING CITY QUERY
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

  pprint(location)
  return jsonify(result)


app.run(host="0.0.0.0", port=9000, debug=True)