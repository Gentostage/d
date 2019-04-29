import sqlite3 as sql
from flask import Flask

DATABASE = './db/database.sqlite'


class database:
    def __init__(self):
        conn = self.get_db()
        cur = self.get_db().cursor()
        cur.execute("""CREATE TABLE  IF NOT EXISTS data 
                        (title TEXT,
                        data )
                    """)
        conn.commit()

        cur.execute("""INSERT INTO data
                          VALUES ('Test')
                          """)
        conn.commit()

        sql = "SELECT * FROM data"
        cur.execute(sql)
        print(cur.fetchall())

    def get_db(self):
        db = getattr(Flask, '_database', None)
        if db is None:
            db = Flask._database = sql.connect(DATABASE)
        return db

    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
