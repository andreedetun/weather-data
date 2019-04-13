import os
import sys
import requests
import json

# Specify what city to get data about.
city = sys.argv[1]

# Get api key from config file.
with open('config.json') as config_file:
    config = json.load(config_file)
    key = config['api-key']

# Format the url used for weather requests correctly.
url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&APPID={key}'

# Send response to the api.
r = requests.get(url)

# Extract the data recieved.
data = r.json()

# This will for example return 'Clear', 'Rain' etc.
general = data['list'][0]['weather'][0]['main']

# This will for example return 'clear sky' etc.
description = data['list'][0]['weather'][0]['description']

# This will for example return '5.4' (celcius)
cur_temp = data['list'][0]['main']['temp']

# This will for example return '4.4' (celcius)
max_temp = data['list'][0]['main']['temp_max']

# This will for example return '-5.4' (celcius)
min_temp = data['list'][0]['main']['temp_min']

