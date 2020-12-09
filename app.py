from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image
from tkcalendar import Calendar
import ics
import DB_manager
from datetime import datetime


class App:
    def __init__(self, db):
        self.name = "Meeting Scheduler"
        self.db = db

    def start(self):
        try:
            self.root = Tk()
            self.root.geometry("500x800")
            self.root.title(self.name)

            self.create_styles()

            image = Image.open("bg.jpg")
            image = image.resize((500, 800), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            background_label = Label(self.root, image=image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            title = Label(self.root, text=self.name, style='W.TLabel')
            title.pack(pady=50)
            self.show_main_page()

            self.root.mainloop()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def hide_main_page(self):
        try:
            self.add_person_button.pack_forget()
            self.add_meeting_button.pack_forget()
            self.show_meetings_button.pack_forget()
            self.export_button.pack_forget()
            self.import_button.pack_forget()
            self.exit.pack_forget()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def show_main_page(self):
        try:
            self.add_person_button = Button(self.root, text="Add person", style='W.TButton',
                                            command=self.add_person_window)
            self.add_meeting_button = Button(self.root, text="Schedule meeting", style='W.TButton',
                                             command=self.schedule_meeting)
            self.show_meetings_button = Button(self.root, text="Display meetings", style='W.TButton',
                                               command=self.show_meetings_window)
            self.export_button = Button(self.root, text="Export calendar", style='W.TButton',
                                        command=self.export_calendar_window)
            self.import_button = Button(self.root, text="Import calendar", style='W.TButton', command=self.callback)
            self.exit = Button(self.root, text="Exit", style='W.TButton', command=self.exit)

            self.add_person_button.pack(pady=20)
            self.add_meeting_button.pack(pady=20)
            self.show_meetings_button.pack(pady=20)
            self.export_button.pack(pady=20)
            self.import_button.pack(pady=20)
            self.exit.pack(pady=20)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def export_calendar_window(self):
        try:
            c = ics.Calendar()
            e = ics.Event()
            e1 = ics.Event()
            e.name = "Meeting"
            e.begin = '2014-01-01 10:00'
            e.end = '2014-01-01 20:00'
            e1.name = "Meeting 2"
            e1.begin = '2014-01-02 10:00'
            e1.end = '2014-01-02 20:00'
            c.events.add(e)
            c.events.add(e1)
            with open('my.ics', 'w') as my_file:
                my_file.writelines(c)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def show_meetings_window(self):
        try:
            self.hide_main_page()

            self.select_day = Button(self.root, text='Select day', style='W.TButton', command=self.show_calendar)
            self.select_day.pack(pady=10)
            self.selected_day = None
            self.meeting_day = None

            self.select_time_start = Button(self.root, text='Select start time', style='W.TButton',
                                            command=lambda: self.show_hour_picker(True))
            self.select_time_start.pack(pady=10)
            self.selected_time_start = None
            self.hour_meeting_start = None
            self.min_meeting_start = None

            self.select_time_end = Button(self.root, text='Select end time', style='W.TButton',
                                          command=lambda: self.show_hour_picker(False))
            self.select_time_end.pack(pady=10)
            self.selected_time_end = None
            self.hour_meeting_end = None
            self.min_meeting_end = None

            self.back = Button(self.root, text="Back", style='W.TButton', command=self.hide_show_meetings)
            self.save = Button(self.root, text="Display", style='W.TButton', command=self.display_meetings)
            self.back.pack(side="left", expand=True)
            self.save.pack(side="right", expand=True)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def hide_show_meetings(self):
        try:
            self.select_day.pack_forget()
            self.select_time_start.pack_forget()
            self.select_time_end.pack_forget()
            if self.selected_day:
                self.selected_day.pack_forget()
            if self.selected_time_start:
                self.selected_time_start.pack_forget()
            if self.selected_time_end:
                self.selected_time_end.pack_forget()
            self.back.pack_forget()
            self.save.pack_forget()
            self.show_main_page()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def display_meetings(self):
        if self.meeting_day and self.hour_meeting_start and self.min_meeting_start and self.hour_meeting_end and self.min_meeting_end:
            try:
                meetings = self.db.get_meetings_by_interval(self.meeting_day,
                                                            self.hour_meeting_start + ":" + self.min_meeting_start,
                                                            self.hour_meeting_end + ":" + self.min_meeting_end)
                if len(meetings) != 0:
                    self.display_meetings_window = Toplevel(self.root)
                    self.display_meetings_window.geometry("1000x300")
                    for i in range(len(meetings)):
                        entry = Entry(self.display_meetings_window, width=25, font=('Lato', 12, 'normal'),
                                      justify=CENTER)
                        entry.grid(row=i + 1, column=1, pady=1, padx=1)
                        entry.insert(END, "Id: " + str(meetings[i][0]))
                        entry = Entry(self.display_meetings_window, width=25, font=('Lato', 12, 'normal'),
                                      justify=CENTER)
                        entry.grid(row=i + 1, column=2, pady=1, padx=1)
                        entry.insert(END, meetings[i][1])
                        entry = Entry(self.display_meetings_window, width=25, font=('Lato', 12, 'normal'),
                                      justify=CENTER)
                        entry.grid(row=i + 1, column=3, pady=1, padx=1)
                        entry.insert(END, "Start time: " + meetings[i][2].strftime("%H:%M:%S"))
                        entry = Entry(self.display_meetings_window, width=25, font=('Lato', 12, 'normal'),
                                      justify=CENTER)
                        entry.grid(row=i + 1, column=4, pady=1, padx=1)
                        entry.insert(END, "End time: " + meetings[i][3].strftime("%H:%M:%S"))
                else:
                    failure_window = Toplevel(self.root)
                    Label(failure_window, text="No meetings in this interval", font="Lato 14", foreground='red',
                          justify='center').pack(pady=20, padx=20)
            except Exception as error:
                self.display_meetings_window.withdraw()
                failure_window = Toplevel(self.root)
                Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20,
                                                                                                           padx=20)
        else:
            failure_window = Toplevel(self.root)
            Label(failure_window, text="Error! You haven't set all data!", font="Lato 14", foreground='red',
                  justify='center').pack(pady=20, padx=20)

    def add_person_window(self):
        try:
            self.hide_main_page()

            self.nume = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
            self.nume.insert(0, 'Please enter your Last Name!')
            self.nume.pack(pady=20)

            self.prenume = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
            self.prenume.insert(0, 'Please enter your First Name!')
            self.prenume.pack(pady=20)

            self.back = Button(self.root, text="Back", style='W.TButton', command=self.hide_add_person)
            self.save = Button(self.root, text="Save", style='W.TButton', command=self.save_person)
            self.back.pack(side="left", expand=True)
            self.save.pack(side="right", expand=True)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def hide_add_person(self):
        try:
            self.nume.pack_forget()
            self.prenume.pack_forget()
            self.back.pack_forget()
            self.save.pack_forget()
            self.show_main_page()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def save_person(self):
        try:
            self.db.insert_person(self.nume.get(), self.prenume.get())
            success_window = Toplevel(self.root)
            Label(success_window, text="Person saved successfully", font="Lato 14", foreground='green',
                  justify='center').pack(pady=20, padx=20)
            self.nume.pack_forget()
            self.prenume.pack_forget()
            self.back.pack_forget()
            self.save.pack_forget()
            self.show_main_page()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def schedule_meeting(self):
        try:
            self.hide_main_page()

            self.select_day = Button(self.root, text='Select day', style='W.TButton', command=self.show_calendar)
            self.select_day.pack(pady=10)
            self.selected_day = None
            self.meeting_day = None

            self.select_time_start = Button(self.root, text='Select start time', style='W.TButton',
                                            command=lambda: self.show_hour_picker(True))
            self.select_time_start.pack(pady=10)
            self.selected_time_start = None
            self.hour_meeting_start = None
            self.min_meeting_start = None

            self.select_time_end = Button(self.root, text='Select end time', style='W.TButton',
                                          command=lambda: self.show_hour_picker(False))
            self.select_time_end.pack(pady=10)
            self.selected_time_end = None
            self.hour_meeting_end = None
            self.min_meeting_end = None

            self.select_participants = Button(self.root, text='Add participants', style='W.TButton',
                                              command=lambda: self.add_participants())
            self.select_participants.pack(pady=10)
            self.list_participants = None
            self.selected_participants = None

            self.back = Button(self.root, text="Back", style='W.TButton', command=self.hide_schedule_meeting)
            self.save = Button(self.root, text="Save", style='W.TButton', command=self.save_schedule)
            self.back.pack(side="left", expand=True)
            self.save.pack(side="right", expand=True)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def add_participants(self):
        try:
            self.add_participants_window = Toplevel(self.root)
            self.add_participants_window.geometry("400x700")
            Label(self.add_participants_window, text="List of Participants", font="Lato 14", justify=CENTER).pack(
                pady=20)
            self.list_box = Listbox(self.add_participants_window, width="100", font="Lato 14", fg="#bb99ff")
            self.list_box.pack(pady=15)

            Label(self.add_participants_window, text="Id participant:", font="Lato 14", justify=CENTER).pack(pady=10)
            participant = Entry(self.add_participants_window, width='35', font=('Lato', 12, 'normal'), justify=CENTER)
            participant.pack(pady=20)

            reg = self.root.register(self.hour_input)

            participant.config(validate="key", validatecommand=(reg, '%P'))

            add_person = Button(self.add_participants_window, text="Add", style='W.TButton',
                                command=lambda: self.select_participant(participant.get()))
            add_person.pack(pady=10)
            delete_person = Button(self.add_participants_window, text="Delete", style='W.TButton',
                                   command=lambda: self.delete_participant())
            delete_person.pack(pady=10)
            save_list_participants = Button(self.add_participants_window, text="Save", style='W.TButton',
                                            command=lambda: self.save_participants())
            save_list_participants.pack(pady=10)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def select_participant(self, participant_name):
        try:
            self.list_box.insert(END, participant_name)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def delete_participant(self):
        try:
            self.list_box.delete(ANCHOR)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def save_participants(self):
        try:
            list_participants = self.list_box.get(0, self.list_box.size() - 1)
            # self.list_participants = [participant.split(" ") for participant in list_participants]
            self.list_participants = set(list_participants)
            if self.selected_participants:
                self.selected_participants.pack_forget()
            self.selected_participants = Label(self.root, text="Participants: " + ','.join(self.list_participants),
                                               font="Lato 14")
            self.selected_participants.pack()
            self.add_participants_window.withdraw()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def hide_schedule_meeting(self):
        try:
            self.select_day.pack_forget()
            self.select_time_start.pack_forget()
            self.select_time_end.pack_forget()
            self.select_participants.pack_forget()
            if self.selected_day:
                self.selected_day.pack_forget()
            if self.selected_time_start:
                self.selected_time_start.pack_forget()
            if self.selected_time_end:
                self.selected_time_end.pack_forget()
            if self.selected_participants:
                self.selected_participants.pack_forget()
            self.back.pack_forget()
            self.save.pack_forget()
            self.show_main_page()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def save_schedule(self):
        if self.meeting_day and self.hour_meeting_start and self.min_meeting_start and self.hour_meeting_end and self.min_meeting_end and self.list_participants:
            try:
                self.db.insert_meeting(self.meeting_day, self.hour_meeting_start + ":" + self.min_meeting_start,
                                       self.hour_meeting_end + ":" + self.min_meeting_end,
                                       self.list_participants)
                success_window = Toplevel(self.root)
                Label(success_window, text="Meeting saved successfully", font="Lato 14", foreground='green',
                      justify='center').pack(pady=20, padx=20)
                self.db.get_scheduler()
                self.hide_schedule_meeting()
            except Exception as error:
                failure_window = Toplevel(self.root)
                Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20,
                                                                                                           padx=20)
        else:
            failure_window = Toplevel(self.root)
            Label(failure_window, text="Error! Meeting wasn't saved beacause you haven't set all data!", font="Lato 14",
                  foreground='red',
                  justify='center').pack(pady=20, padx=20)

    def show_calendar(self):
        try:
            self.calendar_window = Toplevel(self.root)

            now = datetime.now()
            year = int(now.strftime("%Y"))
            month = int(now.strftime("%m"))
            day = int(now.strftime("%d"))
            self.calendar = Calendar(self.calendar_window, font="Lato 12", selectmode='day', cursor="hand1", year=year,
                                     month=month, day=day)
            self.calendar.pack(fill="both", expand=True)
            Button(self.calendar_window, text="OK", command=self.get_date).pack()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def get_date(self):
        try:
            self.meeting_day = self.calendar.selection_get()
            if self.selected_day:
                self.selected_day.pack_forget()
            self.selected_day = Label(self.root, text=self.meeting_day, font="Lato 14")
            self.selected_day.pack()
            self.calendar_window.withdraw()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def show_hour_picker(self, is_start_hour):
        try:
            self.hour_window = Toplevel(self.root)
            self.hour_window.geometry("200x350")
            Label(self.hour_window, text="Enter the hour(HH):", font="Lato 14").pack(pady=20)
            self.hour = Entry(self.hour_window, width='10', font=('Lato', 12, 'normal'), justify=CENTER)
            self.hour.pack(pady=10)
            Label(self.hour_window, text="Enter the minutes(MM):", font="Lato 14").pack(pady=20)
            self.min = Entry(self.hour_window, width='10', font=('Lato', 12, 'normal'), justify=CENTER)
            self.min.pack(pady=10)

            reg = self.root.register(self.hour_input)

            self.hour.config(validate="key", validatecommand=(reg, '%P'))
            self.min.config(validate="key", validatecommand=(reg, '%P'))

            Button(self.hour_window, text="OK", command=lambda: self.get_hour(is_start_hour)).pack()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def hour_input(self, input):
        try:
            if input.isdigit():
                return True
            elif input is "":
                return True
            else:
                return False
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def get_hour(self, is_start_hour):
        try:
            time_no_valid = Label(self.hour_window, text="The time you entered is not valid", font="Lato 12",
                                  foreground='red', wraplength='150', justify='center')
            hour = self.hour.get()
            min = self.min.get()
            if hour == '' or min == '' or len(hour) != 2 or len(min) != 2:
                time_no_valid.pack(pady=20)
            else:
                hour = int(hour)
                min = int(min)
                self.validate_time(hour, min, is_start_hour, time_no_valid)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def validate_time(self, hour, min, is_start_hour, time_no_valid):
        try:
            if 24 > hour >= 0 and 0 <= min < 60:
                if is_start_hour:
                    if self.selected_time_start:
                        self.selected_time_start.pack_forget()
                    if self.selected_time_end and (int(self.hour_meeting_end) < hour or (
                            int(self.hour_meeting_end) == hour and int(self.min_meeting_end) < min)):
                        time_no_valid.pack(pady=20)
                    else:
                        self.hour_meeting_start = self.hour.get()
                        self.min_meeting_start = self.min.get()
                        self.selected_time_start = Label(self.root,
                                                         text="Start: " + self.hour_meeting_start + ':' + self.min_meeting_start,
                                                         font="Lato 14")
                        self.selected_time_start.pack()
                        self.hour_window.withdraw()
                else:
                    if self.selected_time_end:
                        self.selected_time_end.pack_forget()
                    if self.selected_time_start and (int(self.hour_meeting_start) > hour or (
                            int(self.hour_meeting_start) == hour and int(self.min_meeting_start) > min)):
                        time_no_valid.pack(pady=20)
                    else:
                        self.hour_meeting_end = self.hour.get()
                        self.min_meeting_end = self.min.get()
                        self.selected_time_end = Label(self.root,
                                                       text="End: " + self.hour_meeting_end + ':' + self.min_meeting_end,
                                                       font="Lato 14")
                        self.selected_time_end.pack()
                        self.hour_window.withdraw()

            else:
                time_no_valid.pack(pady=20)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def callback(self):
        print(1)

    def exit(self):
        try:
            self.root.destroy()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def create_styles(self):
        try:
            style = Style()
            style.configure('W.TButton', font=('Lato', 15, 'bold'), background='#bb99ff', foreground='#bb99ff')
            style.configure('W.TButton', padding=10, borderwidth=0)
            style.configure('W.TLabel', font=('Lato', 20, 'bold'), foreground='#bb99ff', wraplength='250',
                            justify='center')
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)


if __name__ == '__main__':
    try:
        db = DB_manager.DB_manager()
        db.connect()
        # db.create_tables()
        app = App(db)
        app.start()
    except Exception as error:
        print(error)
