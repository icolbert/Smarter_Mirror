from mirror_apps import *
from tkinter import *

clock_count = weather_count = forecast_count = 0

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='grey10')
        
        self.topFrame = Frame(self.tk, background = 'grey10')
        self.centerFrame1 = Frame(self.tk, background = 'grey10')
        self.centerFrame2 = Frame(self.tk, background = 'grey10')
        self.leftFrame1 = Frame(self.tk, background = 'grey10')
        self.leftFrame2 = Frame(self.tk, background = 'grey10')
        self.bottomFrame = Frame(self.tk, background = 'grey10')

        self.leftFrame1.pack(side=LEFT, fill=Y)
        self.leftFrame2.pack(side=LEFT, fill=Y)
        self.topFrame.pack(side = TOP, fill=X)
        self.centerFrame1.pack(side = TOP, fill=X)
        self.centerFrame2.pack(side=TOP, fill=X)
        self.bottomFrame.pack(side = BOTTOM, fill=X, expand = YES)
        
        self.state = True
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        self.clock = Clock(self.topFrame) # setting clock in the top frame (packed on the right)
        self.weather = Weather(self.centerFrame1) # setting the weather in the highest center frame
        self.forecast = Forecast(self.centerFrame2) # setting forecast in the second center frame
        
        commands = {'clock':self.set_clock, 'weather':self.set_weather, 'forecast':self.set_forecast}
        self.buttons = control_display(self.tk,self.leftFrame1,commands)
        self.tk.attributes("-fullscreen", self.state)
        
    def set_clock(self): # command attached to the clock button
        global clock_count
        if clock_count == 0:
            self.clock.pack(side=RIGHT, anchor=N, padx=50, pady=60)
            clock_count+=1
        else:
            self.clock.pack_forget()
            clock_count-=1

    def set_weather(self): # command attached to the weather button
        global weather_count
        if weather_count == 0:
            self.weather.pack(side=RIGHT, anchor=N, padx=50)
            weather_count+=1
        else:
            self.weather.pack_forget()
            weather_count-=1

    def set_forecast(self): # command attached to the forecast button
        global forecast_count
        if forecast_count == 0:
            self.forecast.pack(side=RIGHT, anchor=N, padx=50)
            forecast_count+=1
        else:
            self.forecast.pack_forget()
            forecast_count-=1
        
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    window = FullscreenWindow()
    window.tk.mainloop()
