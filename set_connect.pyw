from tkinter import *
from tkinter import messagebox
import xml.etree.ElementTree as xml
import xml.etree.ElementTree as ET
import requests
class SetConnect:
    def __init__(self, parent, title = "Настройки", icon=None):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.span = []
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
        self.address_entry = Entry(self.root, textvariable=self.address_vmix, width=20)
        self.address_entry.grid(row=0, column=1)

        self.port_lbl = Label(self.root, text="Порт vMix: ").grid(row=1, column=0)
        self.port_entry = Entry(self.root, textvariable=self.port_vmix, width=20)
        self.port_entry.grid(row=1, column=1)

        self.test_button = Button(self.root, text="Test", command=self.test_connect, width=15)
        self.test_button.grid(row=2, column=1)

        self.ok_button = Button(self.root, text="Ok", command=self.createXML, width=15)
        self.ok_button.grid(row=2, column=0)

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


    def show_message(self):
        url = self.address_entry.get()
        port = self.port_entry.get()
        messagebox.showinfo("GUI Python", f"{url}:{port}")

    def createXML(self):
        url = self.address_entry.get()
        port = self.port_entry.get()
        my_file = open('res/conf.xml', 'w')

        root = xml.Element("vmix")
        #appt = xml.Element("appointment")
        appt = xml.Element("setting")
        root.append(appt)  # рутовый элемен
        # добавляем дочерний элемент к groupings
        groupby = xml.SubElement(appt, "config")
        groupby.set("url", url)  # устанавливаем аттрибут для groupby
        groupby.set("port", port)  # устанавливаем еще один аттрибут для groupby
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
