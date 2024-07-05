import requests
from pprint import pprint

API_Key = '4e6097b6222c709f55f234b3b9627bd5'

city = input("Enter a city: ")

base_url = "https://api.openweathermap.org/data/2.5/weather?&appid="+API_Key+"&q="+city

weather_data = requests.get(base_url).json()

pprint(weather_data)