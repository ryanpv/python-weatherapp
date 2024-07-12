import requests
import datetime
from flask import Flask, jsonify, request, redirect, session, render_template
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

API_Key = os.getenv('API_KEY')
SECRET_Key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_Key

############ TEMPLATES #############
@app.route('/template1')
def template1():
  return render_template('index.html', utc_dt=datetime.datetime.now())

############## ROUTES ###############
@app.route('/', methods=['GET'])
def home_page():
  data = {
    "message": "These are the list of routes",
    "route_1": "'/coordinates?city=<city>' to get lat/lon of a city's coordinates",
    "route_2": "'/coordinates/list?lat=<lat_value>&lon=<lon_value>' to fetch weather using lat/lon values",
    "route_3": "'/coordinates/list/<city>' fetches coordinates of city and redirects to route 4",
    "route_4": "'/coordinates/data' retrieves coordinates from session and uses it to fetch data",
    "route_5": "'/cities/<city>' fetches weather using just city name"
  }

  return render_template('index.html', routes_data=data)


# ROUTE TO GET LAT / LON COORDINATES
@app.route('/coordinates', methods=['GET', 'POST'])
def coordinates():
  try:
    print("METHOD: ", request.method)
    if request.method == 'POST':
      print('POSTING: ', request.form['city_name'])
      return "Succuessfully posted"
  
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
  
# REDIRECT ROUTE - SEARCH LON / LAT USING CITY NAME 
@app.route('/coordinates/list/<city>')
def city_search(city):
  base_url = "http://api.openweathermap.org/geo/1.0/direct?q="+city+"&appid="+API_Key
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
  return redirect(f"http://localhost:9000/coordinates/data")

@app.route('/coordinates/data')
def redirectedData():
  coordinates = session.get('data')
  lat = coordinates.get('lat')
  lon = coordinates.get('lon')

  base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={ lat }&lon={ lon }&appid={ API_Key }"
  result = requests.get(base_url).json()
  return result

# LIST OF CITIES
@app.route('/cities', methods=['GET', 'POST'])
def city_list():
  try:
    cities = ['city1', 'city2', 'city3']

    if request.method == 'GET':
      print('cities get requested', cities)
      return render_template('index.html', city_list=cities)
    
    if request.method == 'POST':
      print("POST to /cities")
      city = request.form['city_name']
      cities.append(city)
      return render_template('index.html', city_list=cities)
    
  except Exception as e:
    print(e)

# DIRECT QUERY USING CITY NAME
@app.route('/cities/<city>', methods=['GET'])
def city_weather(city):
  location = session.get('data')
  base_url = "https://api.openweathermap.org/data/2.5/weather?&appid="+API_Key+"&q="+city
  # base_url = f"https://api.openweathermap.org/data/2.5/weather?lat={ lat }&lon={ lon }&appid={ API_Key }"
  result = requests.get(base_url).json()

  pprint(location)
  return jsonify(result)



app.run(host="0.0.0.0", port=9000, debug=True)