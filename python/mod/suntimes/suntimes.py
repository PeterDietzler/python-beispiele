import requests
import json
from datetime import datetime, time, timedelta
from time import sleep


"""
https://api.sunrise-sunset.org/json?lat=49.018718&lng=12.08948&formatted=0

{"results":
    {
    "sunrise":"2021-01-13T07:01:04+00:00",
    "sunset":"2021-01-13T15:40:06+00:00",
    "solar_noon":"2021-01-13T11:20:35+00:00",
    "day_length":31142,
    "civil_twilight_begin":"2021-01-13T06:25:06+00:00",
    "civil_twilight_end":"2021-01-13T16:16:03+00:00",
    "nautical_twilight_begin":"2021-01-13T05:45:32+00:00",
    "nautical_twilight_end":"2021-01-13T16:55:38+00:00",
    "astronomical_twilight_begin":"2021-01-13T05:07:33+00:00",
    "astronomical_twilight_end":"2021-01-13T17:33:37+00:00"
    },
"status":"OK"}

"""





def htmlRequest(lat, lng ):
    x = lat
    y = lng
    
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y
    home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y +'&formatted=0'
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y +'&formatted=1'
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y +'&date=toda'
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y + '&date=2050-01-13'
    
    r = requests.get(home) # Daten abfragen
    #print(r.content )
    return r

def getRequesContent(lat, lng ):
    x = lat
    y = lng
    
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y
    home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y +'&formatted=0'
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y +'&formatted=1'
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y +'&date=toda'
    #home = 'https://api.sunrise-sunset.org/json?lat=' + x +'&lng=' + y + '&date=2050-01-13'
    
    r = requests.get(home) # Daten abfragen
    content    = json.loads(r.content)    
    return content


   
def printResult(r, timezone ):
    d = datetime.now()
    today_date = d.date() # Heutiges Datum
    time_now = d.time() # Momentane Uhrzeit / UTC

    data = json.loads(r.content)
    sunrise = data['results']['sunrise'] # Daten für Sonnenaufgang
    sunset = data['results']['sunset'] # Daten für Sonnenuntergang
    day_l   =  data['results']['day_length'] 
    solar_n   =  data['results']['solar_noon'] 

    sunrise_time = time(int(sunrise[11:13]) + timezone, int(sunrise[14:16])) # Sonnenaufgang in Zeit-Format umwandeln
    sunset_time  = time(int( sunset[11:13]) + timezone, int( sunset[14:16])) # Sonnenuntergang in Zeit-Format umwandeln
    solar_noon   = time(int(solar_n[11:13]) + timezone, int(solar_n[14:16])) # Sonnenuntergang in Zeit-Format umwandeln
    
    print('-' * 40 + "suntimes.py" +'-' * 40)
    print('Sonnenaufgang   : ' + str(sunrise_time))
    print('Sonnenuntergang : ' + str(sunset_time))
    print('Sonnehöchststand: ' + str(solar_noon))
    
    stunden = day_l / 3600
    minuten = day_l % 60
    print( 'Tageslichtdauer : %d:%d' % (stunden, minuten) )
 

def sunsetxy(lat, lng):
    result = htmlRequest(str(lat), str(lng))
    printResult(result, 1)

def set( lat, lng, timezone ):
    data    = getRequesContent(str(lat), str(lng))
    sunset  = data['results']['sunset'] # Daten für Sonnenuntergang
    sunset_time  = time(int( sunset[11:13]) + timezone, int( sunset[14:16])) # Sonnenuntergang in Zeit-Format umwandeln
    return sunset_time

def rice( lat, lng, timezone ):
    data    = getRequesContent(str(lat), str(lng))
    sunrise = data['results']['sunrise'] # Daten für Sonnenaufgang
    sunrise_time = time(int(sunrise[11:13]) + timezone, int(sunrise[14:16])) # Sonnenaufgang in Zeit-Format umwandeln
    return sunrise_time

def noon( lat, lng, timezone):
    data    = getRequesContent(str(lat), str(lng))
    solar_n   =  data['results']['solar_noon'] 
    solar_noon   = time(int(solar_n[11:13]) + timezone, int(solar_n[14:16])) # Sonnenhöchtstand in Zeit-Format umwandeln
    return solar_noon

def daytime( lat, lng, timezone):
    data    = getRequesContent(str(lat), str(lng))
    day_l   =  data['results']['day_length'] 
    stunden = int( day_l / 3600)
    minuten = day_l % 60;
    buff = str(stunden) + ":" + str(minuten)
    return buff



































