from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image

from tkcalendar import Calendar


class App:
    def __init__(self):
        self.name = "Meeting Scheduler"

    def start(self):
        self.root = Tk()
        self.root.geometry("500x500")
        self.root.title(self.name)

        self.create_styles()

        title = Label(self.root, text=self.name, style='W.TLabel')
        title.pack(pady=40)

        # image = PhotoImage(file='rsz_5895d2d1cba9841eabab6077.png')
        self.show_main_page()

        self.root.mainloop()

    def hide_main_page(self):
        self.add_person_button.pack_forget()
        self.add_meeting_button.pack_forget()
        self.show_meetings_button.pack_forget()
        self.export_button.pack_forget()

    def show_main_page(self):
        self.add_person_button = Button(self.root, text="Add person", style='W.TButton', command=self.add_person_window)
        self.add_meeting_button = Button(self.root, text="Schedule meeting", style='W.TButton',
                                         command=self.schedule_meeting)
        self.show_meetings_button = Button(self.root, text="Display meetings", style='W.TButton', command=self.callback)
        self.export_button = Button(self.root, text="Export calendar", style='W.TButton', command=self.callback)

        self.add_person_button.pack(pady=20)
        self.add_meeting_button.pack(pady=20)
        self.show_meetings_button.pack(pady=20)
        self.export_button.pack(pady=20)
        print(1)

    def add_person_window(self):
        self.hide_main_page()

        self.nume = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
        self.nume.insert(0, 'Please enter your name!')
        self.nume.pack(pady=20)

        self.prenume = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
        self.prenume.insert(0, 'Please enter your Surname!')
        self.prenume.pack(pady=20)

        self.back = Button(self.root, text="Back", style='W.TButton', command=self.hide_add_person)
        self.save = Button(self.root, text="Save", style='W.TButton', command=self.save_person)
        self.back.pack(side="left", expand=True)
        self.save.pack(side="right", expand=True)

    def hide_add_person(self):
        self.nume.pack_forget()
        self.prenume.pack_forget()
        self.back.pack_forget()
        self.save.pack_forget()
        self.show_main_page()

    def save_person(self):
        print(self.nume.get())
        print(self.prenume.get())

        self.nume.pack_forget()
        self.prenume.pack_forget()
        self.back.pack_forget()
        self.save.pack_forget()
        self.show_main_page()

    def schedule_meeting(self):
        self.hide_main_page()

        self.select_day = Button(self.root, text='Select day', style='W.TButton', command=self.show_calendar)
        self.select_day.pack(pady=10)

        self.select_time = Button(self.root, text='Select time', style='W.TButton', command=self.show_hour_picker)
        self.select_time.pack(pady=10)

    def show_calendar(self):
        self.calendar_window = Toplevel(self.root)

        self.calendar = Calendar(self.calendar_window, font="Lato 12", selectmode='day', cursor="hand1", year=2020,
                                 month=11, day=5)
        self.calendar.pack(fill="both", expand=True)
        Button(self.calendar_window, text="OK", command=self.get_date).pack()

    def get_date(self):
        self.meeting_day = self.calendar.selection_get()
        Label(self.root, text=self.meeting_day, font="Lato 14").pack()
        print(self.meeting_day)
        self.calendar_window.withdraw()

    def show_hour_picker(self):
        self.hour_window = Toplevel(self.root)
        self.hour_window.geometry("200x350")
        Label(self.hour_window, text="Enter the hour:", font="Lato 14").pack(pady=20)
        self.hour = Entry(self.hour_window, width='10', font=('Lato', 12, 'normal'), justify=CENTER)
        self.hour.pack(pady=10)
        Label(self.hour_window, text="Enter the minutes:", font="Lato 14").pack(pady=20)
        self.min = Entry(self.hour_window, width='10', font=('Lato', 12, 'normal'), justify=CENTER)
        self.min.pack(pady=10)

        reg = self.root.register(self.hour_input)

        self.hour.config(validate="key", validatecommand=(reg, '%P'))
        self.min.config(validate="key", validatecommand=(reg, '%P'))

        Button(self.hour_window, text="OK", command=self.get_hour).pack()

    def hour_input(self, input):
        if input.isdigit():
            return True
        elif input is "":
            return True
        else:
            return False

    def get_hour(self):
        time_no_valid = Label(self.hour_window, text="The time you entered is not valid", font="Lato 12",
                              foreground='red', wraplength='150', justify='center')
        hour = self.hour.get()
        min = self.min.get()
        if hour == '' or min == '':
            time_no_valid.pack(pady=20)
        else:
            hour = int(hour)
            min = int(min)
            if 24 > hour >= 0 and 0 <= min < 60:
                # self.time_no_valid.pack_forget()
                self.hour_meeting = self.hour.get()
                self.min_meeting = self.min.get()
                Label(self.root, text=self.hour_meeting + ':' + self.min_meeting, font="Lato 14").pack()
                self.hour_window.withdraw()
            else:
                time_no_valid.pack(pady=20)

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
