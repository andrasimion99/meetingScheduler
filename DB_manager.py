import psycopg2


class DB_manager:
    def __init__(self):
        self.db = "test"
        self.user = "postgres"
        self.password = "1234"
        self.host = "127.0.0.1"
        self.port = "4444"

    def connect(self):
        self.conn = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host,
                                     port=self.port)
        print("Opened database successfully")

    def create_tables(self):
        """ create tables in the PostgreSQL database"""
        commands = ("""
                CREATE TABLE persons (
                    person_id SERIAL PRIMARY KEY,
                    person_nume VARCHAR(255) NOT NULL,
                    person_prenume VARCHAR(255) NOT NULL
                )
                """,
                    """
                 CREATE TABLE meetings (
                     meeting_id SERIAL PRIMARY KEY,
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
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            self.conn.commit()
            print("Tables created")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
