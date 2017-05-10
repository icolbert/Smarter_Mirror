from mirror_apps import *
from tkinter import *

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='grey10')
        
        self.topFrame = Frame(self.tk, background = 'grey10')
        self.centerFrame1 = Frame(self.tk, background = 'grey10')
        self.centerFrame2 = Frame(self.tk, background = 'grey10')
        self.bottomFrame = Frame(self.tk, background = 'grey10')
        
        self.topFrame.pack(side = TOP, fill=X)
        self.centerFrame1.pack(side = TOP, fill=X)
        self.centerFrame2.pack(side=TOP, fill=X)
        self.bottomFrame.pack(side = BOTTOM, fill=X, expand = YES)
        
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=S, padx=50, pady=60)
        # weather
        self.weather = Weather(self.centerFrame1)
        self.weather.pack(side=RIGHT, anchor=N, padx=50)
        # forecast
        self.forecast = Forecast(self.centerFrame2)
        self.forecast.pack(side=RIGHT, anchor=N, padx=50)


    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    window = FullscreenWindow()
    here()
    window.tk.mainloop()
