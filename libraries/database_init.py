import sqlite3


class DataBase(object):
    def __init__(self, database_name):
        self.database_name = database_name

    def create_db(self):
        conn = sqlite3.connect(self.database_name)

    def create_table(self): 
        conn = sqlite3.connect(self.database_name)
        conn.execute('''DROP TABLE {tn} IF EXISTS;'''.format(tn=self.table_name))
        conn.execute('''CREATE TABLE {tn}
           (ID INT PRIMARY KEY      NOT NULL,
           NAME            TEXT     NOT NULL,
           DATE            TEXT     NOT NULL,
           TEXT            TEXT     NOT NULL,
           MENTIONS        TEXT     NOT NULL);'''.format(tn=self.table_name))
        conn.close()

    def feed_table(self, tweet_id, followers_name, tweet_date, tweet_text, tweet_mentions):
        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO TWEETS (ID,NAME,DATE,TEXT,MENTIONS) VALUES (?,?,?,?,?)",
                     (tweet_id, followers_name, tweet_date, tweet_text, tweet_mentions))

        conn.commit()
        conn.close()
