from tkinter import *
from tkinter import messagebox
from tkinter import ttk 
from main import *
from datetime import timedelta, datetime
from pymediainfo import MediaInfo
import xml.etree.ElementTree as ET
import locale
import os

class Manager:
    def __init__(self, parent, items = [], span = [], title = "Планировщик", icon=None):
        self.items = [] # Итемы в списке
        self.i = 0
        self.items_in_list = [] # Переменная для обработки инпутов
        self.tree_to_send = [] # Переменная для обработки дерева
        self.result = '00:00:00'
        self.root = Toplevel(parent)
        self.root.title(title)
        self.list_input = [] # Глобальный список инпутов в процессе парсинга
        self.pars(self.list_input) # Сам процесс парсинга 
        self.get_items(self.items) # Заполнение Combobox
        self.span = ['None','None','00:00:00',str(datetime.now())[:-7],'None'] # Для первоначального заполнения , в процессе работы менеджера переменная видоизменяется
        # Frames
        self.other_frame= LabelFrame(self.root, bd=0)
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
        if icon:
            self.iconbitmap(icon)
        self.tree = ttk.Treeview(self.root, columns=('Title', 'GUID', 'Duration','Type', 'Start', 'End'), height=30, show='headings')#
        self.tree_info = ttk.Treeview(self.event_info, columns=('Path', 'Duration'), height=10, show='headings')
        # Draw Frames
        self.draw_label_frame() # Самый первый фрэйм с импутами и прочим
        self.draw_table() # Frame С таблицей
        self.draw_event_info() # Нижний фрейм с информацией по видеолисту 
        self.draw_button_frame() #Фрэйм где ADD REFRESH APPEND CLEAR
        self.draw_time_btn_frame()# выбор времени
        self.grab_focus()

    def draw_label_frame(self):
        self.key = StringVar(value=self.span[1])
        self.time_input = StringVar(value=self.span[2])
        self.date_now_input = StringVar(value=self.span[3])
        self.type_i = StringVar(value=self.span[4])

        self.lbl1 = Label(self.label_frame, text="Имя: ", anchor=W).grid(row=0, column=0)
        self.title_entry = ttk.Combobox(self.label_frame, values=list(self.items), width=37)
        self.title_entry.current(0)
        self.title_entry.grid(row=0, column=1)

        self.lbl2 = Label(self.label_frame, text="GUID: ", anchor=W).grid(row=1, column=0)
        self.key_entry = Entry(self.label_frame, textvariable=self.key, width=40)
        self.key_entry.grid(row=1, column=1)

        self.lbl3 = Label(self.label_frame, text="Время: ", anchor=W).grid(row=2, column=0)
        self.time_entry = Entry(self.label_frame, textvariable=self.time_input, width=40, state='disabled')
        self.time_entry.grid(row=2, column=1)

        self.lbl4 = Label(self.label_frame, text="Начало: ", anchor=W).grid(row=3, column=0)
        self.start_entry = Entry(self.label_frame, textvariable=self.date_now_input, width=40)
        self.start_entry.grid(row=3, column=1)

        self.get_button = Button(self.label_frame, text="Получить", command=self.get_title, width=15)
        self.get_button.grid(row=5, column=1, padx=5, pady=5)

        self.add_button = Button(self.label_frame, text="Добавить", command=self.insert_tree, width=15)#span_print 
        self.add_button.grid(row=6, column=1, padx=5, pady=5)

        self.add_button = Button(self.label_frame, text="Удалить", command=self.selectItem_remove, width=15)#span_print insert_tree
        self.add_button.grid(row=6, column=0, padx=5, pady=5)

        self.key_entry.insert = (0, self.key)
        self.time_entry.insert = (0, self.time_input)
        self.start_entry.insert = (0, self.date_now_input)

    def draw_button_frame(self):
        self.save_button = Button(self.btn_frame, text="Сохранить", command=self.save_to_xml, width=10)
        self.save_button.grid(row=0, column=0, padx=5, pady=5)

        self.refres_btn = Button(self.btn_frame, text="Обновить", command=self.refres_items, width=10)
        self.refres_btn.grid(row=0, column=1, padx=5, pady=5)

        self.insert_btn = Button(self.btn_frame, text="Добавить", command=self.span_print, width=10)# command=self.get_title, Пока не написана функция будет пустая кнопка
        self.insert_btn.grid(row=0, column=2, padx=5, pady=5)

        self.clear_button = Button(self.btn_frame, text="Отчистить", command=self.clear_tree, width=10)
        self.clear_button.grid(row=0, column=3, padx=5, pady=5)

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
        self.tree.column('Title', width=150, anchor=W)
        self.tree.column('GUID', width=200, anchor=CENTER)
        self.tree.column('Duration', width=170, anchor=CENTER)
        self.tree.column('Type', width=100, anchor=CENTER)
        self.tree.column('Start', width=200, anchor=CENTER)
        self.tree.column('End', width=200, anchor=CENTER)

        self.tree.heading('Title',text='Input')
        self.tree.heading('GUID',text='Ключ')
        self.tree.heading('Duration',text='Проболжительность')
        self.tree.heading('Type',text='Тип')
        self.tree.heading('Start',text='Начало')
        self.tree.heading('End',text='Конец')
        
        self.tree.grid(row=0, column=0)

    def draw_event_info(self):
        self.tree_info.column('Path', width=300, anchor=W)
        self.tree_info.column('Duration', width=100, anchor=CENTER)
        self.tree_info.heading('Path',text='Файл')
        self.tree_info.heading('Duration',text='Время')
        
        self.tree_info.grid(row=0, column=0)

    def insert_tree(self):
        now = datetime.now()
        i_num = 0
        self.i = self.i + 1
        i_num = i_num + 1
        text = self.title_entry.get()
        key = self.key_entry.get()
        time = self.time_entry.get()
        start = self.start_entry.get()
        # Получение окончания планировки
        duration = datetime.time(datetime.strptime(str(time), "%H:%M:%S"))
        # Конвертируем обратно в миллисекунды
        req = timedelta(hours=int(duration.hour), minutes=int(duration.minute), seconds=int(duration.second)+1) / timedelta(milliseconds=1)# Перевод в миллисекунды
        end = (datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S")) + (timedelta(milliseconds = int(req)))
        if now > end:
            messagebox.showwarning(title="Предупреждение!!", message="Задача не может быть добавлена. Она просрочена или раньше настоящего времени!")
        elif now < end:
            item = self.tree.insert('', 'end', text="Item_"+str(self.i), values=(text, key, time, str(self.span[4]), start, end))
            if self.span[4] == 'VideoList':
                ziro_point = start # отправная точка , необходима для отсчета времени начало-конца видео :) 
                                # Очень удобно и к тому же полезно
                for x in self.items_in_list:
                    text = x['Path'] # Путь. С путем все понятно
                    base = base=os.path.basename(text)
                    time_video = datetime.time(datetime.strptime(str(x['Duration']), "%H:%M:%S"))
                    req_video = timedelta(hours=int(time_video.hour), minutes=int(time_video.minute), seconds=int(time_video.second) + 1) / timedelta(milliseconds = 1)
                    next_video = (datetime.strptime(str(ziro_point), "%Y-%m-%d %H:%M:%S")) + (timedelta(milliseconds = int(req_video)))
                    self.tree.insert(item, 'end', text=str(i_num), values=(base, text, time_video, 'Video', ziro_point, next_video))
                    ziro_point = next_video

    def selectItem_remove(self):
        curItem = self.tree.focus()
        self.tree.delete(curItem)

    def clear_tree(self): # Отчистка планировщика
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.i = 0
    # Забираем все элементы с TREEVIEW и сохраняем все в xml
    def span_print(self):
        list_tree_lines = []
        for item in self.tree.get_children():
            item_text = self.tree.item(item,"values")
            list_tree_lines.append(item_text)
        
        filename = 'last_shedule.xml'
        root_xml = ET.Element("root")
        appt_xml = ET.Element("events")
        root_xml.append(appt_xml)
        for i in list_tree_lines:
            # создаем дочерний суб-элемент. 
            event_input = ET.SubElement(appt_xml, "event")
            event_input.set('guid', i[1])
            event_input.set('duration', i[2])
            event_input.set('type', i[3])
            event_input.set('start', i[4])
            event_input.set('end', i[5])
            event_input.text = i[0]
        tree = ET.ElementTree(root_xml)
        tree.write("temp/"+filename+"")         
        self.root.destroy()

    def save_to_xml(self):
        list_tree_lines = []
        for item in self.tree.get_children():
            item_text = self.tree.item(item,"values")
            list_tree_lines.append(item_text)
        filename = ''+str(datetime.strptime(str(datetime.now())[:-7], "%Y-%m-%d %H:%M:%S"))+'.xml'
        root_xml = ET.Element("root")
        appt_xml = ET.Element("events")
        root_xml.append(appt_xml)
        for i in list_tree_lines:
            # создаем дочерний суб-элемент. 
            event_input = ET.SubElement(appt_xml, "event")
            event_input.set('guid', i[1])
            event_input.set('duration', i[2])
            event_input.set('type', i[3])
            event_input.set('start', i[4])
            event_input.set('end', i[5])
            event_input.text = i[0]
        tree = ET.ElementTree(root_xml)
        tree.write("temp/"+filename+"")         

    def get_title(self):
        self.span.clear()
        value = self.title_entry.get()
        index = self.title_entry.current()
        self.item_info_list = []
        all_time = 0
        for i in self.tree_info.get_children():
            self.tree_info.delete(i)
        i_num = 0
        for i in self.list_input:
            title = i['Title']
            now = datetime.now() + timedelta(seconds=5)
            if value in title:
                key = i['GUID']
                type_i = i['Type']
                if type_i == 'VideoList':
                    self.items_in_list.clear()
                    root = ET.parse('res/vmix.xml').getroot()
                    root_find = root.findall('inputs/input')
                    for x in root_find:
                        inp = x.get('key')
                        if inp == key:
                            y = x.find('list')
                            for fn in y:
                                mi = MediaInfo.parse(fn.text)
                                duration_in_ms = mi.tracks[0].duration
                                try:
                                    time = datetime.strftime(datetime.strptime(str(timedelta(milliseconds = int(duration_in_ms))), "%H:%M:%S"), "%H:%M:%S")
                                except:
                                    time = datetime.strftime(datetime.strptime(str(timedelta(milliseconds = int(duration_in_ms)))[:-7], "%H:%M:%S"), "%H:%M:%S")
                                res = {'Path': fn.text,'Duration': time}
                                base = base=os.path.basename(fn.text)
                                self.tree_info.insert('', 'end', text=str(i_num), values=(base, time))
                                i_num = i_num + 1
                                all_time = int(all_time) + int(duration_in_ms)
                                self.items_in_list.append(res)
                    try:
                        sum_time = datetime.strftime(datetime.strptime(str(timedelta(milliseconds = int(all_time))), 
                                                "%H:%M:%S"), "%H:%M:%S")
                    except:
                        sum_time = datetime.strftime(datetime.strptime(str(timedelta(milliseconds = int(all_time)))[:-7], 
                                "%H:%M:%S"), "%H:%M:%S")
                    data = [value, key, sum_time, str(now)[:-7], type_i]# [:-7] - нужно для удаления миллисекунд, чтоб читабельно было
                else:
                    try:
                        time = datetime.strftime(datetime.strptime(str(timedelta(milliseconds = int(i['Time'])))[:-7], 
                                    "%H:%M:%S"), "%H:%M:%S")
                    except:
                        time = "00:00:00"
                    data = [value, key, time, str(now)[:-7], type_i]# [:-7] - нужно для удаления миллисекунд, чтоб читабельно было
    
        self.span = data
        self.draw_label_frame()
        self.title_entry.current(int(index))

    def get_items(self, value):
        for t in self.list_input:
            title = t['Title']
            self.items.append(title)

    def refres_items(self):
        self.list_input.clear()
        self.items.clear()
        self.pars(self.list_input)
        self.get_items(self.items)
        self.draw_label_frame()

    # выбор времени
    # надо как то вынести в другой файл

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

    def grab_focus(self):
        self.root.grab_set()
        self.root.resizable(False, False)
        self.root.focus_set()
        self.root.wait_window()
