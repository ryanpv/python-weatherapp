import requests
from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

API_Key = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/')
def home_page():
  return "Hello World"

@app.route('/<city>', methods=['GET'])
def city_weather(city):
  base_url = "https://api.openweathermap.org/data/2.5/weather?&appid="+API_Key+"&q="+city

  weather_data = requests.get(base_url).json()
  return weather_data


app.run(host="0.0.0.0", port=9000, debug=True)