from tkinter import *
from tkinter import ttk 
from datetime import timedelta, datetime
import button_functions
import locale
import xml.etree.ElementTree as ET
import os

class Manager:
    
    def __init__(self, parent, items = [], span = [], title = "Планировщик", icon=None):
        self.items = []
        self.i = 0
        self.items_in_list = []
        self.result = '00:00:00'
        self.root = Toplevel(parent)
        self.root.title(title)
        self.list_input = []
        self.pars(self.list_input)
        self.get_items(self.items)
        self.span = ['None','None','00:00:00',str(datetime.now())[:-7],'None']
        # Frames
        self.other_frame= LabelFrame(self.root, text = 'Обработка INPUTS', bd=0)
        self.other_frame.grid(row=0, column=1, sticky=N, padx=2, pady=2)
        self.btn_frame = LabelFrame(self.other_frame, bd=0)
        self.btn_frame.grid(row=0, column=0, sticky=N, padx=2, pady=2)
        self.label_frame = LabelFrame(self.other_frame, bd=0)
        self.label_frame.grid(row=2, column=0, sticky=N)
        self.push_frame = LabelFrame(self.other_frame, bd=0)
        self.push_frame.grid(row=1, column=0, sticky=N)
        self.time_btn_frame = LabelFrame(self.other_frame, bd=0)
        self.time_btn_frame.grid(row=3, column=0, sticky=N)
        self.event_info = LabelFrame(self.other_frame, bd=0)
        self.event_info.grid(row=4, column=0, sticky=N)
        #self.lbl_info = Label(self.root, text="IMAPOLICMEN")
        #self.lbl_info.grid(row=1, column=1)
        if icon:
            self.iconbitmap(icon)
        self.tree = ttk.Treeview(self.root, columns=('Title', 'GUID', 'Duration','Type', 'Start', 'End'), height=30, show='headings')#
        self.tree_info = ttk.Treeview(self.event_info, columns=('Path', 'Duration'), height=10, show='headings')
        # Draw Frames
        self.draw_label_frame()
        self.draw_table() # Frame С таблицей
        self.draw_event_info()
        self.draw_button_frame() #Фрэйм где ADD REFRESH APPEND CLEAR
        self.draw_push_frame()
        self.draw_time_btn_frame()
        self.grab_focus()

    def draw_label_frame(self):
        #self.start = StringVar(value=self.span[0])
        self.key = StringVar(value=self.span[1])
        self.time_input = StringVar(value=self.span[2])
        self.date_now_input = StringVar(value=self.span[3])
        self.type_i = StringVar(value=self.span[4])

        self.lbl1 = Label(self.label_frame, text="Имя: ", anchor=W).grid(row=0, column=0)
        self.title_entry = ttk.Combobox(self.label_frame, values=list(self.items), width=37)
        self.title_entry.current(0)
        #self.title_entry = Entry(self.label_frame, text='self.message')
        self.title_entry.grid(row=0, column=1)

        self.lbl2 = Label(self.label_frame, text="GUID: ", anchor=W).grid(row=1, column=0)
        self.key_entry = Entry(self.label_frame, textvariable=self.key, width=40)
        self.key_entry.grid(row=1, column=1)

        self.lbl_type = Label(self.label_frame, text="ТИП: ", anchor=W).grid(row=4, column=0)
        self.type_entry = Entry(self.label_frame, textvariable=self.type_i, width=40)
        self.type_entry.grid(row=4, column=1)

        self.lbl3 = Label(self.label_frame, text="Время: ", anchor=W).grid(row=2, column=0)
        self.time_entry = Entry(self.label_frame, textvariable=self.time_input, width=40)
        self.time_entry.grid(row=2, column=1)

        self.lbl4 = Label(self.label_frame, text="Начало: ", anchor=W).grid(row=3, column=0)
        self.start_entry = Entry(self.label_frame, textvariable=self.date_now_input, width=40)
        self.start_entry.grid(row=3, column=1)

        self.get_button = Button(self.label_frame, text="Get", command=self.get_title, width=15)
        self.get_button.grid(row=5, column=1, padx=5, pady=5)

        self.add_button = Button(self.label_frame, text="Add", command=self.insert_tree, width=15)#span_print 
        self.add_button.grid(row=6, column=1, padx=5, pady=5)

        self.add_button = Button(self.label_frame, text="Print", command=self.span_print, width=15)#span_print insert_tree
        self.add_button.grid(row=6, column=0, padx=5, pady=5)

        self.ref_button = Button(self.label_frame, text="Refresh", command=self.check, width=15)
        self.ref_button.grid(row=5, column=0, padx=5, pady=5)

        self.key_entry.insert = (0, self.key)
        self.time_entry.insert = (0, self.time_input)
        self.start_entry.insert = (0, self.date_now_input)
        self.type_entry.insert = (0, self.type_i)


    def draw_button_frame(self):
        self.clear_button = Button(self.btn_frame, text="Add", command=self.get_title, width=10)
        self.clear_button.grid(row=0, column=0, padx=5, pady=5)

        self.load_button = Button(self.btn_frame, text="Refresh", command=self.clear_tree, width=10)
        self.load_button.grid(row=0, column=1, padx=5, pady=5)

        self.clear_button = Button(self.btn_frame, text="Append", command=self.get_title, width=10)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)

        self.load_button = Button(self.btn_frame, text="Clear", command=self.clear_tree, width=10)
        self.load_button.grid(row=0, column=3, padx=5, pady=5)
    
    def draw_push_frame(self):
        self.clear_button = Button(self.push_frame, text="Запланировать", width=22)# command=,
        self.clear_button.grid(row=0, column=0, padx=5, pady=5)

        self.load_button = Button(self.push_frame, text="Отчистить", command=self.clear_tree, width=22)
        self.load_button.grid(row=0, column=1, padx=5, pady=5)

    def draw_time_btn_frame(self):
        self.but_08 = Button(self.time_btn_frame, text="08:00", command=self.time_08, width=10).grid(row=0, column=0, padx=5, pady=5)
        self.but_09 = Button(self.time_btn_frame, text="09:00", command=self.time_09, width=10).grid(row=0, column=1, padx=5, pady=5)
        self.but_10 = Button(self.time_btn_frame, text="10:00", command=self.time_10, width=10).grid(row=0, column=2, padx=5, pady=5)
        self.but_11 = Button(self.time_btn_frame, text="11:00", command=self.time_11, width=10).grid(row=0, column=3, padx=5, pady=5)
        self.but_12 = Button(self.time_btn_frame, text="12:00", command=self.time_12, width=10).grid(row=1, column=0, padx=5, pady=5)
        self.but_13 = Button(self.time_btn_frame, text="13:00", command=self.time_13, width=10).grid(row=1, column=1, padx=5, pady=5)
        self.but_14 = Button(self.time_btn_frame, text="14:00", command=self.time_14, width=10).grid(row=1, column=2, padx=5, pady=5)
        self.but_15 = Button(self.time_btn_frame, text="15:00", command=self.time_15, width=10).grid(row=1, column=3, padx=5, pady=5)
        self.but_16 = Button(self.time_btn_frame, text="16:00", command=self.time_16, width=10).grid(row=2, column=0, padx=5, pady=5)
        self.but_17 = Button(self.time_btn_frame, text="17:00", command=self.time_17, width=10).grid(row=2, column=1, padx=5, pady=5)
        self.but_18 = Button(self.time_btn_frame, text="18:00", command=self.time_18, width=10).grid(row=2, column=2, padx=5, pady=5)
        self.but_19 = Button(self.time_btn_frame, text="19:00", command=self.time_19, width=10).grid(row=2, column=3, padx=5, pady=5)
        self.but_20 = Button(self.time_btn_frame, text="20:00", command=self.time_20, width=10).grid(row=3, column=0, padx=5, pady=5)
        self.but_21 = Button(self.time_btn_frame, text="21:00", command=self.time_21, width=10).grid(row=3, column=1, padx=5, pady=5)
        self.but_22 = Button(self.time_btn_frame, text="22:00", command=self.time_22, width=10).grid(row=3, column=2, padx=5, pady=5)
        self.but_23 = Button(self.time_btn_frame, text="23:00", command=self.time_23, width=10).grid(row=3, column=3, padx=5, pady=5)




    def draw_table(self):
        self.tree.column('Title', width=150, anchor=CENTER)
        self.tree.column('GUID', width=200, anchor=CENTER)
        self.tree.column('Duration', width=170, anchor=CENTER)
        self.tree.column('Start', width=200, anchor=CENTER)
        self.tree.column('End', width=200, anchor=CENTER)

        self.tree.heading('Title',text='Input')
        self.tree.heading('GUID',text='Ключ')
        self.tree.heading('Duration',text='Проболжительность')
        self.tree.heading('Start',text='Начало')
        self.tree.heading('End',text='Конец')
        
        self.tree.grid(row=0, column=0)

    def draw_event_info(self):
        self.tree_info.column('Path', width=300, anchor=CENTER)
        self.tree_info.column('Duration', width=150, anchor=CENTER)
        self.tree_info.heading('Path',text='Путь')
        self.tree_info.heading('Duration',text='Время')
        
        self.tree_info.grid(row=0, column=0)

    def insert_tree(self):
        self.i = self.i + 1
        text = self.title_entry.get()
        key = self.key_entry.get()
        time = self.time_entry.get()
        start = self.start_entry.get()
        # Получение окончания планировки
        result = [start, time]
        duration = datetime.time(datetime.strptime(result[1], "%H:%M:%S"))
        # Конвертируем обратно в миллисекунды
        req = timedelta(hours=int(duration.hour), 
        minutes=int(duration.minute),
        seconds=int(duration.second)+1) / timedelta(milliseconds=1)
        x = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        y = timedelta(milliseconds = int(req))
        end = (datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")) + (timedelta(milliseconds = int(req)))
        #print('Начало: ',date_now_input,' - Конец: ',time_input)
        self.tree.insert('', 'end', text=str(self.i), values=(text, key, time, start, end))

    def clear_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.i = 0

    def span_print(self):
        now = datetime.strptime(self.span[2], "%H:%M:%S")
        time = now.strftime("%H:%M:%S")
        print("time:", time)
        print(self.span)
        print(self.result)

    def pars_items(self, key):

        root = ET.parse('res/API.xml').getroot()
        root_find = root.findall('inputs/input')

        for x in root_find:
            inp = x.get('key')
            if inp == key:
                y = x.find('list')
                for i in y:
                    self.items_in_list.append(i.text)
    
    def get_title(self):
        self.span.clear()
        value = self.title_entry.get()
        index = self.title_entry.current()
        for i in self.list_input:
            title = i['Title']
            if value in title:
                key = i['GUID']
                type_i = i['Type']
                try:
                    time = datetime.strftime(datetime.strptime(str(timedelta(milliseconds = int(i['Time'])))[:-7], 
                            "%H:%M:%S"), "%H:%M:%S")
                except:
                    time = "00:00:00"
                now = datetime.now() + timedelta(seconds=5)
                data = [value, key, time, str(now)[:-7], type_i]# [:-7] - нужно для удаления миллисекунд, чтоб читабельно было
        print('DO : --> ',self.items_in_list)
        print(type_i)
        print(key)
        if type_i == 'VideoList':
            root = ET.parse('res/vmix.xml').getroot()
            root_find = root.findall('inputs/input')
            print(root_find)
            for x in root_find:
                inp = x.get('key')
                print(inp)
                if inp == key:
                    y = x.find('list')
                    for i in y:
                        self.items_in_list.append(i.text)

        print('Posle: --> ',self.items_in_list)
        self.span = data
        #print(self.span)
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def get_items(self, value):
        for t in self.list_input:
            title = t['Title']
            self.items.append(title)

    def check(self):
        self.list_input.clear()
        self.items.clear()
        self.pars(self.list_input)
        self.get_items(self.items)
        self.draw_label_frame()

    def pars(self, value):
        # Забираем IP и PORT подключения VMIX
        root_conf = ET.parse('res/conf.xml').getroot() 
        root_conf_find = root_conf.findall('setting/')
        for conf in root_conf_find:
            url = conf.get('url')
            port = conf.get('port')
            os.system('curl -o res/vmix.xml http://'+str(url)+':'+str(port)+'/API')
        # Теперь из выгруженного файла забираем INPUT
        root = ET.parse('res/vmix.xml').getroot()
        root_find = root.findall('inputs/')
        for tag in root_find:
            title = tag.get('title')
            key = tag.get('key')
            duration = tag.get('duration')
            input_n = tag.get('number')
            type_i = tag.get('type')
            data = {'Input': input_n,'Title': title, 'GUID': key, 'Time': duration, 'Type':type_i}
            self.list_input.append(data)

    def time_08(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("08:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_09(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("09:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_10(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("10:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_11(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("11:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_12(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("12:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))
    
    def time_13(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("13:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_14(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("14:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_15(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("15:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_16(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("16:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_17(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("17:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_18(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("18:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))
    
    def time_19(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("19:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))
    
    def time_20(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("20:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_21(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("21:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_22(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("22:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def time_23(self):
        index = self.title_entry.current()
        date = datetime.date(datetime.strptime(str(self.start_entry.get()) , "%Y-%m-%d %H:%M:%S"))
        time = datetime.time(datetime.strptime("23:00:00" , "%H:%M:%S"))
        self.result = datetime.combine(date, time)
        self.span.pop(3)
        self.span.insert(3, str(self.result))
        self.draw_label_frame()
        self.title_entry.current(int(index))
    def grab_focus(self):
        self.root.grab_set()
        self.root.resizable(False, False)
        self.root.focus_set()
        self.root.wait_window()
