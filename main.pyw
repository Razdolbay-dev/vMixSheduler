from manager import *
from set_connect import *
from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as xml
from PIL import Image as PilImage
from PIL import ImageTk

class Main:
    def __init__(self, title = "Добро пожаловать! vMixSheduler", icon=r"res/pencil.ico"):
        self.root = Tk()
        self.root.title(title)
        self.tree = ttk.Treeview(self.root, columns=('Title', 'GUID', 'Duration', 'Start', 'End'), height=15, show='headings')
        # Обработка иконки для кнопок
        img_pencl = PilImage.open(r"res/manager.png")
        img_pencl = img_pencl.resize((25,25), PilImage.ANTIALIAS)
        self.icon_mng =  ImageTk.PhotoImage(img_pencl)
        img_clock = PilImage.open(r"res/update.png")
        img_clock = img_clock.resize((25,25), PilImage.ANTIALIAS)
        self.icon_clc =  ImageTk.PhotoImage(img_clock)
        img_tune = PilImage.open(r"res/tune.png")
        img_tune = img_tune.resize((25,25), PilImage.ANTIALIAS)
        self.icon_tun =  ImageTk.PhotoImage(img_tune)
        # Кнопки в топ баре
        if icon:
            self.root.iconbitmap(icon)
        
    def run(self):
        self.draw_wigets()
        self.root.mainloop()
    
    def cmd(self):
        pass

    def run_manger(self):
        Manager(self.root)

    def run_connect(self):
        SetConnect(self.root)

    def draw_wigets(self):
        self.draw_menu()
        self.draw_tree()
        
    def draw_tree(self):
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
        self.tree.pack(side=LEFT, expand="yes", fill=BOTH)

    def draw_menu(self):
        # menu_bar
        menubar = Menu(self.root)
        fileMenu = Menu(self.root, tearoff=0, bg='black')
        fileMenu.add_command(label="Менеджер", command=self.run_manger)
        toolbar = Frame(self.root, bd=1, relief=RAISED)
        # Open Manager
        open_mng = Button(
            toolbar, image=self.icon_mng, relief=FLAT,
            command=self.run_manger
        )
        open_mng.image = self.icon_mng
        open_mng.pack(side=LEFT, padx=2, pady=2)
        # Update
        upd = Button(
            toolbar, image=self.icon_clc, relief=FLAT,
            command=self.run_manger
        )
        upd.image = self.icon_clc
        upd.pack(side=LEFT, padx=2, pady=2)
        # Update
        tune = Button(
            toolbar, image=self.icon_tun, relief=FLAT,
            command=self.run_connect
        )
        tune.image = self.icon_tun
        tune.pack(side=LEFT, padx=2, pady=2)
        # Compil
        toolbar.pack(side=TOP, fill=X)
        self.root.configure(menu=menubar)

if __name__ == "__main__":
    root = Main()
    root.run_manger()
    root.run()