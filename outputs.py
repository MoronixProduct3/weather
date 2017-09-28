import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

lcd_rs        = 27  
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4

lcd_columns = 16
lcd_rows    = 2

led_Sun = 7
led_Cloud = 8
led_Rain = 11
led_Snow = 9
led_Tomo = 17
gnd_Pin = [15,10]



lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


GPIO.setmode(GPIO.BCM)

GPIO.setup(led_Sun, GPIO.OUT)
GPIO.setup(led_Cloud, GPIO.OUT)
GPIO.setup(led_Rain, GPIO.OUT)
GPIO.setup(led_Snow, GPIO.OUT)
GPIO.setup(led_Tomo, GPIO.OUT)
GPIO.setup(gnd_Pin, GPIO.OUT)

GPIO.output(gnd_Pin, GPIO.LOW)

def displayLCD (strList):
    lcd.message(strList[0][:16]+"\n"+strList[1][:16])


def clearLCD():
    lcd.clear()

def setLeds(displayData):
    GPIO.output(led_Sun, displayData['Sun'])
    GPIO.output(led_Cloud, displayData['Cloud'])
    GPIO.output(led_Rain, displayData['Rain'])
    GPIO.output(led_Snow, displayData['Snow'])
    GPIO.output(led_Tomo, displayData['Tomorrow'])
