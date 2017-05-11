import time
import threading
import traceback
import locale
import json
import numpy as np
from urllib import request
from tkinter import *
from contextlib import contextmanager

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
news_country_code = 'us'
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

LOCALE_LOCK = threading.Lock()

@contextmanager

def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

def here():
    print('We good over here!')

def in_here():
    print('We in this bitch')

def out_here():
    print('We out this bitch')

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='grey10')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Verdana', large_text_size), fg="white", bg='grey10')
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Verdana', small_text_size), fg="white", bg='grey10')
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Verdana', small_text_size), fg="white", bg='grey10')
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(''):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format
                
            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                if int(time.strftime('%I')) < 10:
                    self.timeLbl.config(text=time2[1:])
                else:
                    self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            self.timeLbl.after(200, self.tick)


# class Weather calls Frame from tkinter() as its parent.
# It accesses the Open Weather Map API to download current weather and store in into a label for the GUI
class Weather(Frame):
    def __init__(self,parent,*args, **kwargs):
        Frame.__init__(self, parent, bg='grey10')
        self.DoW = int(time.strftime('%w'))
        self.temperature = ''
        self.weather = ''
        self.forecast = ''
        
        self.currentTempLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="grey10")
        self.currentTempLbl.pack(side=BOTTOM, anchor=E)
        
        self.get_weather()
            
    def get_weather(self):

        '''
        API Key: e8f68888e32b9e688db40c7a784aa417
        '''
        
        try:
            weather_api_url = "http://api.openweathermap.org/data/2.5/weather?id=524901&APPID=e8f68888e32b9e688db40c7a784aa417&q=92037,us&units=imperial"
            req1 = request.urlopen(weather_api_url)         # calls for weather from Open Weather Map
            omw1 = req1.read().decode('utf-8')              # decodes the weather bytes into a json format
            weather = json.loads(omw1)                      # decodes json into dictionary
            self.weather = weather['main']['temp']
            self.temperature = str(round(weather['main']['temp']))+u'\N{DEGREE SIGN}'+'F in '+str(weather['name'])
            self.currentTempLbl.config(text=self.temperature)

            self.currentTempLbl.after(120000, self.get_weather)

        except Exception as e:
            traceback.print_exc()
            print('Error: ',e)
            print('Cannot get weather')    


# class Forecast uses the frame function from tkinter as its parent as well
# Uses the same API as the weather class, except gets the 5 day/3 hour forecast

class Forecast(Frame):
    def __init__(self,parent,*args,**kwargs):
        self.DoW = int(time.strftime('%w')) #initialize the numerical day of the week
        
        Frame.__init__(self, parent, bg='grey10')
        self.minLbl = Label(self, font=('Helvetica', medium_text_size), fg='grey50', bg='grey10')
        self.minLbl.pack(side=RIGHT)
        self.maxLbl = Label(self, font=('Helvetica', medium_text_size), fg='grey70', bg='grey10')
        self.maxLbl.pack(side=RIGHT)
        self.dayLbl = Label(self, font=('Helvetica', medium_text_size), fg='white',  bg='grey10')
        self.dayLbl.pack(side=RIGHT, padx=15)
        
        self.print_forecast()

    def get_forecast(self):
        
        ##   Using the same API Key as get_weather
        
        try:
            forecast_api_url = "http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=e8f68888e32b9e688db40c7a784aa417&q=92037,us&units=imperial"
            req2 = request.urlopen(forecast_api_url)        # calls for the forecast from the Open Weather Map
            omw2 = req2.read().decode('utf-8')              # decodes the forecast bytes into a json format
            forecast = json.loads(omw2)                     # decodes json into dictionary
            data = forecast['list']
            return data
        
        except Exception as e:
            print('Error: ',e)
            print('Cannot get forecast')

    def forecast_display(self):
        try:
            data = self.get_forecast()
            next_month = 'abcd'
            date = time.strftime('%Y-%m-')
            year  = int(time.strftime('%Y'))
            month = int(time.strftime('%m'))
            day = int(time.strftime('%d'))
            forecast = np.matrix('0 0;0 0;0 0;0 0')
            i = self.DoW
            j = 0
            forecast[i-self.DoW,0] = int(data[j]['main']['temp'])
            forecast[i-self.DoW,1] = int(data[j]['main']['temp'])
            
            while i < self.DoW + 4:

                # nested if statement criterion for solving the edge case problem
                if month < 10:
                    if day < 10:
                        check = date+'0%d' % day
                    elif month == 9:
                        check = date+'%d' % day
                        next_month = str(year)+'-10-01'
                    else:
                        check = str(year)+'-0'+str(month)+'-'+str(day)
                        next_month = str(year)+'-0'+str(month+1)+'-01'
                elif month == 12:
                    if day < 10:
                        check = str(year)+'-'+str(month)+'-0'+str(day)
                    else:
                        check = str(year)+'-'+str(month)+'-'+str(day)
                        next_month = str(year+1)-'01-01'
                else:
                    if day < 10:
                        check = str(year)+'-'+str(month)+'-0'+str(day)
                    else:
                        check = str(year)+'-'+str(month+1)+'-01'

                if check in data[j]['dt_txt']:
                    
                    #print(data[j]['main']['temp'],type(data[j]['main']['temp']))
                    if data[j]['main']['temp'] > forecast[i-self.DoW,0]:
                        #print(str(data[j]['main']['temp'])+' vs '+str(forecast[i-DoW,0]))
                        forecast[i-self.DoW,0] = data[j]['main']['temp']
                        #print('changed max('+str(j)+'): '+data[j]['dt_txt'])
                        
                    elif data[j]['main']['temp'] < forecast[i-self.DoW,1]:
                        forecast[i-self.DoW,1] = data[j]['main']['temp']
                        #print('changed min('+str(j)+'): '+data[j]['dt_txt'])

                elif next_month in data[j]['dt_txt']: # solves edge cases for forecast call (month and year switches)
                    day = 1
                    if month < 12:
                        month += 1
                    else:
                        month = 1
                
                else:
                    i+=1
                    day+=1
                    
                    if i-self.DoW < 4: # initialize first readings to both the max and min for the next day
                        forecast[i-self.DoW,0]=data[j]['main']['temp']
                        forecast[i-self.DoW,1]=data[j]['main']['temp']
                j+=1

            return forecast

        except Exception as e:
            print('Error: ',e)
            print('Cannot display forecast')

    def print_forecast(self):
        data = self.forecast_display()
        units = [self.DoW+1, self.DoW+2, self.DoW+3]

        # solves end of week edge cases
        if self.DoW == 6:
            units = [0, 1, 2]
        elif self.DoW == 5:
            units = [6, 0, 1]
        elif self.DoW == 4:
            units = [5, 6, 0]
            
        days = ['         Sunday',
                '         Monday',
                '     Tuesday',
                'Wednesday',
                '    Thursday',
                '         Friday',
                '    Saturday']

        minimum = maximum = future = ''
        j = 0
        while j < 3:
            if j < 2:
                minimum += '%d\n' % data[j+1,1]
                maximum += '%d\n' % data[j+1,0]
                future  += '%s\n' % days[units[j]]
            else:
                minimum += '%d' % data[j+1,1]
                maximum += '%d' % data[j+1,0]
                future  += days[units[j]]
            j+=1
            
        self.minLbl.config(text=minimum)
        self.maxLbl.config(text=maximum)
        self.dayLbl.config(text=future)

        self.minLbl.after(3600000, self.print_forecast)
        

