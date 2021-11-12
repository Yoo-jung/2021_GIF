import requests
import json

response = requests.get('http://api.weatherapi.com/v1/current.json?key=56e480e2ae5c44f381d65742211111&q=seoul&aqi=yes')
jsonObj = json.loads(response.text)
print(jsonObj['current']['temp_c'], jsonObj['current']['condition']['text'])