import os
import sys
import requests
import json
from twilio.rest import Client
from datetime import datetime
from threading import Timer
 
# Specify what city to get data about.
city = sys.argv[1]

# Get api key & twilio credentials from config file.
with open('config.json') as config_file:
    config = json.load(config_file)
    key = config['api-key']
    sid = config['twilio-sid']
    secret = config['twilio-secret']
    number = config['number']

# Format the url used for weather requests correctly.
url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&APPID={key}'

# Get response fromo the api.
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

# Authenticate the twilio client.
client = Client(sid, secret)

def send_report(): 
# Create the message and send.
    message = client.messages \
                    .create(
                         body=f"Latest forecast for {city}: {general}, {description}, with the current temperature of {cur_temp}\N{DEGREE SIGN}c, max temp: {max_temp}\N{DEGREE SIGN}c, min temp: {min_temp}\N{DEGREE SIGN}c",
                        from_='+46769448018', # This is the number on twilio
                        to=number # Number in config file
                    )

# Time stuff when this will be executed
cur_time = datetime.today()

# Will execute the next morning at 7am.
send_time = cur_time.replace(day=cur_time.day + 1, hour=7, minute=0, second=0, microsecond=0)

delta_t = send_time - cur_time

secs = delta_t.seconds + 1

if __name__ == '__main__':
    timer = Timer(secs, send_report)
    timer.start()
