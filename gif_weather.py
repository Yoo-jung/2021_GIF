import requests
import json

# get API data
response = requests.get('http://api.weatherapi.com/v1/current.json?key=56e480e2ae5c44f381d65742211111&q=seoul&aqi=yes')
jsonObj = json.loads(response.text)

# print weather data-> temp & condition
print(jsonObj['current']['temp_c'], jsonObj['current']['condition']['text'])

# print date data & time
print(jsonObj['location']['localtime'])

# sort Season data
seoson = jsonObj['location']['localtime'][5:7]
if  seoson == '12' or seoson <= '2':
    print('Winter')
elif seoson >= '9' and seoson <= '11':
    print('Fall')
elif seoson >= '5' and seoson <= '8':
    print('Summer')
else:
    print('Spring')