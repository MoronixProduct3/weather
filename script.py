import os.path
import urllib.request
import schedule
from unidecode import unidecode
import time
import json
import codecs
from apixu.client import ApixuClient, ApixuException

#Constants
api_key = ''
location = ''
forecastFile= 'forecast.json'
languageFile= 'lang.json'
languageURL='http://www.apixu.com/doc/conditions.json'
displayLanguageNumber = 8

#Variables
lang = None
forecast = None
boolDisplay = {'Sun': False, 'Cloud': False, 'Rain': False, 'Snow': False, 'Tomorrow': False}
lcdText = ['linel', 'line2']
weather = ApixuClient(api_key)

def forecastAnalysis():
    #If the time is past 3 PM, forecast will be for tomorrow, resets at 3AM
    if forecast['forecast']['forecastday'][1]['date'] == time.strtime('%Y-%m-%d', time.localtime()):
        workingDay = 1
        boolDisplay['Tomorrow'] = True
    elif time.localtime().tm_hour >= 15:
        workingDay = 1
        boolDisplay['Tomorrow'] = True
    else:
        workingDay = 0
        boolDisplay['Tomorrow'] = False

    #Setting french lcd display
    displayCode = forecast['forecast']['forecastday'][workingDay]['day']['condition']['code']
    for i in range(0,len(lang)-1):
        if lang[i]['code'] == displayCode:
            lcdText[0] = unidecode(lang[i]['languages'][displayLanguageNumber]['day_text'])
            break
        
    #Setting temperature line
    tempLine ="Temp: "
    tempLine += str(int(round(forecast['forecast']['forecastday'][workingDay]['day']['mintemp_c'],0)))
    tempLine += " a "
    tempLine += str(int(round(forecast['forecast']['forecastday'][workingDay]['day']['maxtemp_c'],0)))
    tempLine += "C"
    lcdText[1] = tempLine

def updateStation():
    #Welcoming user
    print("Starting Weather station");

    #check for lang file
    if not os.path.isfile(languageFile):
        print("Setting up language File...")
        urllib.request.urlretrieve(languageURL,languageFile)
        print("OK")
    with codecs.open(languageFile, encoding='utf-8-sig') as reader:
	content = reader.read()
	lang = json.loads(content)

    #Acquire 2 day forecast (to get next day forecast at night
    print("Retrieving forecast...", end=' ')
    forecast = weather.getForecastWeather(q=location, days=2)
    with open(forecastFile, 'w') as writer:
        json.dump(forecast)
    print("OK")

    #aggregate data
    "Analysing data"
    forecastAnalysis()

