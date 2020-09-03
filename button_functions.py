from tkinter import *
from tkinter import ttk 
from datetime import timedelta, datetime

def push_time_08():
    value = self.title_entry.get()
    index = self.title_entry.current()
    date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
    time = datetime.time(datetime.strptime("08:00:00" , "%H:%M:%S"))
    self.result = datetime.combine(date, time)
    self.span.pop(3)
    self.span.insert(3, str(self.result))
    self.draw_label_frame()
    self.title_entry.current(int(index))