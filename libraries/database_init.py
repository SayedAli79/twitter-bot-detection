import sqlite3

class DataBase(object):

    def create_db(database_name='bot_detection.db'):


        conn = sqlite3.connect(database_name)
    
    def create_table(database_name='bot_detection.db'):
    

        conn = sqlite3.connect(database_name)
        conn.execute('''CREATE TABLE TWEETS
       (ID INT PRIMARY KEY      NOT NULL,
       NAME            TEXT     NOT NULL,
       DATE            TEXT     NOT NULL,
       TEXT            TEXT     NOT NULL,
       MENTIONS        TEXT     NOT NULL);''')
        conn.close()