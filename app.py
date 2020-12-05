from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image


class App:
    def __init__(self):
        self.name = "Meeting Scheduler"

    def start(self):
        self.root = Tk()
        self.root.geometry("500x500")

        self.create_styles()

        title = Label(self.root, text=self.name, style='W.TLabel')
        title.pack(pady=40)

        # image = PhotoImage(file='rsz_5895d2d1cba9841eabab6077.png')
        self.showMainPage()

        self.root.mainloop()

    def add_person_window(self):
        self.add_person_button.pack_forget()
        self.add_meeting_button.pack_forget()
        self.show_meetings_button.pack_forget()
        self.export_button.pack_forget()

        self.nume = Entry(self.root, width='50')
        self.nume.insert(0, 'Please enter your name!')
        self.nume.pack(pady=20)

        self.prenume = Entry(self.root, width='50')
        self.prenume.insert(0, 'Please enter your sirname!')
        self.prenume.pack(pady=20)

        self.back = Button(self.root, text="Back", style='W.TButton', command=self.add_person_back)
        self.save = Button(self.root, text="Save", style='W.TButton', command=self.save_person)
        self.back.pack(side="left", expand=True)
        self.save.pack(side="right", expand=True)

    def add_person_back(self):
        self.nume.pack_forget()
        self.prenume.pack_forget()
        self.back.pack_forget()
        self.save.pack_forget()
        self.showMainPage()

    def save_person(self):
        self.nume.pack_forget()
        self.prenume.pack_forget()
        self.back.pack_forget()
        self.save.pack_forget()
        self.showMainPage()

    def showMainPage(self):
        self.add_person_button = Button(self.root, text="Add person", style='W.TButton', command=self.add_person_window)
        self.add_meeting_button = Button(self.root, text="Schedule meeting", style='W.TButton', command=self.callback)
        self.show_meetings_button = Button(self.root, text="Display meetings", style='W.TButton', command=self.callback)
        self.export_button = Button(self.root, text="Export calendar", style='W.TButton', command=self.callback)

        self.add_person_button.pack(pady=20)
        self.add_meeting_button.pack(pady=20)
        self.show_meetings_button.pack(pady=20)
        self.export_button.pack(pady=20)
        print(1)

    def callback(self):
        print(1)

    def create_styles(self):
        # image = Image.open('rsz_5895d2d1cba9841eabab6077.png')
        # image = image.resize((100, 40), Image.ANTIALIAS)
        # image = ImageTk.PhotoImage(image)
        style = Style()
        # style.theme_use('clam')
        style.configure('W.TButton', font=('Lato', 15, 'bold'), background='#bb99ff', foreground='#bb99ff')
        style.configure('W.TButton', padding=10, borderwidth=0)
        # style.theme_use('default')
        style.configure('W.TLabel', font=('Lato', 20, 'bold'), foreground='#bb99ff', wraplength='250', justify='center')


if __name__ == '__main__':
    app = App()
    app.start()
