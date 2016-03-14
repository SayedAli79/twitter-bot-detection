import sqlite3


class DataBase(object):
    def __init__(self, database_name):
        self.database_name = database_name

    def create_db(database_name='bot_detection.db'):
        conn = sqlite3.connect(database_name)

    def create_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute('''CREATE TABLE TWEETS
       (ID INT PRIMARY KEY      NOT NULL,
       NAME            TEXT     NOT NULL,
       DATE            TEXT     NOT NULL,
       TEXT            TEXT     NOT NULL,
       MENTIONS        TEXT     NOT NULL);''')
        conn.close()

    def feed_table(self, tweet_id, followers_name, tweet_date, tweet_text, tweet_mentions):
        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO TWEETS (ID,NAME,DATE,TEXT,MENTIONS) VALUES (?,?,?,?,?)",
                     (tweet_id, followers_name, tweet_date, tweet_text, tweet_mentions))

        conn.commit()
        conn.close()
