import psycopg2

conn = psycopg2.connect(database="test", user="postgres", password="1234", host="127.0.0.1", port="4444")

print("Opened database successfully")


def create_tables():
    """ create tables in the PostgreSQL database"""
    # command = """
    # CREATE TABLE persons (
    #     person_id SERIAL PRIMARY KEY,
    #     person_nume VARCHAR(255) NOT NULL,
    #     person_prenume VARCHAR(255) NOT NULL
    # )
    # """
    # command = """DROP TABLE meetings;"""
    # command = """
    #     CREATE TABLE meetings (
    #         meeting_id SERIAL PRIMARY KEY,
    #         meeting_day DATE NOT NULL,
    #         meeting_start TIME NOT NULL,
    #         meeting_end TIME NOT NULL
    #     )
    #     """
    command = """
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
            """

    try:
        cur = conn.cursor()
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print("Tables created")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# create_tables()


def insert_person(nume, prenume):
    """ insert a new person into the persons table """
    sql = """INSERT INTO persons(person_nume, person_prenume)
                 VALUES(%s,%s) RETURNING person_id;"""
    person_id = None
    try:
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (nume, prenume,))
        # get the generated id back
        person_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return person_id


# print(insert_person("Filimon", "Raluca"))

def get_persons():
    """ query data from the vendors table """
    try:
        cur = conn.cursor()
        cur.execute("SELECT person_id, person_nume, person_prenume FROM persons ORDER BY person_id")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# get_persons()

# ar trebui sa fac dupa numar matricol
def get_person(nume, prenume):
    """ query data from the vendors table """
    person_id = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT person_id FROM persons WHERE person_nume = %s AND person_prenume = %s", (nume, prenume))
        person_id = cur.fetchone()[0]

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return person_id


def insert_meeting(day, start, end, participants):
    """ insert a new person into the persons table """
    sql = """INSERT INTO meetings(meeting_day, meeting_start, meeting_end)
                 VALUES(%s,%s,%s) RETURNING meeting_id;"""
    meeting_id = None
    try:
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (day, start, end,))
        # get the generated id back
        meeting_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()

        for participant in participants:
            sql_schedule = """INSERT INTO scheduler(meeting_id, person_id)
                             VALUES(%s,%s);"""
            person_id = get_person(participant[0], participant[1])
            cur.execute(sql_schedule, (meeting_id, person_id))
            conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# print(insert_meeting('2020-12-06 15:10:00', '2020-12-06 16:10:00'))
# print(insert_meeting('2020-12-06', '15:00', '16:10'))
# insert_meeting('2020-12-05', '15:00', '16:10', [("Simion", "Andra"), ("Filimon", "Raluca")])


def get_meetings():
    """ query data from the vendors table """
    try:
        cur = conn.cursor()
        cur.execute("SELECT meeting_id, meeting_day, meeting_start, meeting_end FROM meetings ORDER BY meeting_start")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()
            # print(row[1], row[2])
            # print(row[2] < row[3])
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# get_meetings()


def get_scheduler():
    """ query data from the vendors table """
    try:
        cur = conn.cursor()
        cur.execute("SELECT meeting_id, person_id FROM scheduler ORDER BY meeting_id")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


get_scheduler()
