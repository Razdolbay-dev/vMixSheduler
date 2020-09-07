from tkinter import *
from tkinter import messagebox
import xml.etree.ElementTree as xml
import xml.etree.ElementTree as ET
import requests
import os
class SetConnect:
    def __init__(self, parent, title = "Настройки", icon=None):
        self.root = Toplevel(parent)
        self.root.title(title)
        
        self.span = []
        self.list_input = []
        self.items = []

        self.get_items()
        self.pars()
        #print(self.span)
        self.label_frame = LabelFrame(self.root, text = 'This is Label Frame №1')
        self.label_frame.grid(row=0, column=1, sticky=N)
        if icon:
            self.iconbitmap(icon)
        self.draw_grid()
        self.grab_focus()

    def draw_grid(self):
        
        self.address_vmix = StringVar(value=self.span[0])
        self.port_vmix = StringVar(value=self.span[1])

        self.address_lbl = Label(self.root, text="Адресс vMix: ").grid(row=0, column=0)
        self.address_entry = Entry(self.root, textvariable=self.address_vmix, width=23)
        self.address_entry.grid(row=0, column=1)

        self.port_lbl = Label(self.root, text="Порт vMix: ").grid(row=1, column=0)
        self.port_entry = Entry(self.root, textvariable=self.port_vmix, width=23)
        self.port_entry.grid(row=1, column=1)

        self.lbl1 = Label(self.root, text="Default: ", anchor=W).grid(row=2, column=0)
        self.title_entry = ttk.Combobox(self.root, values=list(self.items))
        self.title_entry.current(0)
        self.title_entry.grid(row=2, column=1)

        self.ok_button = Button(self.root, text="Ok", command=self.createXML, width=15)
        self.ok_button.grid(row=3, column=0)

        self.test_button = Button(self.root, text="Test", command=self.test_connect, width=15)
        self.test_button.grid(row=3, column=1)

        self.address_entry.insert = (0, self.address_vmix)
        self.port_entry.insert = (0, self.port_vmix)

    def test_connect(self):
        url = self.address_entry.get()
        port = self.port_entry.get()
        try:
            req = requests.get('http://'+str(url)+':'+str(port)+'/API/')
            if req.status_code == 200:
                messagebox.showinfo("Информация: ", f"Связь установлена! Нажмите клавишу Ok")
                print(req)
        except:
            messagebox.showinfo("Информация: ", f"Нет связи с сервером!")
            print('Нет связи с сервером!')

    def pars(self):
        root = ET.parse('res/conf.xml').getroot()
        root_find = root.findall('setting/')
        for tag in root_find:
            url = tag.get('url')
            port = tag.get('port')
            data = [url, port]
            print(data)
        self.span = data

    def get_items(self):
        self.list_input.clear()
        self.items.clear()
        #os.system('curl -o res/vmix.xml http://'+ str(self.span[0]) +':'+ str(self.span[1]) +'/API')
        root = ET.parse('res/vmix.xml').getroot()
        root_find = root.findall('inputs/input')
        for x in root_find:
            key = x.get('key')
            inp = x.get('title')
            data_inp = {'Title':inp, 'GUID':key}
            self.list_input.append(data_inp)
        print(self.list_input)
        for y in self.list_input:
            title = y['Title']
            self.items.append(title)
        


    def show_message(self):
        url = self.address_entry.get()
        port = self.port_entry.get()
        messagebox.showinfo("GUI Python", f"{url}:{port}")

    def createXML(self):
        url = self.address_entry.get()
        port = self.port_entry.get()
        my_file = open('res/conf.xml', 'w')
        value = self.title_entry.get()
        root = xml.Element("vmix")
        #appt = xml.Element("appointment")
        appt = xml.Element("setting")
        root.append(appt)  # рутовый элемен
        # добавляем дочерний элемент к groupings
        groupby = xml.SubElement(appt, "config")
        groupby.set("url", url)  # устанавливаем аттрибут для groupby
        groupby.set("port", port)  # устанавливаем еще один аттрибут для groupby
        for y in self.list_input:
            title = y['Title']
            if value in title:
                key = y['GUID']
                groupby.set("key", key)
        #groupby.text = 'vMix Connection'
        message = xml.tostring(root, "utf-8")  # формируем XML документ в строку message
        # Добавляем строчку кодировки для xml файла
        doc = '<?xml version="1.0" encoding="UTF-8"?>' + message.decode("utf-8")
        # ##################### выводим результат формирования xml на экран ###########
        # меняем кодировку чтобы под виндовс было понятно что написано русскими буквами
        my_file.write(doc)
        my_file.close()
        self.root.destroy()

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()
