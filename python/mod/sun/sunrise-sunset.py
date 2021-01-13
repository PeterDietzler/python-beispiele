import requests
import json
from datetime import datetime, time, timedelta
from time import sleep
import pifacedigitalio as p # nur für PiFace Digital nötig

pifacedigital = p.PiFaceDigital()
url = 'https://api.sunrise-sunset.org/json?lat=49.018718&lng=12.08948&formatted=0' # URL definieren, lat und lng anpassen
r = requests.get(url) # Daten abfragen

while True:
    d = datetime.now()
    today_date = d.date() # Heutiges Datum
    time_now = d.time() # Momentane Uhrzeit / UTC

    data = json.loads(r.content)
    sunrise = data['results']['sunrise'] # Daten für Sonnenaufgang
    sunset = data['results']['sunset'] # Daten für Sonnenuntergang
    sunrise_time = time(int(sunrise[11:13]), int(sunrise[14:16])) # Sonnenaufgang in Zeit-Format umwandeln
    sunset_time = time(int(sunset[11:13]), int(sunset[14:16])) # Sonnenuntergang in Zeit-Format umwandeln

    if time_now > sunrise_time and time_now < sunset_time: # Zeit zwischen Sonnenaufgang / -untergang

        if pifacedigital.output_pins[1].value == 1: # Ist das Relais nicht aus
            pifacedigital.output_pins[1].turn_off() # schalte es aus
    else:
        if pifacedigital.output_pins[1].value != 1: # Ist das Relais nicht an
            pifacedigital.output_pins[1].turn_on() # schalte es an

    sleep(60)
    
    if str(sunrise[0:10]) != str(today_date): # Unterschiedliches Datum, hole neue Daten
        r = requests.get(url)
