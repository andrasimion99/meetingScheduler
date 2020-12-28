import psycopg2


class DB_manager:
    """

    """
    def __init__(self):
        """

        """
        self.db = "test"
        self.user = "postgres"
        self.password = "1234"
        self.host = "127.0.0.1"
        self.port = "4444"

    def connect(self):
        """

        :return:
        """
        try:
            self.conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host,
                                         port=self.port)
            print("Opened database successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            raise error

    def create_tables(self):
        """

        :return:
        """
        """ create tables in the PostgreSQL database"""
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

        :return:
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

        :param email:
        :param nume:
        :param prenume:
        :return:
        """
        """ insert a new person into the persons table """

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

        :return:
        """
        """ get all persons from the persons table """
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

        :param person_email:
        :return:
        """
        """ query person from the persons table by id"""
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

        :param name:
        :param day:
        :param start:
        :param end:
        :param participants:
        :return:
        """
        """ insert a new meeting into the meetings table """
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

        :return:
        """
        """ get all meetings from the meetings table """
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

        :return:
        """
        """get the schedules from the scheduler table """
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

        :param day:
        :param start:
        :param end:
        :return:
        """
        """get the meetings from the meetings table within an interval of time"""
        try:
            sql = """SELECT meeting_name, meeting_day, meeting_start, meeting_end, meeting_id FROM meetings WHERE meeting_day=%s 
            AND meeting_start >= %s AND meeting_end <= %s; """
            cur = self.conn.cursor()
            cur.execute(sql, (day, start, end,))
            rows = cur.fetchall()
            # print(rows)
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

        :param meeting_id:
        :return:
        """
        """get the schedules from the scheduler table by a meeting_id"""
        try:
            sql = """SELECT person_email FROM persons WHERE person_id IN (SELECT person_id FROM scheduler WHERE 
            meeting_id = %s); """
            cur = self.conn.cursor()
            cur.execute(sql, (meeting_id,))
            rows = cur.fetchall()
            # print(rows)
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
