from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

from PIL import ImageTk, Image
from tkcalendar import Calendar
import ics
import DB_manager
from datetime import datetime


class App:
    """
    The class manages the GUI application.
    """

    def __init__(self, db):
        """
        Initialize the database to which we make requests and the name of the app which will appear on the windows

        :param db: represents the database for our application
        """
        self.name = "Meeting Scheduler"
        self.db = db

    def start(self):
        """
        The method starts the application creating the main window with the background
        and the title of the application

        :return: displays the created window and creates a window with an exception if encountered
        """
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
        """
        The method hides the main page when we navigate to an option.

        :return: hides the buttons form the main page and creates a window with an exception if encountered
        """
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
        """
        The method displays all the buttons form the main page when we want to return to the main page.
        The buttons: add a person, add a meeting to the database, display only some meetings
        and import/export calendars with meetings

        :return: displays the main page and creates a window with an exception if encountered
        """
        try:
            self.add_person_button = Button(self.root, text="Add person", style='W.TButton',
                                            command=self.add_person_window)
            self.add_meeting_button = Button(self.root, text="Schedule meeting", style='W.TButton',
                                             command=self.schedule_meeting)
            self.show_meetings_button = Button(self.root, text="Display meetings", style='W.TButton',
                                               command=self.show_meetings_window)
            self.export_button = Button(self.root, text="Export calendar", style='W.TButton',
                                        command=self.export_calendar_window)
            self.import_button = Button(self.root, text="Import calendar", style='W.TButton',
                                        command=self.import_calendar_window)
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

    def import_calendar_window(self):
        """
        The method opens a dialog file from which the user chooses an .ical or .ics file to import into the database.
        The information imported are: the name and the date of the meeting including the start and end hours
        and the participants of the meeting only if they are already in the database

        :return: a success window if the calendar got imported into the database
                 and creates a window with an exception if encountered
        """
        try:
            files = [("ics files", "*.ics"), ("ical files", "*.ical")]
            file = filedialog.askopenfilename(initialdir="/", title="Select a calendar file", filetypes=files)
            with open(file, 'r') as my_file:
                c = ics.Calendar(my_file.read())
            events = c.events
            for event in events:
                name = event.name
                day = event.begin.format('YYYY-MM-DD')
                start = event.begin.format('HH:mm')
                end = event.end.format('HH:mm')
                attendees = []
                for attendee in event.attendees:
                    attendees.append(attendee.common_name)
                self.db.insert_meeting(name, day, start, end, attendees)
            success_window = Toplevel(self.root)
            Label(success_window, text="Calendar imported successfully", font="Lato 14", foreground='green',
                  justify='center').pack(pady=20, padx=20)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def export_calendar_window(self):
        """
        The method opens a dialog file from which the user chooses an .ical or .ics file to export
        all the meetings from the database.
        The exported information are: the name and the date of the meetings including the start and end hours
        and the emails of the participants of the meetings.

        :return: a success window if the calendar got exported from the database
                 and creates a window with an exception if encountered
        """
        try:
            c = ics.Calendar()
            meetings = self.db.get_meetings()
            for meeting in meetings:
                e = ics.Event()
                e.name = str(meeting[1])
                e.begin = meeting[2].strftime("%Y-%m-%d") + " " + meeting[3].strftime("%H:%M")
                e.end = meeting[2].strftime("%Y-%m-%d") + " " + meeting[4].strftime("%H:%M")
                participants = self.db.get_scheduler_by_meeting(str(meeting[0]))
                for participant in participants:
                    e.add_attendee(str(participant[0]))
                c.events.add(e)
            files = [("ics files", "*.ics"), ("ical files", "*.ical")]
            file = filedialog.asksaveasfile(initialdir="/", title="Save a calendar file", filetypes=files,
                                            defaultextension=files)
            with open(file.name, 'w') as my_file:
                my_file.writelines(c)
            success_window = Toplevel(self.root)
            Label(success_window, text="Calendar exported successfully", font="Lato 14", foreground='green',
                  justify='center').pack(pady=20, padx=20)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def show_meetings_window(self):
        """
        The method display a window where you can set a time interval from which you want to see all the meetings

        :return: displays the window with its buttons for setting the interval
                 and creates a window with an exception if encountered
        """
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
        """
        The method hides all the buttons for the display meetings windows and displays the ones from the main page

        :return: displays the main page and hides the show meetings pages
                 and creates a window with an exception if encountered
        """
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
        """
        The method created a new window where all the meetings from a set interval are displayed in a tabel
        with a meeting on each row, each meeting having the name, the day, start and end hour displayed
        as well as a button where you cna see the participants for that meeting.

        :return: creates a window for displaying the meetings information from an interval of time
                 and creates a window with an exception if encountered
        """
        if self.meeting_day and self.hour_meeting_start and self.min_meeting_start and self.hour_meeting_end and self.min_meeting_end:
            try:
                meetings = self.db.get_meetings_by_interval(self.meeting_day,
                                                            self.hour_meeting_start + ":" + self.min_meeting_start,
                                                            self.hour_meeting_end + ":" + self.min_meeting_end)
                if len(meetings) != 0:
                    self.display_meetings_window = Toplevel(self.root)
                    self.display_meetings_window.geometry("1200x300")
                    for i in range(len(meetings)):
                        entry = Entry(self.display_meetings_window, width=25, font=('Lato', 12, 'normal'),
                                      justify=CENTER)
                        entry.grid(row=i + 1, column=1, pady=1, padx=1)
                        entry.insert(END, "Name: " + str(meetings[i][0]))
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
                        participants = Button(self.display_meetings_window, text='See participants', style='W.TButton',
                                              command=lambda: self.get_participants_from_meeting(meetings[i][4]))
                        participants.grid(row=i + 1, column=5, pady=1, padx=1)
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

    def get_participants_from_meeting(self, meeting_id):
        """
        The method creates a new window where the participants' emails from a meeting are displayed.

        :param meeting_id: represents the meeting for which we want to see the persons

        :return: creates a window where participants are displayed and creates a window with an exception if encountered
        """
        self.get_participants_from_meeting_window = Toplevel(self.display_meetings_window)
        self.get_participants_from_meeting_window.geometry("400x400")
        scrollbar = Scrollbar(self.get_participants_from_meeting_window)
        scrollbar.pack(side=RIGHT, fill=Y)
        Label(self.get_participants_from_meeting_window, text="List of Participants", font="Lato 14",
              justify=CENTER).pack(pady=20)
        self.list_box_participants = Listbox(self.get_participants_from_meeting_window, width="100", font="Lato 14",
                                             fg="#bb99ff", yscrollcommand=scrollbar.set)
        self.list_box_participants.pack(pady=15)

        try:
            all_persons = self.db.get_scheduler_by_meeting(meeting_id)
            for person in all_persons:
                self.list_box_participants.insert(END, person[0])
        except Exception as error:
            failure_window = Toplevel(self.display_meetings_window)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20,
                                                                                                       padx=20)

    def add_person_window(self):
        """
        The method displays a window where you cna add a person to the database.
        Three entries are displayed where the user should introduce the first and last name of the person
        as well as the person's email.

        :return: displays a window for adding new persons and creates a window with an exception if encountered
        """
        try:
            self.hide_main_page()

            self.nume = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
            self.nume.insert(0, 'Please enter your Last Name!')
            self.nume.pack(pady=20)

            self.prenume = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
            self.prenume.insert(0, 'Please enter your First Name!')
            self.prenume.pack(pady=20)

            self.email = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
            self.email.insert(0, 'Please enter your email adress!')
            self.email.pack(pady=20)

            self.back = Button(self.root, text="Back", style='W.TButton', command=self.hide_add_person)
            self.save = Button(self.root, text="Save", style='W.TButton', command=self.save_person)
            self.back.pack(side="left", expand=True)
            self.save.pack(side="right", expand=True)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def hide_add_person(self):
        """
        The method hides the window for adding new persons to the database and displays the main page.

        :return: displays the main page, hides the actual window and creates a window with an exception if encountered
        """
        try:
            self.email.pack_forget()
            self.nume.pack_forget()
            self.prenume.pack_forget()
            self.back.pack_forget()
            self.save.pack_forget()
            self.show_main_page()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def save_person(self):
        """
        The method takes the input form the user and adds a person to the database, displaying the main page afterwards.

        :return: creates a success window if the person is added to the database and displays the main page
                 or creates a window with an exception if encountered
        """
        try:
            self.db.insert_person(self.email.get(), self.nume.get(), self.prenume.get())
            success_window = Toplevel(self.root)
            Label(success_window, text="Person saved successfully", font="Lato 14", foreground='green',
                  justify='center').pack(pady=20, padx=20)
            self.email.pack_forget()
            self.nume.pack_forget()
            self.prenume.pack_forget()
            self.back.pack_forget()
            self.save.pack_forget()
            self.show_main_page()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def schedule_meeting(self):
        """
        The method displays a window where a new meeting can be scheduled and added into the database.
        The new meeting should have a name, the day when it's happening along with its start and end hour
        as well as the participants for the meeting.

        :return: displays all the buttons for adding a new meeting into the database
                 and creates a window with an exception if encountered
        """
        try:
            self.hide_main_page()

            self.meeting_name = Entry(self.root, width='50', font=('Lato', 12, 'normal'))
            self.meeting_name.insert(0, 'Please enter the name of the meeting!')
            self.meeting_name.pack(pady=20)

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
            self.list_participants = set()

            self.see_participants = Button(self.root, text='See participants', style='W.TButton',
                                           command=lambda: self.show_selected_participants())
            self.see_participants.pack(pady=10)

            self.back = Button(self.root, text="Back", style='W.TButton', command=self.hide_schedule_meeting)
            self.save = Button(self.root, text="Save", style='W.TButton', command=self.save_schedule)
            self.back.pack(side="left", expand=True)
            self.save.pack(side="right", expand=True)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def add_participants(self):
        """
        The method creates two new windows: one in which all the persons from the database are displayed
        and from which you can select who you want to attend the meeting and the other window where
        you see all the participants you have added and can edit the list if necessary.

        :return: creates 2 windows for managing the participants for a meeting
                 and creates a window with an exception if encountered
        """
        try:
            self.add_participants_window = Toplevel(self.root)
            self.add_participants_window.geometry("400x700")
            scrollbar = Scrollbar(self.add_participants_window)
            scrollbar.pack(side=RIGHT, fill=Y)
            Label(self.add_participants_window, text="List of Participants", font="Lato 14", justify=CENTER).pack(
                pady=20)
            self.list_box = Listbox(self.add_participants_window, width="100", font="Lato 14", fg="#bb99ff",
                                    yscrollcommand=scrollbar.set)
            self.list_box.pack(pady=15)

            self.display_participants_window = Toplevel(self.root)
            self.display_participants_window.geometry("400x700")
            scrollbar = Scrollbar(self.display_participants_window)
            scrollbar.pack(side=RIGHT, fill=Y)
            Label(self.display_participants_window, text="Select the Participants", font="Lato 14",
                  justify=CENTER).pack(pady=20)
            self.list_box_select = Listbox(self.display_participants_window, width="100", font="Lato 14", fg="#bb99ff",
                                           yscrollcommand=scrollbar.set)
            self.list_box_select.pack(pady=15)

            try:
                all_persons = self.db.get_persons()
                for person in all_persons:
                    self.list_box_select.insert(END, person[1])
            except Exception as error:
                failure_window = Toplevel(self.root)
                Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20,
                                                                                                           padx=20)

            add_person = Button(self.display_participants_window, text="Add", style='W.TButton',
                                command=lambda: self.select_participant(self.list_box_select.get(ACTIVE)))
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

    def show_selected_participants(self):
        """
        The method creates a new window where you can check the participants for the meeting you want to add
        before you save it.

        :return: creates a window for displaying the participants of a new meeting
                 and creates a window with an exception if encountered
        """
        self.display_selected_participants_window = Toplevel(self.root)
        self.display_selected_participants_window.geometry("400x700")
        scrollbar = Scrollbar(self.display_selected_participants_window)
        scrollbar.pack(side=RIGHT, fill=Y)
        Label(self.display_selected_participants_window, text="Selected Participants", font="Lato 14",
              justify=CENTER).pack(pady=20)
        self.list_box_display = Listbox(self.display_selected_participants_window, width="100", font="Lato 14",
                                        fg="#bb99ff",
                                        yscrollcommand=scrollbar.set)
        self.list_box_display.pack(pady=15)

        try:
            all_persons = self.list_participants
            for person in all_persons:
                self.list_box_display.insert(END, person)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20,
                                                                                                       padx=20)

    def select_participant(self, participant_name):
        """
        The method lets the user select a participant from a window and add him to the list of persons
        for the new meeting.

        :param participant_name: the participant we want to add in the meeting

        :return: adds participants to the meeting or creates a window with an exception if encountered
        """
        try:
            self.list_box.insert(END, participant_name)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def delete_participant(self):
        """
        The method lets the user modify the list he has made for the meeting by deleting mistaken persons.

        :return: deletes a person from the list of participants or creates a window with an exception if encountered
        """
        try:
            self.list_box.delete(ANCHOR)
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def save_participants(self):
        """
        The method saves the final list of participants for a meeting,
        choosing a person only once if there are duplicates.

        :return: creates the list of participants or creates a window with an exception if encountered
        """
        try:
            list_participants = self.list_box.get(0, self.list_box.size() - 1)
            self.list_participants = set(list_participants)
            success_window = Toplevel(self.root)
            Label(success_window, text="List of participants saved successfully", font="Lato 14", foreground='green',
                  justify='center').pack(pady=20, padx=20)
            self.add_participants_window.withdraw()
            self.display_participants_window.withdraw()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def hide_schedule_meeting(self):
        """
        The method hides the window for scheduling a meeting a displays the main page.

        :return: displays the main page and creates a window with an exception if encountered
        """
        try:
            self.meeting_name.pack_forget()
            self.select_day.pack_forget()
            self.select_time_start.pack_forget()
            self.select_time_end.pack_forget()
            self.select_participants.pack_forget()
            self.see_participants.pack_forget()
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

    def save_schedule(self):
        """
        The method saves the meeting into the database with all the information we have completed,
        displaying the main page afterwards.

        :return: creates a success window if the meeting is added into the database
                 or creates a window with an exception if encountered
        """
        if self.meeting_day and self.hour_meeting_start and self.min_meeting_start and self.hour_meeting_end and self.min_meeting_end and self.list_participants:
            try:
                self.db.insert_meeting(self.meeting_name.get(), self.meeting_day,
                                       self.hour_meeting_start + ":" + self.min_meeting_start,
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
        """
        The method creates a new window with a calendar from which the user can choose the day for the meeting.

        :return: creates a calendar window and creates a window with an exception if encountered
        """
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
        """
        The method selects and saves the day for a meeting, closing the respective window.

        :return: selects the day for a meeting and creates a window with an exception if encountered
        """
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
        """
        The method displays a new window where the user can write the start hour or end hour for the meeting.

        :param is_start_hour: representing if the user chooses the start or end hour for the meeting

        :return: creates a new window for picking a hour and creates a window with an exception if encountered
        """
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
        """
        The method validates the input of the user when choose an hour.
        This way the user can only give as input digits.

        :param input: represents the input of the user for the hour

        :return: validates the user's input and creates a window with an exception if encountered
        """
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
        """
        The method saves the input for the hour the user chose.

        :param is_start_hour: represents if the user gave an input for the start or end hour

        :return: saves the start and end hours and creates a window with an exception if encountered
        """
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
        """
        The method validates the numbers the user introduced so that they correspond to a valid hour and minutes
        and so that the ending hour is always after the start hour.

        :param hour: represents the hour the user chose

        :param min: represents the minutes the user chose

        :param is_start_hour: represents whether the user chose the start or end hour

        :param time_no_valid: represents a label with a warning that the time is not valid

        :return: validates the time for user's input and creates a window with an exception if encountered
        """
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

    def exit(self):
        """
        The method ends the application.

        :return: end the app and creates a window with an exception if encountered
        """
        try:
            self.root.destroy()
        except Exception as error:
            failure_window = Toplevel(self.root)
            Label(failure_window, text=error, font="Lato 14", foreground='red', justify='center').pack(pady=20, padx=20)

    def create_styles(self):
        """
        The method creates some styles for the buttons so that we can reuse it.

        :return: creates styled buttons and creates a window with an exception if encountered
        """
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
    """
    The main function where the app is created and the connection to the database is established.
    
    :return: creates a window with an exception if encountered
    """
    try:
        db = DB_manager.DB_manager()
        db.connect()
        # db.create_tables()
        app = App(db)
        app.start()
    except Exception as error:
        print(error)
