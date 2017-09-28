# Python packages used:   schedule unidecode  
import os.path
import urllib.request, urllib.error, urllib.parse
import schedule
from unidecode import unidecode
import time
import json
import codecs
import outputs
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
    global forecast
    global lang
    #If the time is past 3 PM, forecast will be for tomorrow, resets at 3AM
    if forecast['forecast']['forecastday'][1]['date'] == time.strftime('%Y-%m-%d', time.localtime()):
        workingDay = 1
        boolDisplay['Tomorrow'] = True
        print("Presenting tommorow's forecast:")
    elif time.localtime().tm_hour >= 15:
        workingDay = 1
        boolDisplay['Tomorrow'] = True
        print("Presenting tommorow's forecast:")
    else:
        workingDay = 0
        boolDisplay['Tomorrow'] = False
        print("Presenting today's forecast:")

    #Setting french lcd display
    displayCode = forecast['forecast']['forecastday'][workingDay]['day']['condition']['code']
    for i in range(0,len(lang)-1):
        if lang[i]['code'] == displayCode:
            lcdText[0] = unidecode(lang[i]['languages'][displayLanguageNumber]['day_text'])
            break
    print(lcdText[0])
        
    #Setting temperature line
    tempLine ="Temp: "
    tempLine += str(int(round(forecast['forecast']['forecastday'][workingDay]['day']['mintemp_c'],0)))
    tempLine += " a "
    tempLine += str(int(round(forecast['forecast']['forecastday'][workingDay]['day']['maxtemp_c'],0)))
    tempLine += "C        "
    lcdText[1] = tempLine
    print(lcdText[1])

    #Sun/Cloud prediction
    averageSkyAlpha = 0.0
    for i in range(5,19):
        averageSkyAlpha += forecast['forecast']['forecastday'][workingDay]['hour'][i]['cloud']
    averageSkyAlpha /= 15.0
    print("Average clouds: "+str(averageSkyAlpha), end=" -> ")
    if averageSkyAlpha > 60:
        boolDisplay['Cloud'] = True;
        boolDisplay['Sun'] = False;
    elif averageSkyAlpha > 35:
        boolDisplay['Cloud'] = True;
        boolDisplay['Sun'] = True;    
    else:
        boolDisplay['Cloud'] = False;
        boolDisplay['Sun'] = True;
    print("Sun: "+str(boolDisplay['Sun'])+" /Cloud: "+str(boolDisplay['Cloud']))

    #Precipitation
    boolDisplay['Rain'] = False;
    boolDisplay['Snow'] = False;
    for i in range(3,22):
        if forecast['forecast']['forecastday'][workingDay]['hour'][i]['will_it_snow'] != 0:
            boolDisplay['Snow'] = True;
        elif forecast['forecast']['forecastday'][workingDay]['hour'][i]['will_it_rain'] != 0:
            boolDisplay['Rain'] = True;
    print("It will rain: "+str(boolDisplay['Rain']))
    print("It will snow: "+str(boolDisplay['Snow']))

    #Update display
    outputs.displayLCD(lcdText)
    outputs.setLeds(boolDisplay)
    


def updateStation():
    #Welcoming user
    print("Starting Weather station");

    #check for lang file
    if not os.path.isfile(languageFile):
        print("Setting up language File...",end=' ')
        urllib.request.urlretrieve(languageURL,languageFile)
        print("OK")
    global lang
    with codecs.open(languageFile, encoding='utf-8-sig') as reader:
        content = reader.read()
        lang = json.loads(content)

    #Acquire 2 day forecast (to get next day forecast at night
    print("Retrieving forecast...", end=' ')
    global forecast
    forecast = weather.getForecastWeather(q=location, days=2)
    #with open(forecastFile, 'w') as writer:
    #    json.dump(forecast, writer)
    print("OK")

    #aggregate data
    print("Analysing data")
    forecastAnalysis()


def wait_for_internet_connection():
    while True:
        try:
            response=urllib.request.urlopen('http://google.com',timeout=1)
            return
        except urllib.error.URLError:
            pass


outputs.clearLCD()
print("Waiting for network...", end=' ')
wait_for_internet_connection()
print("OK")
updateStation()

schedule.every().day.at("3:01").do(updateStation)
schedule.every().day.at("15:01").do(forecastAnalysis)


while True:
    schedule.run_pending()
    time.sleep(1)
    
