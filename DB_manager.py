import psycopg2


class DB_manager:
    """
    A class that manages connection and queries to the database.
    """

    def __init__(self):
        """
        Initialize the database parameters such as the database name,
        the user and password for authentication and the server's host and port
        """
        self.db = "test"
        self.user = "postgres"
        self.password = "1234"
        self.host = "127.0.0.1"
        self.port = "4444"

    def connect(self):
        """
        The method creates a connection to the DB_manager's database

        :return: raises an exception if encountered
        """
        try:
            self.conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host,
                                         port=self.port)
            print("Opened database successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            raise error

    def create_tables(self):
        """
        The method creates tables in the PostgreSQL database.

        The persons table with person_id(PK), person_email(UNIQUE), person_nume, person_prenume
        The meetings table with meeting_id(PK), meeting_name, meeting_day,
        meeting_start(the starting time), meeting_end(the ending time)
        The scheduler table with meeting_id(FK), person_id(FK) and the tuple (meeting_id, person_id) as a PK

        :return: raises an exception if encountered and executes a rollback
        """
        commands = ("""
                CREATE TABLE persons (
                    person_id SERIAL PRIMARY KEY,
                    person_email VARCHAR(255) NOT NULL UNIQUE,
                    person_nume VARCHAR(255) NOT NULL,
                    person_prenume VARCHAR(255) NOT NULL
                )
                """,
                    """
                 CREATE TABLE meetings (
                     meeting_id SERIAL PRIMARY KEY,
                     meeting_name VARCHAR(255) NOT NULL,
                     meeting_day DATE NOT NULL,
                     meeting_start TIME NOT NULL,
                     meeting_end TIME NOT NULL
                 )
                 """,
                    """
                 CREATE TABLE scheduler (
                     meeting_id INTEGER NOT NULL,
                     person_id INTEGER NOT NULL,
                     PRIMARY KEY (meeting_id, person_id),
                     FOREIGN KEY (meeting_id)
                         REFERENCES meetings (meeting_id)
                         ON UPDATE CASCADE ON DELETE CASCADE,
                     FOREIGN KEY (person_id)
                         REFERENCES persons (person_id)
                         ON UPDATE CASCADE ON DELETE CASCADE
                 )
                 """)

        try:
            cur = self.conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            self.conn.commit()
            print("Tables created")
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error

    def drop_tables(self):
        """
        The methos drops the tables, mostly used for testing/development

        :return: raises an exception if encountered and executes a rollback
        """
        commands = ("""DROP TABLE persons CASCADE""",
                    """DROP TABLE meetings CASCADE""",
                    """DROP TABLE scheduler CASCADE""")
        try:
            cur = self.conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            self.conn.commit()
            print("Tables dropped")
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error

    def insert_person(self, email, nume, prenume):
        """
        The method inserts a new person into the persons table with an auto generated id.

        :param email: the email of the person which gets inserted

        :param nume: the first name of the person which gets inserted

        :param prenume: the last name of the person which gets inserted

        :return: raises an exception if encountered and executes a rollback
        """

        try:
            sql = """INSERT INTO persons(person_email, person_nume, person_prenume)
                                                     VALUES(%s,%s,%s) RETURNING person_id;"""
            cur = self.conn.cursor()
            cur.execute(sql, (email, nume, prenume,))
            self.conn.commit()
            print("Person added with id: " + str(cur.fetchone()[0]))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error

    def get_persons(self):
        """
        The method gets all persons from the persons table.

        :return: all fetched rows with all fields or raises an exception if encountered and executes a rollback
        """
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM persons ORDER BY person_id")
            rows = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error
        return rows

    def get_person(self, person_email):
        """
        The method query a person from the persons table by his unique email

        :param person_email: the email of the person we want to get

        :return: the information about the queried person or raises an exception if encountered and executes a rollback
        """
        sql = """SELECT * FROM persons WHERE person_email=%s"""
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (person_email,))
            row = cur.fetchone()
            print(row)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error
        return row

    def insert_meeting(self, name, day, start, end, participants):
        """
        The method inserts a new meeting into the meetings table along with its participants in the scheduler table.
        The participants will be added only if they are already in the persons table.

        :param name: represents the name of the meeting

        :param day: represents the day the meeting is happening

        :param start: represents the start hour of the meeting

        :param end: represents the end hour of the meeting

        :param participants: represents an array with all the emails of the persons who attend the meeting

        :return: raises an exception if encountered and executes a rollback
        """

        try:
            sql = """INSERT INTO meetings(meeting_name, meeting_day, meeting_start, meeting_end)
                                 VALUES(%s,%s,%s,%s) RETURNING meeting_id;"""
            cur = self.conn.cursor()
            cur.execute(sql, (name, day, start, end,))
            meeting_id = cur.fetchone()[0]
            self.conn.commit()
            if len(participants) != 0:
                sql_participants = """SELECT person_id FROM persons WHERE person_email IN ("""
                tuple_participants = tuple(participants)
                for _ in participants:
                    sql_participants += '%s,'
                sql_participants = sql_participants[:-1]
                sql_participants += ');'
                cur.execute(sql_participants, tuple_participants)
                participants_id = cur.fetchall()
                print(participants_id)
                self.conn.commit()
                for participant in participants_id:
                    sql_schedule = """INSERT INTO scheduler(meeting_id, person_id)
                                     VALUES(%s,%s);"""
                    cur.execute(sql_schedule, (meeting_id, participant[0]))
                    self.conn.commit()
            print("Meeting added successfully with id: " + str(meeting_id))
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error

    def get_meetings(self):
        """
        The method gets all meetings from the meetings table.

        :return: all fetched rows with all fields or raises an exception if encountered and executes a rollback
        """

        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT * FROM meetings ORDER BY meeting_start")
            rows = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error
        return rows

    def get_scheduler(self):
        """
        The method gets all the schedules from the scheduler table.
        A schedule is formed of a meeting_id and a person_id attending to the meeting.

        :return: raises an exception if encountered and executes a rollback
        """

        try:
            cur = self.conn.cursor()
            cur.execute("SELECT meeting_id, person_id FROM scheduler ORDER BY meeting_id")
            row = cur.fetchone()
            while row is not None:
                print(row)
                row = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error

    def get_meetings_by_interval(self, day, start, end):
        """
        The method gets the meetings from the meetings table within an interval of time.

        :param day: the day from which we are searching the meeting

        :param start: the start hour of the earliest meeting representing the min part of the interval

        :param end: the end hour of the latest meeting representing the max part of the interval

        :return: all fetched rows with all the fields or raises an exception if encountered and executes a rollback
        """

        try:
            sql = """SELECT meeting_name, meeting_day, meeting_start, meeting_end, meeting_id FROM meetings WHERE meeting_day=%s 
            AND meeting_start >= %s AND meeting_end <= %s; """
            cur = self.conn.cursor()
            cur.execute(sql, (day, start, end,))
            rows = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error
        return rows

    def get_scheduler_by_meeting(self, meeting_id):
        """
        The method gets the schedules from the scheduler table by a given meeting_id.
        We use this when we want to see all the participants from a meeting.

        :param meeting_id: the meeting which we are search for

        :return: a list of email addresses of the participants of the meeting
                 or raises an exception if encountered and executes a rollback
        """

        try:
            sql = """SELECT person_email FROM persons WHERE person_id IN (SELECT person_id FROM scheduler WHERE 
            meeting_id = %s); """
            cur = self.conn.cursor()
            cur.execute(sql, (meeting_id,))
            rows = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            cur = self.conn.cursor()
            cur.execute("""rollback;""")
            self.conn.commit()
            cur.close()
            raise error
        return rows

# try:
#     db = DB_manager()
#     db.connect()
#     # db.drop_tables()
#     # db.create_tables()
#     # db.insert_person("anrebeca@gmail.com", "Ana", "Rebeca")
#     # db.insert_person("anarebeca@gmail.com", "Ana", "Rebeca")
#     # db.get_person('anrebeca@gmail.com')
#     # db.get_persons()
#     # db.insert_meeting('Facultate', '2020-12-07', '10:00', '15:10', {'isim@yahoo.com', 'anrebeca@gmail.com'})
#     # print(db.get_meetings())
#     # db.get_scheduler()
#     # db.get_scheduler_by_meeting('3')
# #     db.get_meetings_by_interval('2020-12-06', '10:00', '17:00')
# #     db.get_scheduler_by_meeting('12')
# except Exception as error:
#     print(error)
